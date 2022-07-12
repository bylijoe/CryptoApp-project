## Docker

Docker es un proyecto de código abierto que automatiza el despliegue de aplicaciones dentro de contenedores de software, proporcionando una capa adicional de abstracción y automatización de virtualización de aplicaciones en múltiples sistemas operativos.Docker utiliza características de aislamiento de recursos del kernel Linux, tales como cgroups y espacios de nombres (namespaces) para permitir que "contenedores" independientes se ejecuten dentro de una sola instancia de Linux, evitando la sobrecarga de iniciar y mantener máquinas virtuales

Podra encontrar la documentacion al respector en el siguiente enlace [Docker](https://docs.docker.com/get-started/overview/)


## Dockerfile

Mediante el ficherto Dockerfile **Multi-stage** podremos crear la imagen docker de nuestra aplicacion que utilizaremos en las distintas secciones de nuestro proyecto:

        FROM python:3.8.11-alpine3.14 as base

        FROM base AS dependencias 

        WORKDIR /install

        RUN apk add --no-cache gcc musl-dev linux-headers
        COPY src/requirements.txt .
        RUN pip install --prefix=/install -r requirements.txt


        FROM base

        COPY --from=dependencias /install  /usr/local

        WORKDIR /app
        COPY src .

        ENV FLASK_APP=run
        ENV FLASK_RUN_HOST=0.0.0.0
        ENV FLASK_ENV=development
        ENV MYSQL_HOST=mysql-server
        ENV MYSQL_PORT=3306
        ENV MYSQL_USER=kc_user
        ENV MYSQL_PASSWORD=password
        ENV MYSQL_DATABASE=movimientos

        EXPOSE 5000

        CMD ["flask", "run"]


* Crearemos nuestra imagen y la subiremos al correspondiente repositorio [Docker hub](https://hub.docker.com/repository/docker/leosn/crypto_app), para ello situese en el directorio principal del proyecto y ejecute los siguientes comandos:

        docker build -t <username>/crypto-app:0.0.1 -f ./Docker/Dockerfile .
        
        docker push  <username>/crypto-app:0.0.1 
 

Podremos contruir nuestro servicios de forma individual , para ello deberemos crear un a red para conectar tanto la app como nuestro servicio para [mysql](https://hub.docker.com/_/mysql).
situese en el directorio principal y ejecute los siguientes comandos:

 * Crearemos una networ "network-cryp":
 
        docker network create network-cryp
 
 * Ejecutaremos el contenedor correspondiente al servicio mysql:
          
        docker run -e MYSQL_ROOT_PASSWORD=password -e MYSQL_HOST=mysql-server -e MYSQL_USER=kc_user -e MYSQL_DATABASE=movimientos  -e MYSQL_PASSWORD=password --network network-cryp mysql:5.7

        
 * Ejecutaremos el contenedor correspondiente a nuestra app el cual escuchara por el puerto 5000:
        
       docker run -it --rm -p 5000:5000 --network network-cryp crypto-app:0.0.1

        
 
### Docker-compose

Docker Compose es una herramienta que nos permite definir y orquestar de forma local varios contenedores  los cuales estaran unidos por una network.
               
               version: "3.9"
                services:
                  app:
                    build: .
                    ports:
                    - 5000:5000
                    links:
                    - mysql-server
                    restart: always
                  mysql-server:
                    image: mysql:5.7
                    restart: always
                    environment:
                    - MYSQL_ROOT_PASSWORD=password
                    - MYSQL_USER=kc_user
                    - MYSQL_PASSWORD=password
                    - MYSQL_DATABASE=movimientos
                    ports:
                    - 32000:3306
                    volumes:
                    - /my-db:/var/lib/mysql
                    - "./docker/mysql/conf.d:/etc/mysql/conf.d"
                volumes:
                  my-db:     
        

Una vez que tenga un archivo Compose, puede crear e iniciar los distintos servicios si no se indica una network creara una network por defecto la cual permitira la comunicación entre ambos servicios. para ello ejecute el siguientes comandos :

* Ejecutamos la App la cual contiene dos sevicios:

            docker-compose up
            
* Detendremos lo contenedores y eliminaremos contenedores,redes,volumenes e imagenes creadas por **up**, con el siguiente comando:

            docker-compose down

               



  
[Volver](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/blob/main/README.md)
