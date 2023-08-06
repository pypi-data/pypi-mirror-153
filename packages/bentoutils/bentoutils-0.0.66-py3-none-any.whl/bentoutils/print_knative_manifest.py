import os
import re
import sys
import yaml


def gen_manifest(pod_name, version, registry='registry.devsheds.io', node_selector=None, svcname=None, tolerations=None, auth=False):
    envvars = read_env_variables()
    env = [{'name': key, 'value': val} for key, val in envvars.items()]
    if auth:
        # Specify PORT to direct the app to listen on 5000.
        # For a different port, be sure to change oauth2_proxy.cfg
        # where it referenced 5000.
        env.append({'name': 'PORT', 'value': '5000'})

    manifest = {
        'apiVersion': 'serving.knative.dev/v1',
        'kind': 'Service',
        'metadata': {
            'name': svcname or pod_name,
            'namespace': 'default',
        },
        'spec': {
            'template': {
                'spec': {
                    'containers': [
                        {
                            'image': '{}/{}:{}'.format(registry, pod_name, version),
                            'args': [
                                '--workers=1',
                                '--timeout=1000000000'
                            ],
                            'env': env,
                            # big models are taking a long time to start
                            'livenessProbe': {
                                'httpGet': {
                                    'path': '/healthz',
                                },
                                'initialDelaySeconds': 3,
                                'periodSeconds': 5,
                            },
                            'readinessProbe': {
                                'httpGet': {
                                    'path': '/healthz',
                                },
                                'initialDelaySeconds': 3,
                                'periodSeconds': 5,
                                'failureThreshold': 3,
                                'timeoutSeconds': 60*5,
                            },
                        },
                    ],
                    'tolerations': convertTolerations(tolerations),
                },
            },
        },
    }
    if envvars.get('GPU_ENABLED', None) == 'true':
        manifest['spec']['template']['spec']['containers'][0]['resources'] = {
            'limits': {
                'nvidia.com/gpu': 1
            }
        }

    replicas = int(envvars.get('MIN_REPLICAS', '0'))
    if replicas > 0:
        manifest['spec']['template']['metadata'] = {
            'annotations': {
                'autoscaling.knative.dev/minScale': str(replicas)
            }
        }

    if node_selector:
        manifest['spec']['template']['spec']['nodeSelector'] = node_selector

    if auth:
        manifest['spec']['template']['spec']['containers'].append({
            'name': 'oauth2-proxy',
            'image': 'quay.io/oauth2-proxy/oauth2-proxy',
            'command': ['/bin/oauth2-proxy'],
            'args': ['--config=/etc/proxy-config/oauth2_proxy.cfg'],
            'volumeMounts': [
                {
                    'name': 'proxy-config',
                    'mountPath': '/etc/proxy-config/',
                },
            ],
            # multi-container: enabled requires exactly one container
            # to specify a port, so that we know where to route traffic
            # We also currently limit where readiness and liveness 
            # probes may occur to this container.
            'ports': [
                {
                    'containerPort': 8081,
                },
            ],
        })
        manifest['spec']['template']['spec']['volumes'] = [
            {
                'name': 'proxy-config',
                'secret': {
                    'secretName': 'oauth2-proxy-config',
                },
            },
        ]
    else:
        manifest['spec']['template']['spec']['containers'][0]['ports'] = [
            {
                'containerPort': 5000,
            },
        ]

    return yaml.dump(manifest)


def camel_to_kebab(name):
    out = re.sub(r'([a-z0-9]|(?=[A-Z]))([A-Z])', r'\1-\2', name)
    out = out.lower()
    if out[0] == '-':
        out = out[1:]
    return out


def read_env_variables():
    envvars = {}
    if not os.path.exists('.env'):
        return envvars

    with open('.env', 'r') as f:
        for line in f:
            key, val = line.split('=')
            envvars[key] = val.strip()

    return envvars


def convertTolerations(tolerations_str):
    if tolerations_str is None:
        return []

    pairs = [[y.strip() for y in x.strip().split('=')]
             for x in tolerations_str.split(',')]
    tolerations = []
    for key, value in pairs:
        tolerations.append({
            'key': key,
            'operator': 'Equal',
            'value': value,
            'effect': 'NoSchedule',
        })
    return tolerations


if __name__ == '__main__':
    bento = str(sys.argv[1])
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    if len(sys.argv) == 4:
        pod_name = str(sys.argv[2])
        registry = str(sys.argv[3])
        print(gen_manifest(pod_name, version, registry))

    else:
        print('Error: insufficient args')
