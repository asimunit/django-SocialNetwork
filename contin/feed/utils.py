from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from joblib import dump, load
import numpy as np
import nltk
from nltk.tag.stanford import StanfordNERTagger
from .constant import *
import spacy
import subprocess

lemi = WordNetLemmatizer()
tfidf_vectorizer = TfidfVectorizer(stop_words='english')


def post_similarity(query, docs):
    docs.insert(0, query)
    process_docs = [' '.join(map(lambda w: lemi.lemmatize(w), post.split()))
                    for post in docs]
    tfidf_matrix = tfidf_vectorizer.fit_transform(process_docs)
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])
    return similarity


def predict_class(post):
    post_list = [post]
    clf = load(classifier_file_path)
    result = clf.predict(post_list)
    # optimize so that it does not load everytime
    return np.array(np.nonzero(result[0])).tolist()[0]


def stanford_ner(post):
    jar = jar_file_path
    model = ner_model_file_path
    ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
    words = nltk.word_tokenize(post)
    res = ner_tagger.tag(words)
    organisation = []
    location = []
    name = []
    [organisation.append(a) if b == 'ORGANIZATION' else location.append(
        a) if b == 'LOCATION' else name.append(a) if b == 'PERSON' else '' for
     a, b in res]
    response = {
        'organisation': organisation,
        'location': location,
        'name': name

    }

    return response


def spacy_ner(post):
    organisation = []
    location = []
    name = []
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(post)
    [organisation.append(ent.text) if ent.label_ == 'ORG' else location.append(
        ent.text) if ent.label_ == 'LOC' else name.append(
        ent.text) if ent.label_ == 'PERSON' else '' for ent in doc.ents]
    response = {
        'organisation': organisation,
        'location': location,
        'name': name

    }

    return response


def ner(post):
    with open('sample.txt', 'w') as file:
        file.write(post)

    cmnd = 'java -mx600m -cp "*:lib/*" edu.stanford.nlp.ie.crf.CRFClassifier ' \
           '-loadClassifier classifiers/english.all.3class.distsim.crf.ser' \
           '.gz -textFile sample.txt '
    output = subprocess.check_output(cmnd
                                     , shell=True)
    output = output.decode("utf-8")
    tagged_tokens = [tuple(ttok.split('/')) for ttok in output.split()]
    entities = []
    current_entity = []

    last_tag = None

    for i in range(len(tagged_tokens)):

        token, tag = tagged_tokens[i]

        if tag == 'O' or last_tag != tag:

            if last_tag != 'O' and last_tag is not None:
                current_entity = [str(i) for i in current_entity]
                entities.append((' '.join(current_entity), last_tag))
            current_entity = []
        last_tag = tag
        current_entity.append(token)
    entities_binned = {
        'ORGANIZATION': [],
        'PERSON': [],
        'LOCATION': []
    }
    for entity, tag in entities:
        if tag not in entities_binned:
            entities_binned[tag] = []

        entities_binned[tag].append(entity)
    return entities_binned


