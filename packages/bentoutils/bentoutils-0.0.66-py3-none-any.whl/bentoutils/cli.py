import os
import sys

import boto3
import click
import uuid
from bentoml.exceptions import BentoMLException
from bentoml.utils.lazy_loader import LazyLoader
from botocore.client import Config
from kubernetes import client

from bentoutils.kubeutil import from_yaml, delete_from_yaml
from bentoutils.print_kaniko_manifest import camel_to_kebab, gen_manifest as gen_kaniko_manifest, gen_docker_manifest
from bentoutils.print_knative_manifest import gen_manifest as gen_knative_manifest
from bentoutils.print_route_manifest import gen_manifest as gen_route_manifest

yatai_proto = LazyLoader('yatai_proto', globals(), 'bentoml.yatai.proto')


@click.command()
@click.option('--module', help='fully qualified module name containing service to package')
@click.option('--clz', help='class name of service to package')
@click.option('--name', help='model name')
@click.option('--path', help='directory path of pretrained model')
@click.option('--labels', help='comma separated list of key:val pairs')
@click.option('--files', help='comma separated list of file paths to add')
@click.option('--opts', help='comma separated list of key=val pairs')
@click.option('--update', is_flag=True, help='update opts instead of replace')
def pack(module, clz, name, path, labels=None, files=None, opts=None, update=False):
    # Create a service instance
    svc = get_instance(module, clz)

    names = [x.strip() for x in name.split(',')] if name else []
    paths = [x.strip() for x in path.split(',')] if path else []
    if ((len(names) + len(paths)) / 2 != len(names)):
        raise click.BadParameter('length of names, paths does not match')

    for i, name in enumerate(names):
        if opts is not None:
            opts = convert_labels(opts)

        # Package the pretrained model artifact
        svc.pack(name, paths[i], opts=opts, update=update)
    
    if files is not None:
        filepaths = [x.strip() for x in files.split(',')]
        for fp in filepaths:
            with open(fp, 'r') as f:
                content = f.read()

            filename, ext = os.path.splitext(os.path.basename(fp))
            svc.pack(filename, content)

    if labels is None:
        labels = {}
    else:
        labels = convert_labels(labels)

    # Save the service to the model registry for serving
    saved_path = svc.save(labels=labels)

    #print('Saved model to ' + saved_path)
    click.echo(saved_path)


# The `__import__` function will return the top level module of a package, 
# unless you pass a nonempty `fromlist` argument
# https://stackoverflow.com/questions/9806963/how-to-use-the-import-function-to-import-a-name-from-a-submodule
def get_instance(module_name, class_name):
    module = __import__(module_name, fromlist=['object'])
    class_ = getattr(module, class_name)
    return class_()


def convert_value(val):
    if val == 'True':
        return True
    elif val == 'False':
        return False
    # elif val.isdigit():
    #     return int(val)
    # try:
    #     return float(val)
    # except ValueError:
    #     return val
    return val


def convert_labels(labels_str):
    pairs = [[y.strip() for y in x.strip().split('=')]
             for x in labels_str.split(',')]
    return {p[0]:convert_value(p[1]) for p in pairs}


