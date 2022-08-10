# An Flask REST API to manage the applicants
## Techstack
- Flask RESTful
- SQLAlchemy
- PostgreSQL
- Docker
- docker-compose
## Config
- Clone this repository
- Add `.env` file to config 
```
# Example
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:password**@localhost:5432/applicant_manage
SENTRY_DSN=https://b7eec1c2f1e64f3e8e2c01eb6caac83c:09892e1463df44a589d876857ba03fab@sentry.vn/123
API_URL=http://localhost:5000
```
## Migrate database
- Create virtualenv
```
python3 -m venv venv
source venv/bin/activate
```
- Install pakage from requirements.txt
```
pip install -r requirements.txt
```
- Migrate database: (Postgresql must installed extension uuid-ossp)
```
python3 manager.py upgrade
```
## Deployment
- Docker and docker-compose must be required
- Run comands:
```
docker-compose build
docker-compose up -d
```
## API docs
- Api docs could be seen at endpoint :`API_URL/apidocs`

## Run the script to stimulate 1000 API requests
- The script is located at: `workers/stimulate_script.py`
- Config `API_URL` in `.env` to choose testing endpoint
- Run script:
```
python3 manager.py runtask stimulate_script
```

# Server test
### API_URL
`http://103.107.182.123:5000`

