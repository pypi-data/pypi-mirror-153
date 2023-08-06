# Broker Clients

Package to handle broker clients in Apophenia project

Install package in local
~~~
rm -rf dist 
python setup.py sdist
pip install ../broker_clients/
~~~
Upload package to PyPi
~~~
twine upload dist/*
~~~
Update
~~~
twine upload --skip-existing dist/* 
~~~
Install package from github
~~~
pip install git+https://github.com/OswaldoCuzSimon/broker_clients.git
~~~

Install from pypi
~~~
pip install broker-clients
~~~

~~~
alembic -c broker_clients/alembic.ini revision --autogenerate -m "Add column account_balance to Trades"
alembic -c broker_clients/alembic.ini upgrade head
~~~