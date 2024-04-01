# Información del equipo
| Nombre             | Correo                       | Código    | 
|--------------------|------------------------------|-----------|
| Álvaro Bacca       | a.baccap@uniandes.edu.co     | 202121869 |
| Daniel Villar      | d.villarg@uniandes.edu.co    |  |
| Sebastián Guerrero | s.guerrero3@uniandes.edu.co  |  |
| Samuel Chaparro    | sa.chaparro2@uniandes.edu.co |  |
| Juan Pablo Jossa   | j.jossa@uniandes.edu.co      |  |

---

# Estructura del proyecto
## `/data`
Contiene los datos del proyecto. En la subcarpeta `/raw` se tienen los 
datos crudos. Es decir, los dados por el cliente. En la subcarpeta
`/processed` se tienen los datos procesados. Es decir, datos que han pasado
algún tipo de procesamiento ya sea de limpieza y/o preparación.

## `/models`
Contiene los modelos de _machine learning_ ya entrenados. Estos estarán
en formato pickle (`.pkl`) o joblib (`.joblib`).

## `/notebooks`
Contiene los _notebooks_ de Jupyter. Estos incluyen código, explicaciones
textuales, visualizaciones y resultados en documentos individuales. Los 
archivos están en formato `.ipynb`. Estos archivos se utilizarán 
principalmente en la etapa 1 para la exploración y creación de modelos. 

## `main.py`
Maneja la lógica principal del proyecto. Este archivo se utilizará
principalmente en la etapa 2 del proyecto para la creación de la aplicación
completa.

## `requirements.txt`
Contiene las librerías necesarias para correr cualquier parte del proyecto.
Su instalación se debería hacer dentro de un ambiente de ejecución (
se recomienda `venv` utilizando Python 3.11.8). Para instalar, desde la
consola, **con el ambiente activo**, utilizar:

``pip install -r requirements.txt``
