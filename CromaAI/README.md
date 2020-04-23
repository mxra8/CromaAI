# Proceso de instalación y configuración de Croma Archive Intelligence (Croma AI)

## Introducción

Croma es un servicio que analiza tus noticias utilizando modelos machine learning para recomendar noticias similares. También identifica entidades mencionadas en tus textos como personas, organizaciones, lugares y más. Todo el procedimiento de entrenamiento es independiente de tu CMS y puede ser integrado luego de manera muy simple a través de una API basada en JSON.

Este software, su API y el entrenamiento de modelos pudieron realizarse gracias a un aporte de Google a través de su iniciativa Google News Initiative y el equipo de Croma Inc. 


## Descripción general
Croma AI fue desarrollado por completo por Croma Inc para facilitar el acceso de los medios de comunicación de habla hispana a herramientas de machine learning en idioma español. Con años de experiencia en este entorno conocemos la limitaciones y la dificultad de implementar este tipo de tecnología en redacciones grandes, medianas y mucho más en las pequeñas. Por eso desarrollamos Croma AI como una manera de allanar la barrera de entrada a los desarrolladores y medios que quieran experimentar con estas herramientas dentro de sus redacciones.El uso de este software es exclusivamente gratuito y de libre uso para todo medio de comunicación de América Latina que quiera incorporar machine learnign de manera sencilla a su operación diaria.

## Beneficios 
Estos son los beneficios que puede obtener su medio utilizando esta plataforma:
- Realizar un entrenamiento de machine learning de todo su archivo histórico sin necesidad de programar una sola línea de código. Todo lo que necesitas está incluido en este paquete.
- Incorporar noticias relacionadas en su artículos a través de una simple llamada a una API. Esta relaciones no se dan por simples keywords o categorías, sino que utiliza una comprensión de la totalidad del texto para recomendar noticias similares, por más que no compartan los mismos términos.
- Identificar personas, lugares, organizaciones y keywords mencionadas en sus textos. Esto permite la automatización de la generación de tags que pueden ser fácilmente utilizados para potenciar sus esfuerzos de SEO y taggeo de artículos, nuevos e históricos.
- Ofrecer un sistema de búsqueda de artículos basado en relevancia real de sus contenidos. Puede ofrecer búsquedas predictivas y relaciones por entidades en la página de resultados.
- Cualquier otra tarea que se pueda facilitar teniendo su archivo completo y actualizado indexado y accesible vía API.


## Requisitos
El software se debe instalar completamente en un servidor privado de su propiedad.

# Indicaciones para el proceso de instalación
 
## Instalación Anaconda
CromaAI utiliza conda como método de instalación por lo que sugerimos utilizar Anaconda para su instalación
https://anaconda.org/
Bajarlo de la página e instalarlo siguiendo las instrucciones dependiendo de su sistema operativo
      
  Instalar CromaAI
```
$ git clone git@github.com:cromaio/CromaAI.git 
$ cd CromaAI
```
         
## Creación de entorno
Ejecutar los siguientes comandos:
```bash
$ conda env create -f environment.yml 
```
Luego de la instalación acceder al entorno:
```bash
$ conda activate cromaAI
```
Por defecto crea el entorno cromaAI. Si quiere modificarlo puede hacerlo editando el archivo environment.yml situado en la raiz y volviendo a correr el primer comando
Si quiere instalar faiss con GPU debe modificar la linea de config del yml pytorch::faiss-cpu por pytorch::faiss-gpu
                    
## Archivo de configuración para la base de datos
CromaAI utiliza mongodb como base de datos. Abriendo CromaAI/config.py puede editar la configuración
```js
database = {
   'db_name': 'cromaAIdb',
   'host': 'localhost',
   'port': 27018
   }
```
 
## Correr mongo
Seleccione el puerto y el path que se ajuste a sus necesidades Ejecutar:
```bash
$ mongod --port 27018 --dbpath ./data/db/
```
El primer parámetro (port) debe coincidir con el del archivo config
El segundo parámetro es la carpeta donde se guardan los datos de la base de datos
   
## Archivo de configuración - Publicaciones default
Aquí puede modificar y agregar su medio. Hay un ejemplo aca: CromaAI/config.py.sample
```python
database = {
    'db_name': 'cromaAIdb',
    'host': 'localhost',
    'port': 27018
    }

active_publication = 'Redaccion'

publications = [
    {
        "api_url": 'https://cnnespanol.cnn.com/wp-json/wp/v2/',
        "name": 'CNN Esp',
        "fetch_method": 'wordpress',
        "location": 'USA', 
        "url": 'https://cnnespanol.cnn.com'
    },
    {
        "api_url": 'https://www.redaccion.com.ar/wp-json/wp/v2/',
        "name": 'Redaccion',
        "fetch_method": 'wordpress',
        "location": 'Argentina', 
        "url": 'https://www.redaccion.com.ar'
    }
]


models_folder = 'models/redaccion_2020/'
class models:
    gensim_w2v = f'{models_folder}w2vect/w2vect_2.wv' 
    faiss_indexes = f'{models_folder}faiss/indexes'  
    faiss_indexes_tfidf = f'{models_folder}faiss/indexes_tfidf'  
    faiss_ids = f'{models_folder}faiss/ids.npy'      
    spacy = f'{models_folder}ner/model-azure-aws-50k'
    token2tfidf = f'{models_folder}vectorizers/token2tfidf-max_df_1.0-min_df_1.npy'
```

