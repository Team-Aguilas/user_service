# Servicio de Usuarios y Autenticación - Marketplace API

Este microservicio es parte de la aplicación "Marketplace de Frutas y Verduras". Su responsabilidad es gestionar todo lo relacionado con los usuarios y la autenticación:

## Características Principales

-   Registro de nuevos usuarios.
-   Login de usuarios mediante email y contraseña.
-   Generación de tokens de acceso JWT (JSON Web Tokens).
-   Obtención de datos del usuario autenticado (`/me`).
-   Operaciones CRUD para la gestión de usuarios (protegidas para superusuarios).

## Tecnologías Utilizadas

-   **Framework:** FastAPI
-   **Base de Datos:** MongoDB (a través de Motor)
-   **Autenticación:** JWT con `python-jose`
-   **Hashing de Contraseñas:** `passlib` con `bcrypt`
-   **Lenguaje:** Python 3.11+
-   **Validación de Datos:** Pydantic

## Configuración y Puesta en Marcha

### Prerrequisitos

-   Python 3.11 o superior.
-   Una instancia de MongoDB corriendo.
-   Tener el código del `common/` en el directorio raíz del proyecto.

### 1. Configuración del Entorno

Este servicio se ejecuta desde la raíz del monorepo (`market_place_project/`).

1.  **Variables de Entorno:**
    Crea un archivo `.env` en la raíz de este servicio (`users_service/.env`) con el siguiente contenido. **¡Asegúrate de usar una `SECRET_KEY` segura!**
    ```env
    PROJECT_NAME="Servicio de Usuarios"
    MONGO_URI="mongodb://localhost:27017/"
    MONGO_DB_NAME="marketplace_db"
    SECRET_KEY="tu_clave_secreta_muy_larga_y_segura_aqui"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

2.  **Dependencias:**
    Desde la raíz del proyecto (`market_place_project/`), instala las dependencias:
    ```bash
    # Activa tu entorno virtual principal
    pip install -r users_service/requirements.txt
    ```

### 2. Ejecución del Servicio

Para ejecutar el servidor, abre una **nueva terminal** en la **carpeta raíz del proyecto (`market_place_project/`)** y sigue estos pasos:

1.  **Activa tu entorno virtual.**

2.  **Configura el `PYTHONPATH`**:
    ```powershell
    # En Windows (PowerShell)
    $env:PYTHONPATH="."
    ```
    ```bash
    # En Linux o macOS
    export PYTHONPATH="."
    ```

3.  **Inicia el servidor Uvicorn** en el puerto `8002`:
    ```bash
    uvicorn users_service.app.main:app --reload --port 8002
    ```

### Documentación de la API

Una vez que el servicio esté corriendo, la documentación interactiva (Swagger UI) estará disponible en:

[http://localhost:8002/docs](http://localhost:8002/docs)