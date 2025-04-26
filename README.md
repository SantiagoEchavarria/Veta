# Configuración del Entorno Virtual (venv)

## Pasos básicos después de clonar el repositorio

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/SantiagoEchavarria/Veta.git
   cd Veta
   ```
2. **Crear el entorno virtual**
   ```bash
   # Windows
   python -m venv venv

   # Linux/macOS
   python3 -m venv venv
   ```
3. **Activar el entorno virtual**
   ```bash
   # Windows (CMD o PowerShell)
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```
4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
5. **Si no existe `requirements.txt`, puedes generarlo con**
    ```bash
    pip freeze > requirements.txt
    ```
6. **Verificar instalación**
   ```bash
   python -m django --version
   ```
7. **Desactivar entorno virtual (opcional)**
   ```bash
   deactivate
   ```

---

## Usar una versión específica de Python (opcional)

Si necesitas especificar una versión concreta de Python (por ejemplo, 3.11):

1. **Crear entorno virtual con versión específica**
   ```bash
   # Reemplaza 3.11 por tu versión deseada
   python3.11 -m venv venv
   ```
2. **Verificar versión del entorno virtual**
   ```bash
   # Windows
   venv\Scripts\python --version

   # Linux/macOS
   venv/bin/python --version
   ```

---

## Ejecutar el proyecto  
```bash
python manage.py runserver
```

