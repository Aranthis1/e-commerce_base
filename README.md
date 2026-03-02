# e-commerce_base
Proyecto base
# 🛒 E-Commerce Base - Módulo de Administración (MVP)

Este proyecto es un Producto Mínimo Viable (MVP) enfocado exclusivamente en la gestión del catálogo de un e-commerce. Funciona como un panel de administración personalizado donde los usuarios autorizados pueden realizar operaciones CRUD completas sobre los productos.

## ⚙️ 1. Motor de Base de Datos Utilizado

El proyecto utiliza **SQLite3** como motor de base de datos relacional. 
Esta es la opción por defecto de Django y es ideal para este MVP porque no requiere configuración adicional de servidores externos, permitiendo que el proyecto sea altamente portable. 

*(Nota: Gracias al uso del ORM de Django, el motor puede ser escalado fácilmente a PostgreSQL o MySQL en el futuro modificando únicamente el archivo `settings.py`)*.

## 📦 2. Descripción del Modelo de Datos

Todas las operaciones de datos se gestionan a través del ORM de Django. El núcleo de este MVP es la entidad `Product`, definida en `models.py` con los siguientes atributos y validaciones:

* **`name`** (`CharField`): Nombre descriptivo del producto (máx. 200 caracteres).
* **`description`** (`TextField`): Detalles amplios del producto (opcional).
* **`category`** (`CharField` con `choices`): Categoría predefinida del producto. Funciona con una lista estricta para asegurar la integridad de los datos (Ej: Electrónica, Ropa, Hogar).
* **`price`** (`DecimalField`): Precio del producto. Cuenta con un `MinValueValidator` a nivel de base de datos y de formulario para garantizar que el valor sea estrictamente **mayor a 0**.
* **`stock`** (`PositiveIntegerField`): Cantidad de unidades disponibles en inventario (no permite números negativos).
* **`image`** (`ImageField`): Permite cargar y almacenar una imagen física del producto en el servidor (requiere la librería `Pillow`).

## 🗺️ 3. Rutas Principales del Módulo de Administración

El proyecto cuenta con un sistema de rutas protegidas mediante el decorador `@login_required`. Solo los administradores autenticados pueden acceder a las siguientes URLs:

* `GET /accounts/login/`: Pantalla de autenticación y acceso al panel.
* `GET /products/`: **Listado de productos**. Incluye funcionalidades de:
  * Paginación (5 productos por página).
  * Buscador por coincidencia de nombre (`icontains`).
* `GET/POST /products/create/`: **Formulario de creación**. Permite añadir nuevos productos validando campos obligatorios y mostrando una previsualización de la imagen mediante JavaScript.
* `GET/POST /products/edit/<id>/`: **Formulario de edición**. Carga los datos existentes de un producto (asegurando su existencia mediante `get_object_or_404`) para modificarlos.
* `GET/POST /products/delete/<id>/`: **Eliminación**. Pantalla de confirmación para eliminar de manera permanente un producto del catálogo.

Además, el sistema cuenta con un manejo de **Error 404** personalizado con interfaz gráfica.

## 🚀 4. Pasos para Ejecutar el Proyecto

Para levantar este proyecto en un entorno local, sigue estas instrucciones en tu terminal:

**Paso 1: Clonar/Ubicar el proyecto**
Ubícate en la carpeta raíz del proyecto (donde se encuentra el archivo `manage.py`).

**Paso 2: Crear y activar un entorno virtual (Recomendado)**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

**Paso 3: Instalar dependencias
#(Este proyecto requiere Django y Pillow)
pip install django pillow

**Paso 4: Aplicar migraciones a la Base de Datos
#Crea la estructura de tablas necesaria en SQLite3.
python manage.py makemigrations
python manage.py migrate

**Paso 5: Crear un superusuario (Administrador)
python manage.py createsuperuser

**Paso 6: Iniciar el servidor de desarrollo
python manage.py runserver
#Una vez que el servidor esté corriendo, abre tu navegador y visita: http://127.0.0.1:8000/products/. El sistema te pedirá que inicies sesión con las credenciales creadas en el Paso 5.