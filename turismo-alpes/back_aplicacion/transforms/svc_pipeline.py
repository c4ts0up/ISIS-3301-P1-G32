"""
    Service adapter para uso de modelos
"""
import os
import re
from copy import deepcopy
import nltk
import pandas as pd
import stanza
import unicodedata
from joblib import load, dump
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


def build_pipeline(
    pipeline_dump_path: str,
    vectorizer_dump_path: str,
    data_path: str,
    percent_train: float = 0.05
):

    # crea la instancia del pipeline con las clases internas
    pipeline = Pipeline(
        steps=[
            ('lemmatizer', Lemmatizer()),
            ('post-cleaner', PostCleaner(cleaning_func=clean_text)),
            ('vectorizer', Vectorizer()),
            ('classifier', SVC(kernel='rbf', C=1))
        ]
    )

    # carga los datos y toma una muestra
    df_big = pd.read_csv(data_path)
    df = df_big.sample(frac=percent_train)

    # pre procesa los datos para entrenar
    df = Preprocesser().fit_transform(df)

    # crea datasets de entrenamiento y puntuación
    xtr, xts, ytr, yts = train_test_split(
        df['Review'],
        df['Class'],
        test_size=0.20,
        random_state=42069
    )
    xtr = pd.DataFrame(xtr)
    xts = pd.DataFrame(xts)

    # entrena y puntua
    pipeline.fit(xtr, ytr)
    print(pipeline.score(xts, yts))

    # guarda los modelos
    dump(pipeline['vectorizer'], vectorizer_dump_path)
    dump(pipeline, pipeline_dump_path)


def load_pipeline(
    pipeline_path: str,
    vectorizer_path: str,
):
    """

    :param pipeline_path: dirección relativa del joblib del pipeline
    :param vectorizer_path: dirección relativa del joblib del vectorizador
    :return:
    """
    # carga el vectorizador
    vectorizer = load(vectorizer_path)
    # carga el pipeline
    pipeline = load(pipeline_path)
    # sobreescribe el vectorizador con el vectorizador guardado
    #pipeline['vectorizer'].vectorizer_algorithm = vectorizer

    return pipeline


class Preprocesser(BaseEstimator, TransformerMixin):
    """
    Preprocesamiento utilizado únicamente para entrenamiento del modelo
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        alfa = 0.05
        beta = 0.05

        # eliminación de nulos
        df_work = X.dropna()
        # eliminación de duplicados
        df_work = df_work.drop_duplicates()

        # eliminación de longitudes atípicas
        df_work['Conteo'] = [len(x.split()) for x in df_work['Review']]
        upper = df_work['Conteo'].quantile(1 - beta)
        lower = df_work['Conteo'].quantile(alfa)
        # menores que percentil mayor
        df_work = df_work[df_work['Conteo'] <= upper]
        # mayores que percentil menor
        df_work = df_work[df_work['Conteo'] >= lower]

        df_work = df_work.drop(['Conteo'], axis=1)

        return df_work


class Lemmatizer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.stanza_pipeline = stanza.Pipeline(lang="es", processors="tokenize,mwt,pos,lemma")

    def fit(self, X, y=None):
        return self

    def stanza_preprocessing(self, words):
        doc = self.stanza_pipeline(words)
        lemmas = [w.lemma for w in doc.sentences[0].words]
        return lemmas

    def transform(self, X):
        print("Lemmatize transformation...")
        df_work = X
        df_work['Review'] = df_work['Review'].apply(self.stanza_preprocessing)
        return df_work

    def __getstate__(self):
        # Exclude the stanza_pipeline from serialization
        state = self.__dict__.copy()
        del state['stanza_pipeline']
        return state

    def __setstate__(self, state):
        # Restore the stanza_pipeline during deserialization
        self.__dict__.update(state)
        self.stanza_pipeline = stanza.Pipeline(lang="es", processors="tokenize,mwt,pos,lemma")


def clean_text(words):
    """
    Cleans the list of words by performing various operations.

    :param words: (list) List of words to be cleaned.
    :returns: (list) Cleaned list of words.
    """
    words = [w.lower() for w in words]  # Lowercase
    words = [re.sub(r'[^\w\s]', '', word) for word in words if word is not None]  # Remove punctuation
    words = [unicodedata.normalize('NFKD', word).encode('utf-8', 'ignore').decode('utf-8', 'ignore') for word in
             words]  # Remove non-encoded characters
    languages = ['spanish']
    stopword = nltk.corpus.stopwords.words(languages)
    return [w for w in words if w not in stopword]  # Remove stopwords


class PostCleaner(BaseEstimator, TransformerMixin):

    def __init__(self, cleaning_func):
        self.cleaning_func = cleaning_func

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        print("Post lemmatization cleaning transformation...")
        df_work = X.copy()
        df_work['Review'] = df_work['Review'].apply(self.cleaning_func)
        return df_work


class Vectorizer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.vectorizer_algorithm = TfidfVectorizer(
            decode_error='ignore',
            strip_accents='ascii',
            analyzer='word',
            max_features=10000
        )
        self.features = None

        # remiendo. En la primera pasada, se genera el vocabulario
        self.already_fit = False

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        data_stringfied = deepcopy(X)
        data_stringfied['Review'] = data_stringfied['Review'].apply(lambda x: ' '.join(map(str, x)))

        x_data = data_stringfied['Review']

        if self.already_fit:
            print("Vocabulario ya definido...")
            x_data_vectorized_matrix = self.vectorizer_algorithm.transform(x_data)
        else:
            print("Creando vocabulario...")
            x_data_vectorized_matrix = self.vectorizer_algorithm.fit_transform(x_data)

        x_data_vectorized_df = pd.DataFrame(
            x_data_vectorized_matrix.toarray())  # ... for additional features from csr_matrix

        # obtiene el arreglo de palabras con columnas
        self.features = self.vectorizer_algorithm.get_feature_names_out()
        self.already_fit = True

        res = pd.concat([x_data_vectorized_df], axis=1)

        return res
