import time
from kubernetes import config, client
from kubernetes.client import configuration
from kubernetes.client.apis import core_v1_api
from kubernetes.client.rest import ApiException
import argparse
import sys
import os.path
#remove unicode warnings
import warnings
warnings.filterwarnings("ignore", category=UnicodeWarning)


def startDindPod(name,resp,docker_container='dind'):
 cnt = 0
 if not resp:
    print("Pod %s does not exits. Creating it..." % name)
    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': name
        },
        'spec': {
            'hostname': name,
            'subdomain': 'default-subdomain',
            'containers': [{
                'image': 'docker:'+docker_container,
                'name': name,
                "securityContext":  {
                    "privileged": True }
            }]
        }
    }
    try: 
        resp = api.create_namespaced_pod(body=pod_manifest,
                                     namespace='default')
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    
    while True:
        cnt += 1
        resp = api.read_namespaced_pod_status(name, namespace='default')

        if resp.status.phase != 'Pending':            
            break
        #show message if problem with image pull
        if cnt > 20 and resp.status.container_statuses[0].state.waiting:
            print 'Container failed with reason: '+resp.status.container_statuses[0].state.waiting.reason+'\nCheck container logs'
            sys.exit(1)
            
        time.sleep(1)        

    print("Done.")
 else:
    print("Pod already exist, exiting")
    exit(0)
    
def stopDindPod(name,resp):
 if resp:
    print("Pod %s found. Deleting it..." % name)    
    try:     
       resp = api.delete_namespaced_pod(name=name,namespace='default', body=body, pretty='true') 
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)  
        
    while True:
        try: 
            resp = api.read_namespaced_pod(name=name,
                                       namespace='default')
        except ApiException as e:
            break
        print resp.status
        if resp.status.phase != 'Running' or resp.status.phase != 'Pending':
            break
        time.sleep(1)
    print("Done.")
 else: 
    print("Pod %s not found. Exit"  % name)

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', metavar='string', help='k8 config file path',)
    parser.add_argument('-start', help='stop daemon',action="store_true")
    parser.add_argument('-stop',
                        help='stop daemon',action="store_true")
    parser.add_argument('-name', 
                        help='dind container name',required=True)
    parser.add_argument('-docker', 
                        help='docker container to pull')                   
    args = parser.parse_args()
    return vars(args)


def main():
 args = command_line_args()
 k8_config_path = args['c']
 docker_name = args['name']
 
 if k8_config_path:
    if os.path.isfile(k8_config_path):
     try:
       config.load_kube_config(k8_config_path) 
     except ApiException as e:        
       print("Unknown error: %s" % e)
 else: 
    config.load_kube_config()
 
 
 global api 
 global body
 api = core_v1_api.CoreV1Api() 
 body = client.V1DeleteOptions()   
 configuration.assert_hostname = False
 
 resp = None
 try:
   resp = api.read_namespaced_pod(name=docker_name,
                                   namespace='default')
 except ApiException as e:
   if e.status != 404:
      print("Unknown error: %s" % e)
      exit(1) 

 if args['start'] and args['docker']:
    startDindPod(docker_name,resp,args['docker'])
 elif args['start']:
    startDindPod(docker_name,resp,'dind')
 if args['stop']:
    stopDindPod(docker_name,resp)
    
 if not args['stop'] and not args['start']:
    print 'Please specify what to do with daemon, start or stop'
    sys.exit(1)

# main routine
if __name__=='__main__':
  main()
