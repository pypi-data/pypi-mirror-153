# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlmodel_basecrud']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.35',
 'importlib-metadata>=4.11.4,<5.0.0',
 'sqlmodel>=0.0.6,<0.0.7']

setup_kwargs = {
    'name': 'sqlmodel-basecrud',
    'version': '0.1.9',
    'description': 'Simple package that provides base CRUD operations for your models.',
    'long_description': '## SQLModel BaseCRUD\n\n[![codecov](https://codecov.io/gh/woofz/sqlmodel-basecrud/branch/main/graph/badge.svg?token=AZW7YBAJBP)](https://codecov.io/gh/woofz/sqlmodel-basecrud) [![PyPI version](https://badge.fury.io/py/sqlmodel-basecrud.svg)](https://badge.fury.io/py/sqlmodel-basecrud) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sqlmodel-basecrud) [![Downloads](https://static.pepy.tech/personalized-badge/sqlmodel-basecrud?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/sqlmodel-basecrud)\n\n\n_Simple package that provides base CRUD operations for your models._\n\n---\n\n_**Documentation:**_ [https://woofz.github.io/sqlmodel-basecrud/latest](https://woofz.github.io/sqlmodel-basecrud/latest)\n\n_**Sources:**_ [https://github.com/woofz/sqlmodel-basecrud](https://github.com/woofz/sqlmodel-basecrud)\n\n---\n\n### What is SQLModel BaseCRUD?\n\nWith SQLModel BaseCRUD, you can implement your CRUD operations easily in your project. It is simple as declaring a variable!  \nThis package consists in two classes: _BaseCRUD_ and _BaseRepository_.  \n**BaseCRUD** is the basic class that implements the basic CRUD operations, while **BaseRepository** is the repository used to execute those operations. You could also write your own repository class and use basic CRUD operation provided by **BaseRepository** class by extending it to your own repository class!\n\n### Installation\n\n##### Using pip\n\n`pip install sqlmodel-basecrud`\n\n##### Using poetry\n\n`poetry add sqlmodel-basecrud`\n\n### Operations\n\n### Usage\n\n##### Basic setup\n\nConsider these two models as example:\n\n```python\nclass Team(SQLModel, table=True):\n    id: Optional[int] = Field(default=None, primary_key=True)\n    name: str = Field(index=True)\n    headquarters: str\n\n    heroes: List["Hero"] = Relationship(back_populates="team")\n    \n    \nclass Hero(SQLModel, table=True):\n    id: Optional[int] = Field(default=None, primary_key=True)\n    name: str = Field(index=True)\n    secret_name: str\n    age: Optional[int] = Field(default=None, index=True)\n\n    team_id: Optional[int] = Field(default=None, foreign_key="team.id")\n    team: Optional[Team] = Relationship(back_populates="heroes")\n```\n\nWe want to perform some operations on these models. First of all we instantiate a _BaseRepository_, specifying the database session and the model that we want to manipulate.\n\n```python\n# other imports..\nfrom sqlmodel_basecrud import BaseRepository\n\nwith Session(engine) as session:\n    hero_repository = BaseRepository(db=session, model=Hero)\n    team_repository = BaseRepository(db=session, model=Team)\n```\n\n##### CREATE operation\n\nPersists an item into the database.\n\n```python\n# CREATE operation\nmy_hero = Hero(name=\'Github Hero\', secret_name=\'Gitty\', age=31)\nhero_repository.create(my_hero)\n# now my_hero is persisting in the database!\n```\n\n##### GET operation\n\nGET operation simply gets a single record from the database.\n\n```python\nresult = hero_repository.get(id=1, name=\'Github Hero\')\n```\n\n_result_ variable will be an instance of Hero, if a result matches the criteria, or None type.\n\n##### FILTER operation\n\nGets one or more instances from the database, filtering them by one or more column/s.\n\n```python\nresults = hero_repository.filter(age=31)\n```\n\n_results_ will be a _List_ with zero or more elements.\n\n##### GET ALL operation\n\nGets all instances of given module from the Database\n\n```python\nresults = hero_repository.get_all()\n```\n\n_results_ will be a _List_ with zero or more elements.\n\n##### UPDATE operation\n\nUpdates a record into the database.\n\n```python\ninstance_to_update = hero_repository.get(id=1)\ninstance_to_update.name = \'Super New Name\'\ninstance_to_update.age = 27\n\nhero_repository.update(instance_to_update)\n```\n\nThe hero will have his columns \\*name \\*and _age_ with updated values.\n\n##### DELETE operation\n\nRemoves an instance from the database\n\n```python\ninstance_to_remove = hero_repository.get(id=1)\nhero_repository.delete(instance_to_remove)\n```\n\nThe instance will be removed from the database.\n\n### Custom Repository\n\nIf you want to extend the BaseRepository class with some custom methods, you can write your own repository class. Just extend BaseRepository or BaseCRUD class and call the super class constructor, by passing it two essential parameters:\n\n*   **db**: must be a Session instance;\n*   **model**: must be a Type\\[SQLModel\\].\n\n```python\nfrom sqlmodel_basecrud import BaseRepository\n\n\nclass MyCustomRepository(BaseRepository):\n\n    def __init__(self, db: Session, model: Type[SQLModel]):\n        super().__init__(model=model, db=db)\n```\n\n### What\'s next\n\nThe first thing that comes to my mind is to extend the features of Async to BaseCRUD class. I will try to enhance the features of the project. Suggestions are appreciated 🤩\n\n### Inspired by\n\n_FastAPI_: framework, high performance, easy to learn, fast to code, ready for production\n\n_SQLModel_, SQL databases in Python, designed for simplicity, compatibility, and robustness.\n',
    'author': 'Danilo Aliberti',
    'author_email': 'danilo@woofz.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/woofz/sqlmodel-basecrud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
