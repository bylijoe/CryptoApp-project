# Crypto App

Aplicación web en Flask " Simulador de conversión e inversión en Criptomonedas "

## Requerimientos 

* [Python](https://www.python.org/) - Programming language
* [Flask](https://flask.palletsprojects.com/en/2.1.x/) - Web develoment
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/) - Form library
* [Pico CSS](https://picocss.com/) - MiniFramework CSS
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) - Web template engine
* [MySql](https://www.mysql.com/) - Database engine
* [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
* [Pytest](https://docs.pytest.org/en/7.1.x/)- Test library



## Instrucciones de instalación 

* **Instalar el entorno virtual**
```
python -m venv env
```

* **Activar entorno virtual**
```
source env/bin/activate
```

* **Instalar "requirements":**
```
pip install -r src/requirements.txt
```

* **Modificar variable de entorno**

Modificamos la variable de entorno **FLASK_APP** con el valor **run**

* **Vincular API**

Visitar la web de Coinapi para solicitar una APIKEY:
```
https://www.coinapi.io/pricing?apikey
```
Introducir su APIKEY en el archivo **config_ejemplo.py**

Renombrar **config_ejemplo.py** por **config.py**

* **Lanzar aplicación**
```
flask run
```


[Volver](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/blob/main/README.md)


