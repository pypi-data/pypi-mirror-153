# EZTea Web Framework

```bash
# use falcon
pip install eztea[falcon,mysql,migration,testing]

# use django
pip install eztea[django,postgresql,testing]
```

## Usage

### Falcon Example

```python
from validr import T

from eztea.falcon import Application, ResponderContext, Router

router = Router()


@router.get("/")
def hello(
    ctx: ResponderContext,
    name: str = T.str.default("world"),
) -> T.dict(hello=T.str):
    return {"hello": name}


app = Application()
app.include_router(router)
```

### Django Example

```python
from validr import T

from django.http import HttpRequest
from eztea.django import Router

router = Router()


@router.get("/")
def hello(
    req: HttpRequest,
    name: str = T.str.default("world"),
) -> T.dict(hello=T.str):
    return {"hello": name}


urls = router.to_url_s()
```

### Testing Example

```python
from eztea.falcon.testing import WebTestClient
from eztea.django.testing import WebTestClient
from myapp.wsgi import application

def test_hello():
    client = WebTestClient(application)
    response = client.get('/')
    assert response.status_code == 200
    assert reesponse.json() == {"hello": "world"}
```
