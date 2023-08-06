import re
import sys
import uuid
import yaml


def gen_manifest(name, pod_name, image_name, version, saved_path, registry='docker-registry.default.svc.cluster.local:5000', s3_endpoint='http://minio.minio.svc.cluster.local:9000', insecure=False):
    args = [
        '--dockerfile=Dockerfile',
        '--context={}'.format(saved_path),
        '--context-sub-path={}'.format(name),
        '--destination={}/{}:{}'.format(registry, image_name, version),
        '--snapshotMode=redo',
    ]
    if insecure:
        args.append('--insecure')
        args.append('--skip-tls-verify')

    manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': pod_name,
        },
        'spec': {
            'containers': [
                {
                    'name': image_name,
                    'image': 'gcr.io/kaniko-project/executor:v1.7.0',
                    'args': args,
                    'volumeMounts': [
                        {
                            'name': 'kaniko-secret',
                            'mountPath': '/secret',
                        },
                    ],
                    'env': [
                        {
                            'name': 'GOOGLE_APPLICATION_CREDENTIALS',
                            'value': '/secret/kaniko-secret.json',
                        },
                        {
                            'name': 'AWS_ACCESS_KEY_ID',
                            'value': 'minio',
                        },
                        {
                            'name': 'AWS_SECRET_ACCESS_KEY',
                            'valueFrom': {
                                'secretKeyRef': {
                                    'name': 'aws-secret-access-key',
                                    'key': 'pat',
                                }
                            }
                        },
                        {
                            'name': 'AWS_REGION',
                            'value': 'us-east-1',
                        },
                        {
                            'name': 'S3_ENDPOINT',
                            'value': s3_endpoint,
                        },
                        {
                            'name': 'S3_FORCE_PATH_STYLE',
                            'value': 'true',
                        },
                    ],
                },
            ],
            'restartPolicy': 'Never',
            'volumes': [
                {
                    'name': 'kaniko-secret',
                    'secret': {
                        'secretName': 'kaniko-secret',
                    },
                },
            ],
        },
    }
    return yaml.dump(manifest)


def gen_docker_manifest(name, pod_name, image_name, version, saved_path, registry='docker-registry.default.svc.cluster.local:5000', s3_endpoint='http://minio.minio.svc.cluster.local:9000', insecure=False):
    args = [
        '--dockerfile=Dockerfile',
        '--context={}'.format(saved_path),
        '--context-sub-path={}'.format(name),
        '--destination={}/{}:{}'.format(registry, image_name, version),
        '--snapshotMode=redo',
    ]
    if insecure:
        args.append('--insecure')
        args.append('--skip-tls-verify')

    manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': pod_name,
        },
        'spec': {
            'containers': [
                {
                    'name': image_name,
                    'image': 'gcr.io/kaniko-project/executor:v1.7.0',
                    'args': args,
                    'volumeMounts': [
                        {
                            'name': 'kaniko-secret',
                            'mountPath': '.docker/',
                        },
                    ],
                    'env': [
                        {
                            'name': 'AWS_ACCESS_KEY_ID',
                            'value': 'minio',
                        },
                        {
                            'name': 'AWS_SECRET_ACCESS_KEY',
                            'valueFrom': {
                                'secretKeyRef': {
                                    'name': 'aws-secret-access-key',
                                    'key': 'pat',
                                }
                            }
                        },
                        {
                            'name': 'AWS_REGION',
                            'value': 'us-east-1',
                        },
                        {
                            'name': 'S3_ENDPOINT',
                            'value': s3_endpoint,
                        },
                        {
                            'name': 'S3_FORCE_PATH_STYLE',
                            'value': 'true',
                        },
                    ],
                },
            ],
            'restartPolicy': 'Never',
            'volumes': [
                {
                    'name': 'kaniko-secret',
                    'secret': {
                        'secretName': 'kaniko-secret',
                        'items': [
                            {
                                'key': 'config.json',
                                'path': 'config.json',
                            },
                        ],
                    },
                },
            ],
        },
    }
    return yaml.dump(manifest)


def camel_to_kebab(name):
    out = re.sub(r'([a-z0-9]|(?=[A-Z]))([A-Z])', r'\1-\2', name)
    out = out.lower()
    if out[0] == '-':
        out = out[1:]
    return out


if __name__ == '__main__':
    bento = str(sys.argv[1])
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    image_name = camel_to_kebab(name)
    uid = str(uuid.uuid4())[:5]
    pod_name = '{}-{}'.format(image_name, uid)

    if len(sys.argv) == 4:
        saved_path = str(sys.argv[2])
        registry = str(sys.argv[3])
        print(gen_manifest(name, pod_name, image_name, version, saved_path, registry))
    elif len(sys.argv) == 5:
        saved_path = str(sys.argv[2])
        registry = str(sys.argv[3])
        s3_endpoint = str(sys.argv[4])
        print(gen_manifest(name, pod_name, image_name, version, saved_path, registry, s3_endpoint))
    elif len(sys.argv) == 6:
        saved_path = str(sys.argv[2])
        registry = str(sys.argv[3])
        s3_endpoint = str(sys.argv[4])
        insecure = str(sys.argv[5])
        print(gen_manifest(name, pod_name, image_name, version, saved_path, registry, s3_endpoint, insecure is 'true'))
    else:
        print(pod_name)
