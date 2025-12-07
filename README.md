# Configuración del Entorno Virtual (venv)

## Pasos básicos después de clonar el repositorio

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/SantiagoEchavarria/Veta.git
   cd Veta
   ```
2. **Crear el entorno virtual**
   [3.11.2](https://www.python.org/downloads/release/python-3112/)
    ```bash
   # Trabaja con la version 3.11
   # python3.11 -m venv venv
   py -3.11 -m venv venv
   ```
  
3. **Activar el entorno virtual**
   ```bash
   # Windows (CMD o PowerShell)
   venv\Scripts\activate
   ```
   ```
   # Linux/macOS
   source venv/bin/activate
   ```
4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ``` 
---
## Ejecutar el proyecto  
```bash
python manage.py runserver
```

