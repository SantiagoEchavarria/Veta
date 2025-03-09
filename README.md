# Configuración del Entorno Virtual (venv)

## 🔍 ¿Por qué no se sube `venv` al repositorio?
El directorio `venv` contiene un entorno virtual de Python que es específico para cada sistema operativo y máquina. Subirlo al repositorio causaría problemas de compatibilidad entre diferentes usuarios. Además:

- Los archivos dentro de `venv` pueden ser pesados y cambiar frecuentemente.
- La configuración del entorno puede variar según el sistema operativo.
- Se pueden regenerar fácilmente con los paquetes necesarios.

Por eso, en su lugar, usamos un archivo `requirements.txt` que contiene todas las dependencias necesarias.

## ✔️ Pasos para configurar `venv` después de clonar el repositorio

### 1. **Clonar el repositorio**
Si aún no has clonado el proyecto, usa el siguiente comando:
```bash
    git clone https://github.com/SantiagoEchavarria/Veta.git
    cd Veta
```

### 2. **Crear el entorno virtual**
Ejecuta el siguiente comando según tu sistema operativo:

#### ✨ **En Windows**
```bash
    python -m venv venv
```

#### ✨ **En Linux/macOS**
```bash
    python3 -m venv venv
```

### 3. **Activar el entorno virtual**
Antes de instalar las dependencias, debes activar el entorno:

#### 💻 **En Windows (CMD o PowerShell)**
```bash
    venv\Scripts\activate
```

#### 💻 **En Linux/macOS**
```bash
    source venv/bin/activate
```

Si el comando fue exitoso, deberías ver `(venv)` al inicio de la línea de comandos.

### 4. **Instalar las dependencias**
Una vez activado el entorno virtual, instala los paquetes necesarios con:
```bash
    pip install -r requirements.txt
```

Si no existe `requirements.txt`, puedes generarlo con:
```bash
    pip freeze > requirements.txt
```

### 5. **Verificar la instalación**
Puedes verificar que Django y otras dependencias estén instaladas ejecutando:
```bash
    python -m django --version
```
Si no hay errores, todo está listo. 🌟

### 6. **Desactivar el entorno virtual (opcional)**
Si terminas de trabajar y quieres salir del entorno virtual, usa:
```bash
    deactivate
```
Esto restaurará la configuración original de Python en tu sistema.

---

## 🎉 ¡Listo! Ahora puedes ejecutar el proyecto
Si el proyecto es una aplicación Django, puedes iniciarlo con:
```bash
    python manage.py runserver
```
Recuerda siempre activar el entorno virtual antes de ejecutar cualquier comando relacionado con el proyecto. ✨

