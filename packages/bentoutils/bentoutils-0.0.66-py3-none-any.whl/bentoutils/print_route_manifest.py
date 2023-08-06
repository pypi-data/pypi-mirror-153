import os
import re
import sys
import yaml


def gen_manifest(pod_name, cur_rev, new_rev, percent):
    manifest = {
        'apiVersion': 'serving.knative.dev/v1',
        'kind': 'Route',
        'metadata': {
            'name': pod_name,
            'namespace': 'default',
        },
        'spec': {
            'traffic': [
                {
                    'revisionName': new_rev,
                    'percent': str(percent),
                },
                {
                    'revisionName': cur_rev,
                    'percent': str(100 - int(percent)),
                },
            ]
        }
    }

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


def main(pod_name, cur_rev, new_rev):
    envvars = read_env_variables()
    percent = int(envvars.get('TRAFFIC_PERCENT', '100'))
    return gen_manifest(pod_name, cur_rev, new_rev, percent)


if __name__ == '__main__':
    pod_name = str(sys.argv[1])
    cur_rev = str(sys.argv[2])
    new_rev = str(sys.argv[3])
    envvars = read_env_variables()
    percent = int(envvars.get('TRAFFIC_PERCENT', '100'))
    if cur_rev.startsWith('Error') or percent == 100:
        print('')
    else:
        print(gen_manifest(pod_name, cur_rev, new_rev, percent))
