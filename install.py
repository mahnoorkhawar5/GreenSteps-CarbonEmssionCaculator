import os
import os
os.system("/home2/colorspr/virtualenv/django_project/3.11/bin/pip install django")
os.system("/home2/colorspr/virtualenv/django_project/3.11/bin/pip install gunicorn")
os.system("pip install -r /home2/colorspr/django_project/requirements.txt")

venv_pip = "/home2/colorspr/virtualenv/django_project/3.11/bin/pip"

# Upgrade pip
os.system(f"{venv_pip} install --upgrade pip")