@click.command()
@click.option('--module', help='fully qualified module name containing service to package')
@click.option('--clz', help='class name of service to package')
@click.option('--name', help='model name')
@click.option('--bucket', help='bucket name of pretrained model')
@click.option('--path', help='directory path of pretrained model')
@click.option('--labels', help='comma separated list of key=val pairs')
@click.option('--files', help='comma separated list of file paths to add')
@click.option('--opts', help='comma separated list of key=val pairs')
@click.option('--update', is_flag=True, help='update opts instead of replace')
@click.option('--no_ssl', is_flag=True, help='do not use SSL')
@click.option('--no_verify_ssl', is_flag=True, help='do not verify SSL')
def pack_from_s3(module, clz, name, bucket, path, labels=None, files=None, opts=None, update=False, no_ssl=False, no_verify_ssl=False):
    s3 = boto3.resource('s3',
        endpoint_url=os.environ['S3_ENDPOINT_URL'],
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4'),
        region_name='us-east-1',
        use_ssl=(not no_ssl),
        verify=(False if no_verify_ssl else None),
    )

    def download_directory(bucket_name, directory, local_directory=None):
        if local_directory is None:
            local_directory = os.path.join('/tmp', bucket_name, directory)

        if not os.path.exists(local_directory):
            os.makedirs(local_directory)

        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=directory):
            target = os.path.join(local_directory, os.path.relpath(obj.key, directory))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            bucket.download_file(obj.key, target)

    names = [x.strip() for x in name.split(',')] if name else []
    buckets = [x.strip() for x in bucket.split(',')] if bucket else []
    paths = [x.strip() for x in path.split(',')] if path else []
    if ((len(names) + len(buckets) + len(paths)) / 3 != len(names)):
        raise click.BadParameter('length of names, buckets, paths does not match')

    # Create a service instance
    svc = get_instance(module, clz)
    if opts is not None:
        opts = convert_labels(opts)

    for i, name in enumerate(names):
        tmp_path = '/tmp/{}/{}'.format(buckets[i], paths[i])

        if not os.path.exists(tmp_path):
            download_directory(buckets[i], paths[i])

        # Package the pretrained model artifact
        svc.pack(name, tmp_path, opts=opts, update=update)

    if files is not None:
        filepaths = [x.strip() for x in files.split(',')]
        for fp in filepaths:
            with open(fp, 'r') as f:
                content = f.read()

            filename, ext = os.path.splitext(os.path.basename(fp))
            svc.pack(filename, content)

    if labels is None:
        labels = {}
    else:
        labels = convert_labels(labels)

    # Save the service to the model registry for serving
    saved_path = svc.save(labels=labels)

    click.echo(saved_path)


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
def get_pod_name(bento):
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    pod_name = camel_to_kebab(name)
    click.echo(pod_name)
    return pod_name


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--path', help="path to saved artifacts")
@click.option('--registry', help="private registry in 'host:port' format")
@click.option('--s3_endpoint', help="S3 endpoint URL", default=None)
@click.option('--insecure', is_flag=True, help='do not use SSL')
@click.option('--isdockerconfig', is_flag=True, help='use docker config format')
@click.option('--uid', help="unique ID")
def get_kaniko_manifest(bento, path, registry, s3_endpoint, insecure=False, isdockerconfig=False, uid=None, silent=False):
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    if uid is None:
        uid = str(uuid.uuid4())[:5]

    image_name = camel_to_kebab(name)
    pod_name = '{}-{}'.format(image_name, uid)
    if isdockerconfig:
        manifest = gen_docker_manifest(name, pod_name, image_name, version, path, registry=registry, s3_endpoint=s3_endpoint, insecure=insecure)
    else:
        manifest = gen_kaniko_manifest(name, pod_name, image_name, version, path, registry=registry, s3_endpoint=s3_endpoint, insecure=insecure)
    if not silent: click.echo(manifest)
    return manifest, pod_name


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--registry', help="private registry in 'host:port' format")
@click.option('--selector', help='comma separated list of key=val pairs')
@click.option('--svcname', help='service name')
@click.option('--tolerations', help='tolerations')
@click.option('--auth', is_flag=True, help='secure endpoints using oauth2')
def get_knative_manifest(bento, registry, selector=None, svcname=None, tolerations=None, auth=False):
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    pod_name = camel_to_kebab(name)
    if selector is not None:
        selector = convert_labels(selector)

    manifest = gen_knative_manifest(pod_name, version, registry, selector, svcname, tolerations, auth)
    click.echo(manifest)
    return manifest


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--currev', help="current knative revision name")
@click.option('--newrev', help="new knative revision name")
@click.option('--percent', help="percent to route to new revision")
def get_route_manifest(bento, currev, newrev, percent):
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    pod_name = camel_to_kebab(name)
    manifest = gen_route_manifest(pod_name, currev, newrev, percent)
    click.echo(manifest)
    return manifest


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
def get_saved_path(bento, silent=False):
    # Get saved path
    yatai_client = get_default_yatai_client()
    result = None
    try:
        result = yatai_client.repository.get(bento)
    except BentoMLException as e:
        click.echo(str(e))
        sys.exit(1)

    if result is None:
        return None

    saved_path = result.uri.uri
    if not silent: click.echo(saved_path)
    return saved_path


