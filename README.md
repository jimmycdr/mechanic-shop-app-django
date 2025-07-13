# 🛠️ Mechanic Shop App

API REST para la gestión de órdenes de mantenimiento y tareas asociadas en un taller mecánico.  
Desarrollado con **Django** y **Django REST Framework**.

## 🚀 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/jimmycdr/mechanic-shop-app-django.git
cd mechanic-shop-app

2. Instala las dependencias:

```bash
pip install -r requirements.txt

3. Aplica las migraciones:

```bash
python manage.py migrate

4. Ejecuta el servidor:

```bash
python manage.py runserver

## Cargar Datos iniciales:

```bash
python manage.py loaddata dump_maintenance.json