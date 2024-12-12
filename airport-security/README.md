In the service folder the collector service resides.
The service can be tested with the others via the docker-compose file with the command

docker compose up --build

All services open the port 80 within their container network. The camera exposes the port 1111 to the outside for
testing purposes. The services were tested with postman on the local machine. The docker compose file does not contain
resource restriction, because this was implemented directly on the GKE cluster. The collector service was developed with
Pycharm locally and then pushed as an image to docker, which can be observed in collector.deployment.yaml.

The kubernetes-manifest files contain every yaml file in order to startup all services on GKE. Beware the grafana yaml is
also in there and should be executed as described in the Assignment sheet. In order to communicate with the GKE deployed
services you have to use the link http://<exposed-External-ip-Address>.nip.io/cam<x>/stream?toggle=on. There are 4 cameras to talk to another camera
simply change the number.

as concrete examples:
curl -v http://34.30.212.46.nip.io/cam1/stream?toggle=on
curl -v http://34.30.212.46.nip.io/cam2/stream?toggle=on
curl -v http://34.30.212.46.nip.io/cam3/stream?toggle=on
curl -v http://34.30.212.46.nip.io/cam4/stream?toggle=on

Also Alert and Section service is reachable via ingress:
Alert Service:
http://34.30.212.46.nip.io/alerts-svc/alerts?from={{startOfDay}}&to={{endOfDay}}&aggregate=count

Section Service:
http://34.30.212.46.nip.io/section-svc/persons?from={{startOfDay}}&to={{endOfDay}}&aggregate=count

Useful  Pre-Request Script in Postman:
let moment = require('moment');
pm.variables.set('startOfDay', moment().utc().startOf('day').format('YYYY-MM-DD HH:mm:ss'));
pm.variables.set('endOfDay', moment().utc().endOf('day').format('YYYY-MM-DD HH:mm:ss'));


Useful Commands to setup:
kubectl create -f manifests/
kubectl describe ingress
kubectl get [service, deployment, ReplicaSet]
kubectl get HorizontalPodAutoscaler

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install my-release ingress-nginx/ingress-nginx

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install prom-release bitnami/kube-prometheus

(Small Note use http://<cluster-ip>:9090 for Prometheus Data Source in Grafana and ID 15760 as dashboard)


I hope this helps, have nice day :)
