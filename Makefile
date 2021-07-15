migrate:
	python3 manage.py makemigrations && python3 manage.py migrate

run:
	python3 manage.py runserver

shell:
	python3 manage.py shell

freeze:
	pip freeze > requirements.txt
