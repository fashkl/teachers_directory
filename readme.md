Hello Digital&Code !  

App can do the following:  
- Add subject individually from admin panel or directly for logged-in user
- Add teachers individually from admin panel or directly for logged-in user
- Import teachers ***in bulk*** using CSV files for logged-in user only
- Filter teachers by subjects they teach, or/and by first character of last name

### Requirements
- Python > 3.7 
- Docker

### Quickstart
- Run `pip install -r requirements.txt`
- Run `python manage.py runserver 8000`
- open ***http://localhost:8000***

### Running through Docker
- Navigate to docker file directory
- Run `docker build . -t tech-task-td` to build docker image
- Run `docker run  -p 8000:8000 tech-task-td` to run the application 
- open ***http://localhost:8000/***

