# Cleandev Api Template

El objetivo es facilitar la creación de APIS con flask de una forma sencilla, para ellos se ha creado un wrapper
que añade las librerias `Flask-Cors` y `Flask-RESTful` y las preconfigura para que solo tengas que dedicar tiempo
en programar tu API.

# Diagrama
![diagrama](https://gitlab.com/cleansoftware/libs/public/cleandev-api-template/-/raw/master/docs/diagrama.png)


## ApiFactory

No hay mucho que decir en este punto, ya que solo hay que configurar algunos parámetros en el archivo de configuración
y pedirle a la factoría que nos cree una instancia de una `app` de Flask y ya esta, como se muestra en el siguiente
ejemplo.

```python
from flask import Flask
from api_template import ApiFactory
from api_template.config import _debug
from werkzeug.serving import run_simple

app_factory: ApiFactory = ApiFactory()
app: Flask = app_factory.app

if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_debugger=_debug, use_reloader=True)
```

Para crear los recursos del API se sigue los mismos pasos que para `Flask-RESTful` con una pequeña variante, y es que 
deberemos configurar como se mostrara a continuación un paquete donde iran dichos recursos y cada clase que representa
un recurso debe implementar un metodo que retornara una lista que contendrá la dirección del endpoint que se quiera 
agregar de forma automatica en lugar del tradicional `api.add_resource(HelloWorld, '/')` como pone en la documentación.

## Agregando recursos

A continuacion veremos la forma de añadir un recurso a nuestra API.

```python
import json
from flask_restful import Resource
from flask import request, Response
from flask_jwt_extended import create_access_token


class Login(Resource):

    def get(self):
        data: dict = {'message': 'OK', 'data': create_access_token(identity='test@mail.com')}
        return Response(json.dumps(data), status=200, mimetype='application/json')

    def post(self):
        # Example login
        email = request.json.get('email')
        password = request.json.get('password')

        if email == 'test@mail.com' and password == 'test':
            data: dict = {'message': 'OK', 'data': create_access_token(identity=email)}
            return Response(json.dumps(data), status=200, mimetype='application/json')
        else:
            data: dict = {'message': 'User not found', 'data': {}}
            return Response(json.dumps(data), status=404, mimetype='application/json')

    @staticmethod  # Este metodo agrega automaticamente el endpoint al API
    def endpoint() -> list:
        return ['/login']
```
#### Config

Para que esto funcione correctamente deberemos indicarle en el archivo de configuración el nombre del paquete donde se 
encuentran los recursos, puedes ponerlos en un unico fichero o en multiples ficheros dentro del mismo paquete para que
puedas organizarlo de la forma que desees

```properties
[API_TEMPLATE]
path_resources_api = resources
```