install: bin/python

bin/python:
	virtualenv -p /usr/bin/python3 .
	bin/pip install -r requirements.txt

migrate: bin/python
	bin/python teknologr/manage.py migrate

serve: bin/python
	bin/python teknologr/manage.py runserver 8888

deploy: bin/python
	bin/python teknologr/manage.py collectstatic --clear --noinput
	touch teknologr/teknologr/wsgi.py

clean:
	rm -rf bin/ lib/ build/ dist/ *.egg-info/ include/ local/
