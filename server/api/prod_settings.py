import os
from dotenv import load_dotenv
from .settings import *

load_dotenv()

DEBUG = False

allowed_hosts_env = os.getenv("ALLOWED_HOSTS")

if not allowed_hosts_env:
    raise Exception("ALLOWED_HOSTS not found or empty")

ALLOWED_HOSTS = list(map(lambda host: host.strip(), allowed_hosts_env.split(",")))

secret_key_env = os.getenv("SECRET_KEY")

if not secret_key_env:
    raise Exception("SECRET_KEY not found or empty")

SECRET_KEY = secret_key_env

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DATABASE"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST") or "127.0.0.1",
        "PORT": os.getenv("POSTGRES_PORT") or "5432",
    }
}