@click.command()
@click.option('--labels', help="labels to find bento")
def first_bento_with_label(labels):
    yatai_client = get_default_yatai_client()
    bentos = []
    try:
        bentos = yatai_client.repository.list(labels=labels)
    except BentoMLException as e:
        click.echo(str(e))
        sys.exit(1)
    
    if len(bentos) == 0:
        return None

    bento = bentos[0]
    click.echo(f'{bento.name}:{bento.version}')


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--registry', help="private registry in 'host:port' format")
@click.option('--s3_endpoint', help="S3 endpoint URL", default=None)
@click.option('--insecure', is_flag=True, help='do not use SSL')
@click.option('--isdockerconfig', is_flag=True, help='use docker config format')
@click.pass_context
def containerize(ctx, bento, registry, s3_endpoint, insecure=False, isdockerconfig=False):
    path = ctx.invoke(get_saved_path, bento=bento, silent=True)
    manifest, pod_name = ctx.invoke(get_kaniko_manifest, bento=bento, path=path, registry=registry, s3_endpoint=s3_endpoint, insecure=insecure, isdockerconfig=isdockerconfig, silent=True)
    from_yaml(manifest)
    click.echo(pod_name)
    return pod_name


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--pod', help="pod name")
@click.option('--registry', help="private registry in 'host:port' format")
@click.option('--isdockerconfig', is_flag=True, help='use docker config format')
@click.pass_context
def delete_containerize_job(ctx, bento, pod, registry, isdockerconfig=False):
    path = ctx.invoke(get_saved_path, bento=bento)
    uid = pod.split('-')[-1]
    manifest, pod_name = ctx.invoke(get_kaniko_manifest, bento=bento, path=path, registry=registry, isdockerconfig=isdockerconfig, uid=uid)
    delete_from_yaml(manifest)


@click.command()
@click.option('--bento', help='bento service name')
@click.option('--registry', help='registry name')
@click.option('--selector', help='comma separated list of key=val pairs')
@click.option('--svcname', help='service name')
@click.option('--tolerations', help='tolerations as comma separated list of key=val pairs')
@click.option('--auth', is_flag=True, help='secure endpoints using oauth2')
@click.pass_context
def deploy_to_knative(ctx, bento, registry, selector=None, svcname=None, tolerations=None, auth=False):
    manifest = ctx.invoke(get_knative_manifest, bento=bento, registry=registry, selector=selector, svcname=svcname, tolerations=tolerations, auth=auth)
    from_yaml(manifest)

    # Build Docker image
    # client = docker.from_env()
    # tag = f'{registry}/{name}:{version}'
    # client.images.build(path=saved_path, tag=tag)
    # for line in client.push(tag, stream=True, decode=True):
    #     print(line)

    
    # Generate KNative manifest
    # output_dir = tempfile.TemporaryDirectory(dir='/tmp')
    # root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # resources_dir = os.path.join(root_dir, 'templates/knative')
    # env = Environment(loader=FileSystemLoader(resources_dir))
    # template = env.get_template('service.yaml')
    # svc_name = stringcase.spinalcase(name)
    # yaml_file = os.path.join(output_dir, 'service.yaml')
    # template.stream(name=svc_name, registry=registry).dump(yaml_file)

    # # Deploy to KNative
    # from_yaml(yaml_file)

    # # Cleanup
    # output_dir.cleanup()


def get_default_yatai_client():
    from bentoml.yatai.client import YataiClient

    return YataiClient()


# This function assumes the status is not status.OK
def status_pb_to_error_code_and_message(pb_status) -> (int, str):
    from bentoml.yatai.proto import status_pb2

    assert pb_status.status_code != status_pb2.Status.OK
    error_code = status_pb2.Status.Code.Name(pb_status.status_code)
    error_message = pb_status.error_message
    return error_code, error_message