## Buscar artículos y guardarlos en db
Asegurarse de tener un archivo de configuración correcto: config.py Hay un ejemplo: config.py.sample
Ejecutar:
```
$ cp ./CromaAI/config.py.sample ./CromaAI/config.py
```
Luego, para traer los archivos ejecutar
```
$ python ./CromaAI/fetch_articles.py
```
Esto traerá los archivos del medio definido en active_publication

## Bajar modelos de ejemplo
https://drive.google.com/a/croma.io/uc?id=1WqOmiHi4t-WejuiRlwt_6e2kAPaH3ixP&export=download
Copiarlo en carpeta repo_folder/CromaAI Y descomprimirlo
    
# Testeo API
 
## Aclaración
En esta etapa los modelos no están entrenados con los datos de artículos bajados en la etapa anterior. Por eso, no se esperan resultados en muchas de las siguientes APIs
 
## Correr API
Dentro de la carpeta repo_folder/CromaAI
```bash
$ python3 FlaskAPI.py -p 5000 -h localhost
```
Esto corre un servidor en el puerto 5000 por defecto. Puede cambiar el host y el port según sus necesidades
   
### Verficar API - /api/v1/articles
Escribir en el browser:
```
http://localhost:5000/api/v1/articles
```
o desde la linead de comando:

```
$ curl --location --request GET 'http://localhost:5000/api/v1/articles'
```

El resultado debería ser algo parecido a lo siguiente:
```js
{ "articles_page": [ {"_id": {"$oid": "5e9e1d65970a1cca9518671c"}, 
      "author": ["18"], 
      "publication": {
        "$oid": "5e9e16903993318678a548ad"
      }, 
      "publish_date": {
        "$date": 1587340800000
      }, 
      "summary": "<p>La pandemia gatilla …”
      "text": "Esta es la foto del COVID-19 esta ", 
      "title": "GPS PM del lunes 20 de abril del 2020", 
      "url": "https://www.redaccion.com.ar/gps-pm-del-lunes-20-de-abril-del-2020/"
    }, ...
    ]
}
```

### Verficar API - /api/v1/article
Obtener el id del primer articulo, en nuestro ejemplo: 5e9e1d65970a1cca9518671c
Y colocarlo en el pedido para verificar funcionamiento

Escribir en el browser:
```
http://localhost:5000/api/v1/article?id=5e9e1d65970a1cca9518671c
```
o desde la linead de comando:

```
$ curl --location --request GET 'http://localhost:5000/api/v1/article?id=5e9e1d65970a1cca9518671c'
```

El resultado debería ser algo parecido a lo siguiente:
```js
{ "article: [{"_id": {"$oid": "5e9e1d65970a1cca9518671c"}, 
      "author": ["18"], 
      "publication": {
        "$oid": "5e9e16903993318678a548ad"
      }, 
      "publish_date": {
        "$date": 1587340800000
      }, 
      "summary": "<p>La pandemia gatilla …”
      "text": "Esta es la foto del COVID-19 esta ", 
      "title": "GPS PM del lunes 20 de abril del 2020", 
      "url": "https://www.redaccion.com.ar/gps-pm-del-lunes-20-de-abril-del-2020/"
    }
}

```

### Verficar API - /api/v1/article_entities

Obtener el id del primer articulo, en nuestro ejemplo: 5e9e1d65970a1cca9518671c
Y colocarlo en el pedido para verificar funcionamiento

Escribir en el browser:
```
http://localhost:5000/api/v1/article_entities?id=5e9e1d65970a1cca9518671c&cloud=spacy
```
o desde la linead de comando:

```bash
$ curl --location --request GET 'http://localhost:5000/api/v1/article_entities?id=5e9e1d65970a1cca9518671c&cloud=spacy'
```

