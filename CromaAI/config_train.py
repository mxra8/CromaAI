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