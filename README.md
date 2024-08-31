# Proyecto ETL para Datos de Educación

Este proyecto ETL (Extract, Transform, Load) está diseñado para procesar y cargar datos de educación en una base de datos SQL Server. El proyecto incluye scripts para crear las tablas necesarias en la base de datos y un script Python para realizar el proceso ETL.

## Estructura del Proyecto

- `etl.py`: Script principal de ETL que extrae, transforma y carga los datos.
- `dimension_mappings.json`: Archivo JSON que contiene los mapeos de las dimensiones.
- `script.sql`: Script SQL para crear las tablas en la base de datos.
- `c00051a__microdatos_edatos_2012-2022_ckan.csv`: Archivo CSV con los datos de entrada.

## Requisitos

- Python 3.6 o superior
- SQLAlchemy
- pyodbc
- Pandas
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea un entorno virtual e instala las dependencias:

    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Configura tu conexión a la base de datos en el archivo `etl.py`:

    ```python
    connection_string = 'mssql+pyodbc://usuario:contraseña@localhost:puerto/nombre_base_datos?driver=ODBC+Driver+17+for+SQL+Server'
    ```
4.  Descargar el archivo csv desde:
https://datos.gob.es/es/catalogo/a05003423-microdatos-de-insercion-laboral-de-los-egresados-de-las-universidades-publicas-presenciales-de-canarias-estudio-longitudinal-desde-2012

## Uso

1. Crea las tablas en la base de datos ejecutando el script SQL:

    ```sh
    sqlcmd -S localhost -U usuario -P contraseña -d nombre_base_datos -i script.sql
    ```

2. Ejecuta el script ETL:

    ```sh
    python etl.py
    ```

## Estructura de las Tablas

### University

| Columna          | Tipo         | Descripción                        |
|------------------|--------------|------------------------------------|
| University_ID    | INT          | Identificador único de la universidad |
| University_Name  | VARCHAR(255) | Nombre de la universidad           |
| Description      | VARCHAR(255) | Descripción                        |

### Teaching_Field

| Columna            | Tipo         | Descripción                        |
|--------------------|--------------|------------------------------------|
| Teaching_Field_ID  | INT          | Identificador único del campo de enseñanza |
| Teaching_Field_Name| VARCHAR(255) | Nombre del campo de enseñanza      |
| Description        | VARCHAR(255) | Descripción                        |

### Academic_Level

| Columna            | Tipo         | Descripción                        |
|--------------------|--------------|------------------------------------|
| Academic_Level_ID  | INT          | Identificador único del nivel académico |
| Academic_Level_Name| VARCHAR(255) | Nombre del nivel académico         |
| Description        | VARCHAR(255) | Descripción                        |

### Gender

| Columna     | Tipo         | Descripción                        |
|-------------|--------------|------------------------------------|
| Gender_ID   | INT          | Identificador único del género     |
| Gender_Name | VARCHAR(50)  | Nombre del género                  |

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.