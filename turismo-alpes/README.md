# Información del equipo
| Nombre             | Correo                       | Código    | 
|--------------------|------------------------------|-----------|
| Álvaro Bacca       | a.baccap@uniandes.edu.co     | 202121869 |
| Sebastián Guerrero | s.guerrero3@uniandes.edu.co  | 202021249 |
| Daniel Villar      | d.villarg@uniandes.edu.co    | 201923374 |
| Samuel Chaparro    | sa.chaparro2@uniandes.edu.co | 202310076 |
| Juan Pablo Jossa   | j.jossa@uniandes.edu.co      | 202310596 |

---

# Estructura del proyecto
## `/data`
Contiene los datos del proyecto. En la subcarpeta `/raw` se tienen los 
datos crudos. Es decir, los dados por el cliente. En la subcarpeta
`/processed` se tienen los datos procesados. Es decir, datos que han pasado
algún tipo de procesamiento ya sea de limpieza y/o preparación.

Se deben descargar los archivos de 

https://uniandes-my.sharepoint.com/:f:/g/personal/a_baccap_uniandes_edu_co/EhFRbFpP35VFgp5d_uBD_pUBCgSyI4cCpIX10p1gZfpDLA?e=FNllvr

y poner en la carpeta de ```/processed``` para ejecutar el notebook. 
Su elevado peso no permitió que quedaran en el repositorio

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

## Notas
Debido a observaciones de último minuto, el entendimiento de datos quedó
más completo en la rama de ```feature/entendimiento-v3``` y de allí se
extrajeron las gráficas utilizadas en el documento. Asimismo, se cuenta
con funciones adicionales de limpieza y preparación de datos que, dado
su bajo rendimiento en las pruebas, fueron descartadas (explicación en
el documento de entrega).