#!/usr/bin/env python3
# This utility attempts to provide functionality similar to `kubectl apply -f`
# - load and parse yaml
# - try to figure out the object type and API to use
# - figure out if the resource already exists, in which case
#   it needs to be patched or replaced alltogether.
# - otherwise just create a new resource.
# See https://stackoverflow.com/questions/36307950/kubernetes-api-call-equivalent-to-kubectl-apply

import kubernetes
import logging
import re
import sys
import yaml
from kubernetes import config

config.load_kube_config()


def from_yaml(raw, client=None, **kwargs):
    ''' Invoke the K8s API to create or replace an object given a YAML spec.

        @param raw: either a string or an open input stream with a YAML formatted 
                    spec, as you would use for `kubectl apply -f`
        @param client: (optional) preconfigured client environment to use for invocation
        @param kwargs: (optional) further arguments to pass to the create/replace call
        @return: response object from the Kubernetes API call
    '''
    for obj in yaml.load_all(raw, Loader=yaml.FullLoader):
        create_update_or_replace(obj, client, **kwargs)


def delete_from_yaml(raw, client=None, **kwargs):
    for obj in yaml.load_all(raw, Loader=yaml.FullLoader):
        delete_object(obj, client, **kwargs)


def create_update_or_replace(obj, client=None, **kwargs):
    ''' Invoke the K8s API to create or replace a Kubernetes object.

        The first attempt is to create (insert) this object. When this is rejected because
        of an existing object with same name, we attempt to patch the existing object.
        As a last resort, if even the patch is rejected, we *delete* the existing object
        and recreate from scratch.

        @param obj: complete object specification including API version and metadata.
        @param client: (optional) preconfigured client environment to use for invocation
        @param kwargs: (optional) further arguments to pass to the create/replace call
        @return: response object from the Kubernetes API call
    '''
    api_instance = find_api_instance(obj, client)
    try:
        res = invoke_api(api_instance, 'create', obj, **kwargs)
        if isinstance(res, dict):
            logging.debug('K8s: %s created -> uid=%s', describe(obj), res['metadata']['uid'])
        else:
            logging.debug('K8s: %s created -> uid=%s', describe(obj), res.metadata.uid)
    except kubernetes.client.rest.ApiException as e:
        if e.reason != 'Conflict':
            raise

        try:
            # asking for forgiveness...
            res = invoke_api(api_instance, 'patch', obj, **kwargs)
            if isinstance(res, dict):
                logging.debug('K8s: %s PATCHED -> uid=%s', describe(obj), res['metadata']['uid'])
            else:
                logging.debug('K8s: %s PATCHED -> uid=%s', describe(obj), res.metadata.uid)
        except kubernetes.client.rest.ApiException as e:
            if e.reason != 'Unprocessable Entity':
                raise

            try:
                # second attempt... delete the existing object and re-insert
                logging.debug('K8s: replacing %s FAILED. Attempting deletion and recreation...', describe(obj))
                res = invoke_api(api_instance, 'delete', obj, **kwargs)
                logging.debug('K8s: %s DELETED...', describe(obj))
                res = invoke_api(api_instance, 'create', obj, **kwargs)
                if isinstance(res, dict):
                    logging.debug('K8s: %s CREATED -> uid=%s', describe(obj), res['metadata']['uid'])
                else:
                    logging.debug('K8s: %s CREATED -> uid=%s', describe(obj), res.metadata.uid)
            except Exception as ex:
                message = 'K8s: FAILURE updating %s. Exception: %s' % (describe(obj), ex)
                logging.error(message)
                raise RuntimeError(message)
    
    return res


def patch_object(obj, client=None, **kwargs):
    api_instance = find_api_instance(obj, client)
    try:
        res = invoke_api(api_instance, 'patch', obj, **kwargs)
        if isinstance(res, dict):
            logging.debug('K8s: %s PATCHED -> uid=%s', describe(obj), res['metadata']['uid'])
        else:
            logging.debug('K8s: %s PATCHED -> uid=%s', describe(obj), res.metadata.uid)
        return res
    except kubernetes.client.rest.ApiException as e:
        if e.reason == 'Unprocessable Entity':
            message = 'K8s: patch for %s rejected. Exception: %s' % (describe(obj), e)
            logging.error(message)
            raise RuntimeError(message)
        else:
            raise


