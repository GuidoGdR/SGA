## 🚀 Sistema de Gestión de Alumnos (SGA)

Este proyecto es una aplicación de escritorio para la **Gestión de Alumnos**.

---

### 📦 Ejecutable del Programa (Sin Dependencias)

Puedes encontrar una versión ejecutable del programa lista para usar (que no requiere instalar Python ni dependencias) en la siguiente ruta:

* **Ruta:** `dist\Sistema de Gestión de Alumnos\SGA.exe`

Para iniciar el programa, simplemente haz doble clic en **`SGA.exe`**.

---

### ⚙️ Ejecución desde el Código Fuente (Con Dependencias)

Si deseas ejecutar la aplicación directamente desde el código fuente (`main.py`), es **necesario instalar las dependencias** del proyecto.

#### 🛠️ Instalación de Dependencias

Para instalar todas las librerías requeridas, ejecuta el siguiente comando desde la **carpeta raíz del proyecto**:

```bash
pip install -r requirements.txt
```

### 🏗️ Creación del Ejecutable (`.exe`)

Si necesitas generar un nuevo ejecutable del programa, puedes usar `pyinstaller`. Este comando empaqueta la aplicación, oculta la consola e incluye el ícono y los recursos multimedia necesarios:

#### 📝 Comando de Creación

Ejecuta el siguiente comando desde la **carpeta raíz del proyecto**:

```bash
pyinstaller --noconsole --icon=_internal\media\icons\SGA.ico --add-data "_internal\media:media" main.py
```
