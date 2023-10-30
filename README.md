# Backend CLBB

Una vez clonado este proyeto se debe ejecutar el siguiente comando para iniciar los contenedores:

`docker-compose up -d --build`

Una vez que las imagenes se descarguen y el proyecto se genere, se deben aplicar las migraciones, para esto ejecutamos el siguiente comando:

`docker exec -it clbb_web python manage.py migrate`

Luego debemos crear un super usuario para nuestro backend, para eso ejecutamos el siguiente comando y seguir las instrucciones de la linea de comando:

`docker exec -it clbb_web python manage.py createsuperuser`