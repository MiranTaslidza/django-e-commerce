@echo off
@REM ovde se koeisti tačna putanja iza /d ukoliko putanja sadrži razmak koristiti navodne znakove
cd /d "D:\django-e-commerce"
"D:\django-e-commerce\venv\Scripts\python.exe" manage.py delete_inactive_users
