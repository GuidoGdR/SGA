para ejecutar el programa sin usar el .exe es necesario instalar las dependencias:
(desde la carpeta del proyecto ejecutar:)

pip install -r requirements.txt

Crear ejecutable:

pyinstaller --noconsole --icon=_internal\media\icons\SGA.ico --add-data "_internal\media:media" main.py


