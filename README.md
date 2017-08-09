# k8_dind

Docker-in-docker daemon for Kubernetes deployer/handler  
required python 2.7 with kubernetes module (pip install kubernetes==2), tested on windows with minikube

python k8_dind3.py --help  
usage: k8_dind3.py [-h] [-c string] [-start] [-stop] -name NAME  
                   [-docker DOCKER]  
  
optional arguments:  
  -h, --help      show this help message and exit  
  -c string       k8 config file path  
  -start          start daemon  
  -stop           stop daemon  
  -name NAME      dind container name, required parameter  
  -docker DOCKER  docker container to pull, syntax of container naming 'docker:<dind_contaner_name-version>'
  
run example   
python k8_dind3.py -name dind -start  

docker:dind deploying by default, you can specify dind version by -docker option.  
K8 config will try to find in system if path not specified
