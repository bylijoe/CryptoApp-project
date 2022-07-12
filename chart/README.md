## Helm
Helm es el administrador de paquetes de Kubernetes .Se utiliza para crear gráficos de Helm , que son paquetes de recursos de Kubernetes que se utilizan para implementar aplicaciones en un clúster.
Puede encontrar información al respecto en [HELM](https://helm.sh/docs/), en caso de no tener instalado Helm ,encontrará un scrip de instalación en el respectivo repositorio del proyecto.


## Instrucciones para desplegar nuestra aplicacion mediante Helm

* Instalacion de la Release de nuestra aplicación :
    
      helm install crypto-app chart/crypto-app
      
* Instalacion del helm chart de mysql pasandole los valores configuarables mecdiante archivo de configuracion

      helm install mysql bitnami/mysql -f k8s/values-mysql.yaml
      
      
Valores configurables a destacar para el helm chart [Mysql]( https://github.com/bitnami/charts/tree/master/bitnami/mysql):

     auth:
        rootPassword: password
        database: movimientos
        username: kc_user
        password: password

    initdbScripts:
      init.sql: |
        CREATE TABLE movimientos (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        date VARCHAR(45) NOT NULL,
        time VARCHAR(45) NOT NULL,
        from_currency VARCHAR(45) NOT NULL,
        from_quantity REAL NOT NULL,
        to_currency VARCHAR(45) NOT NULL,
        to_quantity REAL NOT NULL,
        PRIMARY KEY (id)); 
        INSERT INTO movimientos VALUES (1,'2022-10-15','20:00','EUR',7.26, 'BTC', 1.0);
        INSERT INTO movimientos VALUES (2,'2022-10-15','20:00','EUR',7.26, 'BTC', 1.0);
    
    metrics:
      enabled: true     


[Volver](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/blob/main/README.md)

[Monitoring](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/tree/main/monitoring)
