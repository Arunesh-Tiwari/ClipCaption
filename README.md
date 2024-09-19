# ClipCaption

## Django Project Setup Guide

This guide will help you set up and run the Django project locally on your Windows machine. The project uses PostgreSQL 14 for the database and requires ffmpeg to be installed.

## Prerequisites

1. **Python**: Ensure you have Python 3.8 or later installed on your machine.
2. **PostgreSQL 14**: Install PostgreSQL 14 and set it up on your machine.
3. **ffmpeg**: Install ffmpeg. Follow [this guide](https://www.ffmpeg.org/download.html) to install it on Windows.
4. **pip**: Ensure you have pip installed for managing Python packages.

## ffmpeg Installation

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
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5433', #Use your default port it may be 5432 on your machine
    }
}
   ```

## Install Project Dependencies

```bash
pip install -r requirements.txt
```

Ensure the `requirements.txt` file includes the following dependencies:

```
Django>=4.2,<5.0
psycopg2-binary
ffmpeg-python>=0.2.0
```

## Set Up Environment Variables

Create a `.env` file in the project root directory and add any necessary environment variables. For example:

```
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password

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

Visit `http://127.0.0.1:8000/upload` in your web browser to view the project.

## Troubleshooting

- **Database Connection Issues**: Double-check the database credentials in `settings.py`.
- **ffmpeg Not Found**: Ensure ffmpeg is installed and its path is added to the system PATH.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