### Verificar API - /api/v1/analyzer/text
Ejecutar desde la linead de comando:
```bash
$ curl --location --request POST 'http://localhost:5000/api/v1/analyzer/text' \
--header 'Content-Type: application/json' \
--data-raw '"Cristina Kirchner se reunio con Mauricio Macri en la Casa Rosada"'
```
El resultada debería ser algo similar a esto:
```js
{
  "doc": {
    "ents": [
      {
        "end": 17, 
        "label": "PER", 
        "start": 0
      }, 
      {
        "end": 46, 
        "label": "PER", 
        "start": 32
      }, 
      {
        "end": 64, 
        "label": "ORG", 
        "start": 53
      }
    ], 
    "text": "Cristina Kirchner se reunio con Mauricio Macri en la Casa Rosada", 
    "tokens": [
      {
        "end": 8, 
        "id": 0, 
        "start": 0
      }, ... 
      {
        "end": 64, 
        "id": 10, 
        "start": 58
      }
    ]
  }, 
  "html": "<div class=\"entities\" style=\"line-height: 2.5; direction: ltr\"><mark class=\"entity\" style=\"background: #ddd; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">Cristina Kirchner<span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem\">PER</span></mark> se reunio con <mark class=\"entity\" style=\"background: #ddd; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">Mauricio Macri<span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem\">PER</span></mark> en la <mark class=\"entity\" style=\"background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">Casa Rosada<span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem\">ORG</span></mark></div>", 
  "related_articles": [
    {
      "article_id": "5e9e1ce2970a1cca95185cde", 
      "similarity": 0.36494454741477966
    }, ... ,
    {
      "article_id": "5e9e1d25970a1cca95186237", 
      "similarity": 0.21402746438980103
    }
  ]
}
```
    
### Verificar API - /api/v1/w2v/autocompete
```
$ curl --location --request POST 'localhost:5000/api/v1/w2v/autocomplete' \
--header 'Content-Type: application/json; charset=UTF-8' \
--data-raw '"Mau"'
```
```js
{
  "words": [
    "Mauricio Macri", 
    "Mauricio macri", 
    "Mauricio", 
    "Mauricio ) Macri", 
    "Mauricio Claver", 
    "Mauro", 
    "Mauricio !", 
    "Maurice Closs", 
    "Mauro Viale", 
    "Mauro Icardi", 
    "Maure Inmobiliaria"
  ]
}
```

 
### Verificar API - /api/v1/w2v/similar
```bash
$ curl --location --request POST 'localhost:5000/api/v1/w2v/similar' \
--header 'Content-Type: application/json' \
--data-raw '{
    "word": "kirchnerismo"
}'
```

```js
{
  "similar_words": [
    {
      "similarity": 0.766370952129364, 
      "word": "peronismo"
    }, 
    {
      "similarity": 0.6919558644294739, 
      "word": "oficialismo"
    }, 
    ...
  ]
}
```

### Verificar API - /api/v1/w2v/related

```bash
$ curl --location --request GET 'http://localhost:5000/api/v1/related?id=5e9e1d65970a1cca9518671c'
```
```js
{
  "related_articles": [
    {
      "article_id": "5e9e1d65970a1cca9518671c", 
      "similarity": 1.0
    }, 
    ...,
    {
      "article_id": "5e9e1d5b970a1cca95186662", 
      "similarity": 0.8513200283050537
    }
  ]
}
```

# Entrenamiento de Modelos
 
## Modelos y técnicas
- NER
- word2Vect - TFIDF
- faiss
 
## NER
Croma provee un modelo pre-entrenado con 50k artículos de medios periodísticos. Los datos de entrenamiento se obtuvieron por comparación de las APIs de AZURE, AWS y GCP y la verificación de personas. El modelo es parte pública de CromaAI y se utiliza a través de Spacy
 
## w2v
Con la tokenización utilizada con el modelo de NER se entrena un modelo de w2v en formato de la librería gensim. Este modelo se utiliza después para relacionar artículos, búsqueda de palabras similares y autocomplete. CromaAI proporciona un modelo pre-entrenado y también las herramientas para entrenar con sus propios artículos.
 
##  TFIDF
Se utiliza esta técnica para mejorar los resultados del modelo w2v en la búsqueda de artículos relacionados.
 
##  FAISS
Esta librería se utiliza para realizar las búsquedas de artículos relacionados de manera eficiente
 
##  Recomendaciones para el entrenamiento
Se recomienda utilizar el modelo de spacy para la tokenización como el modelo pre-entrenado de w2v. Esto se puedo modificar en las siguientes variables del archivo de configuración: spacy_model, word2vect_model
 
##   Archivo de configuración de training - congif_train.py
```python
database = {
    'db_name': 'cromaAIdb',
    'host': 'localhost',
    'port': 27018
    }

model_name = 'redaccion_2020'
spacy_model = 'ML_models/model-azure-aws-50k'
# Si word2vect_model es None, lo busca en la carpeta model_name/w2vect
# Si es un path a archivo, directamente enabled_processes.w2v no lo compara
word2vect_model = 'ML_models/w2vect_2.wv'
publication_name = 'Redaccion'
chunk_size = 1_000

enabled_processes = {
    "tokenize_articles": False,
    "vectorizers": False,
    "w2v": False,
    "faiss": True
}

vectorizeers_hyperparams = {
    "min_df": 1,
    "max_df": 1.0
}

w2v_hyperparams = {
    "size": 100,
    "epochs": 6,
    "min_count":2, 
    "workers":4, 
}
```
##  Entrenar modelos:
Para entrenar los modelos ejecutar:
```bash
$ python3 train_models.py
```
Recuerde antes revisar el archivo config_train.py
     
 
   