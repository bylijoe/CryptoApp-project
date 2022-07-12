## Kubernetes

 Es un sistema de código libre para la automatización del despliegue, ajuste de escala y manejo de aplicaciones en contenedores que fue originalmente diseñado por Google y donado a la Cloud Native Computing Foundation (parte de la Linux Foundation). Soporta diferentes entornos para la ejecución de contenedores, incluido Docker. Puede encontrara la documentacion al respecto en [Kubernetes](https://kubernetes.io/docs/home)
 
 Nos proporciona todo lo necesario para mantener en producción nuestros framework:

- Montaje de volumenes para su persistencia (Soporta multiples soluciones).
- Distribución de secretos y gestor de la configuración.
- Gestión de la vida del contenedor.
- Replicación de contenedores.
- Uso de autoscalado horizontal.
- Service Discovery y balanceo de tus framework.
- Monitorización.
- Acceso a los logs y debug de tus framework.



### Instrucciones para el despliegue:

Una vez desplegada nuestra infraestructura a modo de cluster en GKE , el cual podemos encontrar en [CLUSTER](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/tree/main/infra)
 tendremos que instalar un [ingress-controller](https://kubernetes.github.io/ingress-nginx/deploy/), que nos permitirá exponer  tanto nuestra aplicación como posteriormente Grafana al exterior.Para ello realizaremos los siguientes pasos:
 
 * Habilitaremos los permisos en el cluster, mediante el siguiente comando:
    
       kubectl create clusterrolebinding cluster-admin-binding \
          --clusterrole cluster-admin \
          --user $(gcloud config get-value account)   
                
 * Posteriormente,instalaremos Ingress controller en nuestro cluster:
 
       kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.0/deploy/static/provider/cloud/deploy.yaml
       
       
       
Una vez desplegado el Cluster e instalado  nuestro ingress podremos proceder a lanzar nuestra aplicacion :

* Despliegue de forma conjunta mediante el siguiente comando, situandose en el directoroio principal del proyecto:

      kubectl apply -f k8s

Objetos a desplegar en nuestra aplicacion(documentación al respecto):
* [Configmaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
* [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
* [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* [Persistent Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [Services](https://kubernetes.io/es/docs/concepts/services-networking/service/)

 
[Volver](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/blob/main/README.md)
