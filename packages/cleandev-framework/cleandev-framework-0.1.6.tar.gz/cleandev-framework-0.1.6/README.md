# Cleandev Framework

Esta librería ofrece la posibilidad de transformar modelos en dto y dto en modelos de una forma fácil, esto lleva
acoplado una reglas a la hora de nombrar las clases que representan los dto con respecto a los modelos de base de datos
a cambio ofrece un código muchísimo más compacto y escalable

# Diagrama
![diagrama](https://gitlab.com/cleansoftware/libs/public/cleandev-framework/-/raw/master/docs/diagrama.png)

## Clases

Principalmente existen dos clases `ModelAdapter` y `DataClassAdapter`  
`DataClassAdapter` se encarga de convertir modelos en clases de datos  
`ModelAdapter` se encarga de convertir clases de datos en modelos  

Para que la magia suceda debe existir una relacion de nombres entre los nombres de las clases que representan los modelos
de base de datos y las clases que representan la clase de datos o "dataclass", por ejemplo:

Si tenemos un modelo de base de datos llamado `User` la clase de datos que representa ese modelo debera llamarse
`_UserDataClass` de este modo la librera es capaz de transformar entre tipos de modelos y tipo de clase de datos.

Tiene una pinta similar a esta:

```python
from typing import Optional
from dataclasses import field
from sqlalchemy import String
from sqlalchemy import Column
from postgresql_db import Base
from dataclasses import dataclass
from cleandev_validator import DataClass
from postgresql_db.inmutables import _Params
from cleandev_validator import _DataClassConstrains


class User(Base):
    __tablename__ = 'user'

    uuid = Column(String, primary_key=True)
    username = Column(String)
    email = Column(String)
    lastname = Column(String)

    def __init__(self, **kwargs):
        self.uuid = kwargs.get(_Params.UUID)
        self.username = kwargs.get(_Params.USERNAME)
        self.email = kwargs.get(_Params.EMAIL)
        self.lastname = kwargs.get(_Params.LASTNAME)


@dataclass()
class _UserDataClass(DataClass):
    uuid: str
    username: str
    email: str
    lastname: Optional[str] = field(default=None)

    def __post_init__(self):
        super(_UserDataClass, self)._validate(**self.__dict__)

    @property
    def __constrains__(self):
        return {
            'uuid': str(_DataClassConstrains.STR),
            'username': str(_DataClassConstrains.STR),
            'email': str(_DataClassConstrains.STR),
            'lastname': str(_DataClassConstrains.STR)
        }

```


### DataClassAdapter

Posee dos metodos para el usuario final `model_to_dataclass` y `list_models_to_list_dict`
`model_to_dataclass` Dado un modelo lo convierte a su correspondiente clase de datos  
`list_models_to_list_dict` Dado una lista de modelos retorna una lista de variables tipo `dict` con los valores de las 
clases de datos, en el caso que desearas una instancia de la clase de datos bastaria con pasarle el diccionario en el 
constructor poniendo `**` delante del diccionario


#### model_to_dataclass()

Dado un modelo lo convierte a su correspondiente clase de datos

```python
from models import User
from models import _UserDataClass
from cleandev_framework import DataClassAdapter

if __name__ == '__main__':
    user: User = User(
        uuid='0548604f-4990-482b-977a-7c4164c816a9',
        username='Daniel',
        email='daniel@mail.com',
        lastname='Rodriguez'
    )

    user_data_class: _UserDataClass = DataClassAdapter.model_to_dataclass(user)
    user_data_class.__fields__  # ['uuid', 'username', 'email', 'lastname']
    user_data_class.__filter__(['username', 'email'])  # {'username': 'Daniel', 'email': 'daniel@mail.com'}
    user_data_class.__dict__
    # {'uuid': '0548604f-4990-482b-977a-7c4164c816a9', 'username': 'Daniel', 'email': 'daniel@mail.com', 'lastname': 'Rodriguez'}

```

#### list_models_to_list_dict()

Dado una lista de modelos retorna una lista de variables tipo `dict` con los valores de las 
clases de datos, en el caso que desearas una instancia de la clase de datos bastaria con pasarle el diccionario en el 
constructor poniendo `**` delante del diccionario

```python
import json

from cleandev_framework import DataClassAdapter
from models import User

if __name__ == '__main__':

    user: User = User(
        uuid='0548604f-4990-482b-977a-7c4164c816a9',
        username='Daniel',
        email='daniel@mail.com',
        lastname='Rodriguez'

    )

    # Supongamos que son usuario diferetes =)
    list_users: list = [user, user, user]
    list_dict: dict = DataClassAdapter.list_models_to_list_dict(list_users)

    print(json.dumps(list_dict, indent=4))

    [
        {
            "uuid": "0548604f-4990-482b-977a-7c4164c816a9",
            "username": "Daniel",
            "email": "daniel@mail.com",
            "lastname": "Rodriguez"
        },
        {
            "uuid": "0548604f-4990-482b-977a-7c4164c816a9",
            "username": "Daniel",
            "email": "daniel@mail.com",
            "lastname": "Rodriguez"
        },
        {
            "uuid": "0548604f-4990-482b-977a-7c4164c816a9",
            "username": "Daniel",
            "email": "daniel@mail.com",
            "lastname": "Rodriguez"
        }
    ]
```

### ModelAdapter

Se encarga de convertir clases de datos en modelos


#### dataclass_to_model()

```python
from models import User
from models import _UserDataClass
from cleandev_framework import DataClassAdapter

if __name__ == '__main__':
    user: User = User(
        uuid='0548604f-4990-482b-977a-7c4164c816a9',
        username='Daniel',
        email='daniel@mail.com',
        lastname='Rodriguez'
    )

    user_data_class: _UserDataClass = DataClassAdapter.model_to_dataclass(user)
    user_data_class.__fields__  # ['uuid', 'username', 'email', 'lastname']
    user_data_class.__filter__(['username', 'email'])  # {'username': 'Daniel', 'email': 'daniel@mail.com'}
    user_data_class.__dict__
    # {'uuid': '0548604f-4990-482b-977a-7c4164c816a9', 'username': 'Daniel', 'email': 'daniel@mail.com', 'lastname': 'Rodriguez'}

```