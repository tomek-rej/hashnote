run: 
	python manage.py runserver

test:
	python manage.py test

setup:
	pip install -r requirements.txt
	python manage.py syncdb