def delete_object(obj, client=None, **kwargs):
    api_instance = find_api_instance(obj, client)
    try:
        res = invoke_api(api_instance, 'delete', obj, **kwargs)
        if isinstance(res, dict):
            logging.debug('K8s: %s DELETED. uid was: %s', describe(obj), res['details'] and res['details']['uid'] or '?')
        else:
            logging.debug('K8s: %s DELETED. uid was: %s', describe(obj), res.details and res.details.uid or '?')
        return True
    except kubernetes.client.rest.ApiException as e:
        if e.reason == 'Not Found':
            logging.warning('K8s: %s does not exist (anymore).', describe(obj))
            return False
        else:
            message = 'K8s: deleting %s FAILED. Exception: %s' % (describe(obj), e)
            logging.error(message)
            raise RuntimeError(message)


def find_api_instance(obj, client=None):
    ''' Investigate the object spec and lookup the corresponding API object.
    
        @param client: (optional) preconfigured client environment to use for invocation
        @return: a client instance wired to the appropriate API
    '''
    grp, _, ver = obj['apiVersion'].partition('/')
    if ver == '':
        ver = grp
        grp = 'core'

    # Strip 'k8s.io', camel-case-join dot separated parts. e.g. rbac.authorization.k8s.io -> RbacAuthorzation
    grp = ''.join(part.capitalize() for part in grp.rsplit('.k8s.io', 1)[0].split('.'))
    ver = ver.capitalize()

    api_instance = '%s%sApi' % (grp, ver)
    if api_instance == 'ServingKnativeDevV1Api':
        api_instance = 'CustomObjectsApi'

    return getattr(kubernetes.client, api_instance)(client)


def invoke_api(api_instance, action, obj, **args):
    ''' Find a suitable function and perform the actual API invocation.

        @param api_instance: client object for the invocation, wired to correct API version
        @param action: either 'create' (to inject a new objet) or 'replace','patch','delete'
        @param obj: the full object spec to be passed into the API invocation
        @param args: (optional) extraneous arguments to pass
        @return: response object from the Kubernetes API call
    '''
    is_custom_objects_api = isinstance(api_instance, kubernetes.client.api.custom_objects_api.CustomObjectsApi)

    # transform ActionType from yaml into action_type for swagger API
    kind = camel_to_snake(obj['kind'])

    # determine namespace to place the object in, supply default
    try:
        namespace = obj['metadata']['namespace']
    except:
        namespace = 'default'

    fn_name = '%s_%s' %(action, kind)
    if hasattr(api_instance, fn_name):
        # namespace agnostic API
        fn = getattr(api_instance, fn_name)
    else:
        fn_name = '%s_namespaced_%s' %(action, kind)
        if is_custom_objects_api:
            if fn_name == 'create_namespaced_service':
                fn_name = 'create_namespaced_custom_object'
            elif fn_name == 'patch_namespaced_service':
                fn_name = 'patch_namespaced_custom_object'

        fn = getattr(api_instance, fn_name)
        args['namespace'] = namespace

    if not 'create' in fn_name:
        args['name'] = obj['metadata']['name']
    
    if 'delete' in fn_name:
        from kubernetes.client.models.v1_delete_options import V1DeleteOptions
        obj = V1DeleteOptions()

    # print(', '.join(map(str, args)))
    if is_custom_objects_api:
        if fn_name == 'create_namespaced_custom_object':
            return fn('serving.knative.dev', 'v1', args['namespace'], 'services', obj)
        elif fn_name == 'patch_namespaced_custom_object':
            return fn('serving.knative.dev', 'v1', args['namespace'], 'services', args['name'], obj)

    return fn(body=obj, **args)


def describe(obj):
    return "%s '%s'" % (obj['kind'], obj['metadata']['name'])


def camel_to_snake(str):
    str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str)
    str = re.sub('([a-z0-9])([A-Z])', r'\1_\2', str).lower()
    return str


if __name__ == '__main__':
    from_yaml(sys.argv[0])
