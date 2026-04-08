# Database website for the Olbers Planetarium Bremen

A flask based application for internal management of the planetarium's team.

## Prerequisites

A server machine installed with:
- Python (> 3)
- pip ready (python -m ensurepip --upgrade)
- a Web Server Gateway Interface (WSGI) ready, like Gunicorn (pip install gunicorn)
- a web server ready, like nginx
- a database software ready, like MariaDB

## Setup

1. Clone this repository and create a virtual environment
2. Create a directory for uploads
3. Create a database for the application, ensure a user with full access rights exists
4. Create an .env file and configure the application
5. Run the shell to test everything works fine
6. Initiate the database
7. Create an admin user
8. Setup your server software and wsgi
9. Run the application
10. Navigate to the verification page to set a password for the admin user

### Cloning

### Upload directory

### Database creation

### Configuration

Create a .env file in the main directory of the cloned project. Open with a text editor and fill in the environment variables used by dotenv.
You can see the default values, if any, in the [config.py](config.py) file. Do setup all of the following variables. Otherwise the proper functioning of the application is not guaranteed:

| Variable | Description | Default value |
| --- | --- | --- |
| APP_NAME | A name for the application / website title. | Olbers Planetarium |
| SECRET_KEY | Flask's secret key it uses to sign session cookies and other security related tasks.[^1] | c54ec5889e42b654e72263365d299a8f001bf2e91c0f0fdc244117ca14b6340a |
| DATABASE_URL | URL to the database, including login information.[^2] | sqlite:///path/to/application/app.db |
| MAIL_SERVER | URL to a smtp mail server | None |
| MAIL_DEFAULT_SENDER | The default sender of the system mails. | None |
| MAIL_PORT | The port to connect on to the mail server. | None |
| MAIL_USE_TLS | True or False. Use TLS to connect to the mail server. | False |
| MAIL_USE_SSL | True or False. Use SSL to connect to the mail server. | False |
| MAIL_USERNAME | The username to log in on the mail server. | None |
| MAIL_PASSWORD | The password to log in on the mail server. | None |
| MAIL_DEBUG | True or False. Print debug information when sending emails. | False |
| AUTH_TOKEN_VALIDITY | Time in milliseconds a generated URL token for new users will be valid. | 432000 (5 days) |

[^1]: DO NOT, ABSOLUTELY DO NOT use the default key in an online environment. Generate a key and do not publish it anywhere. See [this stackoverflow answer](https://stackoverflow.com/a/54433731) to learn how to generate a key.
[^2]: It is not recommended to use the default sqlite database for a production environment.

### Shell

Within the main directory, run the following command:
```
flask shell
exit()
```
This will start and stop the flask shell interface. If everything runs without errors, the installation was successful so far.

### Database initialisation

Within the main directory, run the following command:
```
flask db upgrade
```
This will create all the tables within the database. If everything runs without errors, the database was configured correctly.

### Admin user

To create a new, first user, start the flask shell by entering the command "flask shell" again in the main directory. Then run the following commands within flask shell:
```
import pyotp
user=User(username='USERNAME', email='EMAIL@DOMAIN.DE', token_2fa=pyotp.random_base32())
db.session.add(user)
db.session.commit()
db.session.refresh(user)
rights=Right(user_id=user.id, admin=True)
db.session.add(rights)
db.session.commit()
from app.email.mail_utils import generate_token
token=generate_token('EMAIL@DOMAIN.DE', 'SECRET_KEY', 'email-registration')
print(token)
exit()
```
This creates a new user in the database, populating the basic fields and giving the account full admin privileges.
Replace USERNAME with a username of your choosing. Replace EMAIL@DOMAIN.DE with an email address, preferably a real one. Replace SECRET_KEY with your configured secret key.
Copy the printed token from the command line. You will need this in the [First login](#first-login) step.
Take into consideration that the generated token will only be valid within your configured AUTH_TOKEN_VALIDITY time.

### Server software, WSGI

### Running

### First login

To set a password for the created admin user, navigate to your now running webpage in the following way:

https://application.domain/verify?token=TOKEN

Replace TOKEN with the generated token from the [Admin user](#admin-user) step. Setup a password for the new user and possibly two factor authentication (recommand at least for all users with admin privileges).