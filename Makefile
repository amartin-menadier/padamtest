run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Migrate code changes
	python manage.py makemigrations
	python manage.py migrate

clean: 
	python manage.py flush

user:
	python manage.py createsuperuser

data:
	python manage.py create_data