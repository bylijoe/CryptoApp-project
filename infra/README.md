## Infraestructura

### Google Kubernetes Engine (GKE)

* Google Kubernetes Engine (GKE) proporciona un entorno administrado para implementar, administrar y escalar las aplicaciones en contenedores mediante la infraestructura de Google. El entorno de GKE consta de varias máquinas (en particular, instancias de Compute Engine) que se agrupan para formar un clúster.

* Los clústeres de GKE funcionan con el sistema de administración de clúster de código abierto de Kubernetes. Kubernetes proporciona los mecanismos a través de los cuales interactúa con el clúster. Puedes usar comandos y recursos de Kubernetes para implementar y administrar las aplicaciones, realizar tareas de administración, establecer políticas y supervisar el estado de las cargas de trabajo implementadas.

* Cuando ejecutas un clúster de GKE, también obtienes los beneficios de las características avanzadas de administración de clústeres que proporciona Google Cloud. Estos son algunos de ellos:
-----------------------------------

### Terraform Kubernetes Engine Module

* Este módulo maneja la creación y configuración de clústeres de Google Cloud Platform Kubernetes Engine con Node Pools, IP MASQ, Network Policy, etc. Los recursos/servicios/activaciones/eliminaciones que este módulo creará/activará son:

   - Crear un clúster de GKE con los complementos provistos
   - Crear grupos de nodos de GKE con la configuración proporcionada y asociarlos al clúster
   - Reemplace el mapa de configuración predeterminado de kube-dns si stub_domainsse proporciona
   - Activar política de red si network_policyes verdadero
   - Agregue ip-masq-agentel mapa de configuración proporcionado non_masquerade_cidrssi configure_ip_masqes verdadero

Puede encontrar la documentación corespondiente en [modulo-GKE](https://registry.terraform.io/modules/terraform-google-modules/kubernetes-engine/google/latest)
 
 ---------------------------------------------------------------------


#### * Puede desplegar la infraestructura localmente siguiendo las siguientes instruciones:

- Inicializamos el directorio de trabajo e instalamos las dependencias:

      terraform init

- Comprobamos que la sintaxis de la configuración es correcta:

      terraform validate

- Creamos un plan de ejecución para alcanzar el estado deseado de nuestra infraestructura:

      terraform plan
      
- Ejecutamos nuestra configuración y procedemos a crear la infraestructura:

      terraform apply
      
- Podremos eliminar los recursos :      

      terraform destroy


Una vez tengamos levantado nuestro cluster nos dirigiremos a la consola de GCP a la sección Kubernetes Engine  y procedemos a conectarnos a nuestro cluster, mediante el siguiente comando:

      gcloud container clusters get-credentials gke-test-1 --region europe-west3 --project natural-chiller-347811

      
##### En la seccion [CICD](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/tree/main/.github) podra encontrar la automatizacion del despliegue de diciha infrestructura la cual se desplegara segun los eventos configurados en el workflow correspondiente **terraform.yaml**      
      
   [Volver](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/blob/main/README.md)
