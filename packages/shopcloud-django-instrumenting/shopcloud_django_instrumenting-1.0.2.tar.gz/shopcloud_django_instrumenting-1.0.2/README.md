# Instrumenting

## install

```sh
$ pip install shopcloud-django-instrumenting
```

## usage

```py
from shopcloud_django_instrumenting import tracing

tr = tracing.Tracer('name_of_service', 'name_of_operation')
with tr.start_span('event.processing') as span:
    pass

data = tr.close()
```

## deploy

```sh
$ pip3 install wheel twine
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/* 
```