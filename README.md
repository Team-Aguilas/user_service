# User Service - FastAPI Backend

Este módulo define una capa de servicios asincrónica para la gestión de usuarios en una base de datos MongoDB utilizando `motor`. También se encarga del hash de contraseñas mediante funciones de seguridad personalizadas.

## 📂 Ubicación

`app/services/user_service.py`

## 🚀 Funcionalidades principales

Este archivo proporciona funciones para manejar usuarios en la colección `users` de MongoDB.

### 📋 Operaciones disponibles

- **`get_user_by_email(db, email)`**  
  Retorna un usuario a partir de su dirección de correo electrónico.

- **`get_user_by_id(db, user_id)`**  
  Busca un usuario por su ID. Devuelve `None` si no lo encuentra o si el ID no es válido.

- **`create_user(db, user_in)`**  
  Crea un nuevo usuario, encriptando su contraseña antes de almacenarlo.

- **`update_user(db, user_id, user_in)`**  
  Actualiza la información de un usuario, incluyendo su contraseña si se proporciona.

- **`get_all_users(db, skip=0, limit=100)`**  
  Lista paginada de todos los usuarios registrados.

## 🧱 Modelos utilizados

- `UserCreate`
- `UserUpdate`
- `UserInDB`

> Asegúrate de que los modelos estén correctamente definidos en `app.models` y manejen el uso de `ObjectId` y `alias`.

## 🔐 Seguridad

Este servicio hace uso de la función `get_password_hash` desde `app.security` para almacenar contraseñas de forma segura.

## 🛠 Requisitos

- Python 3.10+
- `motor`
- `pydantic`
- `bson`
- Función de hashing (`get_password_hash`) implementada en el módulo de seguridad

## 📌 Notas

- Las funciones son **asincrónicas** para integrarse de forma eficiente con FastAPI.
- Los campos de contraseña se almacenan como `hashed_password`.

## ✅ Ejemplo de uso

```python
from app.services.user_service import create_user
from app.models import UserCreate

new_user = UserCreate(
    email="usuario@ejemplo.com",
    full_name="Nombre Apellido",
    password="contraseña123"
)

user = await create_user(db, new_user)
