## ClipCaption
### Video Demostration of working project ⬇️
[Video Demonstration.webm](https://github.com/user-attachments/assets/360e340d-b947-4416-aa47-0697e521091c)

### You can either use docker or below guide to setup project in your machine.

## Project Setup Using Docker
```bash
cd your-folder
git clone https://github.com/Arunesh-Tiwari/ClipCaption.git
```
Navigate to root directory and run.
```bash
docker-compose up --build
```
### It may happen after running docker compose command migrations not happen and error is caused. To resolve this rerun below command.
```bash
docker-compose up --build
```
Visit `http://127.0.0.1:8000/upload` in your web browser to view the project.

## Django Project Setup Guide

This guide will help you set up and run the Django project locally on your Windows machine. The project uses PostgreSQL 14 for the database and requires ffmpeg to be installed.

## Prerequisites

1. **Python**: Ensure you have Python 3.8 or later installed on your machine.
2. **PostgreSQL 14**: Install PostgreSQL 14 and set it up on your machine.
3. **ffmpeg**: Install ffmpeg. Follow [this guide](https://www.ffmpeg.org/download.html) to install it on Windows.
4. **pip**: Ensure you have pip installed for managing Python packages.

## Check ffmpeg Installation

Ensure ffmpeg is installed and added to your system PATH. You can verify the installation by running:

```bash
ffmpeg -version
```

## Clone the Repository
create a your-folder
```bash
cd your-folder
git clone https://github.com/Arunesh-Tiwari/ClipCaption.git
cd videoprocessor
```
## Set Up Virtual Environment
Create and activate a virtual environment to manage project dependencies:

```bash
python -m venv venv
venv\Scripts\activate
```

## Setup PostgreSQL Database

1. **Create a Database**:
   - Open `pgAdmin` or use `psql` to create a new database.
   - Create a new user and assign it to the database.

2. **Update `settings.py`**:
   - Open `your_project/settings.py` and update the `DATABASES` setting with your PostgreSQL database credentials.

   ```python
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
   }
   ```

## Install Project Dependencies

```bash
pip install -r requirements.txt
```

Ensure the `requirements.txt` file includes the following dependencies:

```
asgiref==3.8.1
Django==4.2.16
ffmpeg-python==0.2.0
future==1.0.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
sqlparse==0.5.1
typing_extensions==4.12.2

```

## Set Up Environment Variables

Create a `.env` file in the project root directory and add any necessary environment variables. For example:

```
POSTGRES_DB=your-db-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password

```

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the Development Server

```bash
python manage.py runserver
```

### ⚠️ **Note:** After setup visit `http://127.0.0.1:8000/upload` in your web browser to view the project.

## Troubleshooting

- **Database Connection Issues**: Double-check the database credentials in `settings.py`.
- **ffmpeg Not Found**: Ensure ffmpeg is installed and its path is added to the system PATH.
- **Connection Error During Migrate `docker-compose up --build`**: Rerun `docker-compose up --build` or `docker-compose up`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
