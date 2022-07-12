# Monitoring


## Deploy Prometheus

* Crearemos un namespace para desplegar el stack de monitorización
	
	  kubectl create namespace monitoring

* Añadiremos el repositorio de helm prometheus-community para poder desplegar el chart kube-prometheus-stack:

	   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts 
	   helm repo update
	

* Desplegaremos el chart Prometheus-comunity del repositorio de helm añadido en el paso anterior con los valores configurados en el archivo:

	   helm -n monitoring upgrade --install  prometheus prometheus-community/prometheus -f prometheus/custom_values_prometheus.yaml



* Obtenga la URL del servidor Prometheus ejecutando estos comandos en el mismo shell:

	   export POD_NAME=$(kubectl get pods --namespace monitoring -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")

	   kubectl --namespace monitoring port-forward $POD_NAME 9090


 realizado el port-forward podremos acceder a Prometeus a través de http://localhost:9090

## Deploy Grafana

* Añadiremos el repositorio correspondiente a Grafana

	  helm repo add grafana https://grafana.github.io/helm-charts
	  helm repo update

* Instalaremos el chart correspondiente con nuestroos valores correspondientes a través del correspondiente archivo: 

	  helm -n monitoring upgrade --install grafana grafana/grafana -f grafana/values.yaml


* Valores configurables a destacar:

       ingress:
         enabled: true
         annotations:
	   kubernetes.io/ingress.class: nginx
         hosts:
	   - grafana.35-242-211-167.nip.io

* Podemos acceder a Grafana mediante la siguiete URL:
     
	 http://grafana.34-159-59-53.nip.io

* Obtendremos la contraseña àra el usuario 'admin', con el siguiente comando:

	  kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
		
--------------------------------------------------------------------------------------------------

## Deploy Stack de monitorizacion Prometheus & Grafana

1.Crearemos un namespace para desplegar el stack de monitorización
	
	  kubectl create namespace monitoring

2.Añadir el repositorio de helm prometheus-community para poder desplegar el chart kube-prometheus-stack:


	  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	  helm repo update
		
3.Desplegaremos el chart kube-prometheus-stack  con los valores configurados en el archivo custom_values_prometheus.yaml en el namespace monitoring	
	
	  helm -n monitoring upgrade --install prometheus prometheus-community/kube-prometheus-stack -f custom_values_prometheus.yaml  --version 34.1.1

4.Realizaremos un port-forward del servicio de Prometheus al puerto 9090 de la máquina:

	  kubectl -n monitoring port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
	
5.Abriremos una nueva pestaña de la terminal y realizaremos un port-forward del servicio de Grafana al puerto 3000 de la máquina:	
	
	  kubectl -n monitoring port-forward svc/prometheus-grafana 3000:80

6.A continucación puede encontrar tanto el usuario como la contraseña
	
	  Usuario: admin
	  Contraseña: prom-operator


# Autoscalling-Stress




[Volver](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/blob/main/README.md)				

