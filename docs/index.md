# Tweet API project

This is a test project API for collecting Twitter data.

# Local Development

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Execute Django's migration command:**
```bash
python manage.py migrate
```
**Note:**
- Currently using SQLite3 database for test development purposes.

**If you want to create your superuser account in admin:**
```bash
python manage.py createsupueruser
```

**Run local server**
```bash
python manage.py runserver
```

# Twitter API endpoints
**Getting tweets by hashtag using curl:**
```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:8000/hashtags/Python/?limit=1
```

**Getting tweets by hashtag using Browseable API:**
```bash
http://localhost:8000/hashtags/Python/?limit=1
```

**Getting user tweets using curl:**
```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:8000/users/twitter/?limit=1
```

**Getting tweets by hashtag using Browseable API:**
```bash
http://localhost:8000/users/twitter/?limit=1
```

**Note:**
- Appending trailing slash is necessary since it is enabled in the configuration.

# API Documentation

**For more information on using the endpoints and create sample test requests:**
```bash
http://localhost:8000/docs/
```
