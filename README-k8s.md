# MyFood order & pay solution
## Requirements
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
## Usage
Follow these steps in the root directory of your local cloned repository:
- Run the following commands:
    ```
    minikube start minikube
    minikube ip
    eval $(minikube docker-env)
    docker build . -t my-food-app:latest
    kubectl apply -f k8s/db
    kubectl apply -f k8s/api
    ```
## API Documentation UI
[Swagger](https://swagger.io/tools/swagger-ui/) specification is available in http://(minikube-ip):(api-svc-port)/docs
