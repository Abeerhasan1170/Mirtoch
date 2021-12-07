# Mirtorch


### How To Set Up Locally
Install virtualenv
```
pip install virtualenv
```

Create virtual environment
```
virtualenv -p python3 env  && source env/bin/activate
```

Export environment variables
```
export API_KEY=key
export SECRET_KEY=secret
export ACCESS_TOKEN=token
export ACCESS_TOKEN_SECRET=tokensecret
export SECRET_KEY=secret
export EMAIL_HOST="smtp.mail.com"
export EMAIL_PORT="587"
export EMAIL_HOST_USER=emailofsender
export EMAIL_HOST_PASSWORD=apppassword
export CURRENT_URL=localhost:8000/
export DB_USER=user
export DB_PASSWORD=pass
export DB_HOST=localhost
export DB_NAME=mirtoch
export CURRENT_ENV=development
```

Install dependencies
```
pip install -r requirements.txt
```

Load static files 
```
python manage.py collectstatic
```

Run the server
```
python manage.py runserver
```
