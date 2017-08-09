# k8_dind

Docker-in-docker daemon for Kubernetes deployer/handler  
required python 2.7 with kubernetes module (pip install kubernetes==2), tested on windows

python k8_dind3.py --help  
usage: k8_dind3.py [-h] [-c string] [-start] [-stop] -name NAME  
                   [-docker DOCKER]  
  
optional arguments:  
  -h, --help      show this help message and exit  
  -c string       k8 config file path  
  -start          start daemon  
  -stop           stop daemon  
  -name NAME      dind container name, required parameter  
  -docker DOCKER  docker container to pull  
  
run example   
python k8_dind3.py -name dind -start  

