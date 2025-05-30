Existe un ejecutable del programa en la carpeta "dist\Sistema de Gestión de Alumnos" con el nombre "SGA.exe"

Para ejecutar el programa sin usar el .exe es necesario instalar las dependencias.

Instalar dependencias:
(ejecutar desde la carpeta del proyecto)

pip install -r requirements.txt


Crear ejecutable:

pyinstaller --noconsole --icon=_internal\media\icons\SGA.ico --add-data "_internal\media:media" main.py


