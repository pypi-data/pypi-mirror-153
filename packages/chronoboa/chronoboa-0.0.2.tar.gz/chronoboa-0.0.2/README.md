<h2>Codigo Facilito</h1>

Este paquete nos permite consumir el API de la plataforma.


<h2>Pasos para crear y subir el paquete en pypi</h2>

Creamos una variable de tipo string que contiene la url de nuestra pypi.

```sh
python3 setup.py sdist
```

Instalamos el paquete twine en nuestro sistema, para autenticarnos en pypi.

```sh
pip install twine
```

Publicamos nuestro paquete en pypi.

```sh
twine upload dist/* 
```