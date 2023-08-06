import copy
import os.path
import random
import pandas as pd
import numpy as np
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy.spatial.distance import euclidean
from sklearn.feature_extraction.text import TfidfVectorizer
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
stop_words = set(stopwords.words('english'))
glove = False
emmbed_glove_dict = {}

def tokenizer(text):
    word_tokens = word_tokenize(text)
    filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stop_words and w.isalpha()]
    return filtered_sentence


def docs_to_groups(docs, clusters):
    clusters_docs = dict()
    for index, doc in enumerate(docs):
        cluster = int(clusters[index])
        docs_list = clusters_docs.get(cluster, list())
        docs_list.append(doc)
        clusters_docs[cluster] = docs_list
    return clusters_docs


def create_input_to_mnli_topics_content(content_dict, path):
    content_list = []
    topics_ind_list = []
    for topic_ind in sorted(content_dict.keys()):
        content_list += content_dict[topic_ind]
        topics_ind_list += [topic_ind] * len(content_dict[topic_ind])
    df_topic_id_content = pd.DataFrame({"topic_ind": topics_ind_list, "content": content_list})
    df_topic_id_content.to_pickle(path, protocol=4)


def create_topic_id_topic_value(topics_ind_list, topic_values, path):
    topic_values_joined = []
    for ten_words_seperated in topic_values:
        topic_values_joined.append(" ".join(ten_words_seperated))
    df_topic_id_value_coherence = pd.DataFrame({"topic_ind": topics_ind_list, "topic_name": topic_values_joined})
    df_topic_id_value_coherence.to_pickle(path, protocol=4)


def get_sum_of_similarity(word_to_compare, words):
    if len(emmbed_glove_dict.get(word_to_compare, [])) == 0:
        return 999
    dist = 0
    words = words.copy()
    words.remove(word_to_compare)
    for w in words:
        dist += 0 if len(emmbed_glove_dict.get(w, [])) == 0 else euclidean(emmbed_glove_dict[word_to_compare],
                                                                           emmbed_glove_dict[w])
    return dist


def remove_nonsimilar_from_topic(topic):
    sums = [get_sum_of_similarity(w, topic) for w in topic]
    topic.pop(sums.index(max(sums)))


def tf_idf_top_words(docs: list):
    vectorized = TfidfVectorizer(use_idf=True, stop_words='english', ngram_range=(1, 1), max_df=0.95, min_df=0.001,
                                 tokenizer=tokenizer)
    tfidf_vectorized_vectors = vectorized.fit_transform(docs)
    feature_names = vectorized.get_feature_names_out()
    # get the first vector out (for the first document)
    first_vector_tfidfvectorizer = tfidf_vectorized_vectors[0]
    # place tf-idf values in a pandas data frame
    df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=feature_names, columns=["tfidf"])
    df = df.sort_values(by=["tfidf"], ascending=False)
    return df.index.values.tolist()[0:5]


def use_synonyms(labels_array):
    for w in labels_array:
        synonyms_array = enhance_topic_with_synonyms(w)
        for i in synonyms_array:
            labels_array = labels_array + i.split(' ')
        # labels_array = labels_array + word.split(' ') for word in enhance_topic_with_synonyms(w)
    return labels_array


def enhance_topic_with_synonyms(word):
    word = word.lower()
    synonyms = []
    synsets = wordnet.synsets(word)
    if (len(synsets) == 0):
        return []
    synset = synsets[0]
    lemma_names = synset.lemma_names()
    for lemma_name in lemma_names:
        lemma_name = lemma_name.lower().replace('_', ' ')
        if (lemma_name != word and lemma_name not in synonyms):
            synonyms.append(lemma_name)
    return synonyms[:2]


def docs_to_clusters(docs_list, docs_label):
    clusters_docs = dict()
    for index, label in enumerate(docs_label):
        doc_list = clusters_docs.get(label, list())
        doc_list.append(docs_list[index])
        clusters_docs[label] = doc_list
    return clusters_docs


def create_topic_name(key, labels_array):
    topic_name = str(key)
    for label in labels_array:
        topic_name += '_' + label
    return topic_name


def create_topic_names_using_tf_idf(docs, labels, is_synonym_enhanced=False, use_glove_reduction=False):
    tf_idf_labels, tf_idf_labels_synonyms, tf_idf_labels_glove = dict(), dict(), dict()
    labels_array_synonyms, labels_array_for_glove = [], []
    docs_groups = docs_to_clusters(docs, labels)
    for key, value in docs_groups.items():
        labels_array = tf_idf_top_words(value)
        if is_synonym_enhanced:
            labels_array_synonyms = use_synonyms(labels_array)
        if use_glove_reduction:
            labels_array_for_glove = copy.deepcopy(labels_array)
            remove_nonsimilar_from_topic(labels_array_for_glove)

        tf_idf_labels[key] = create_topic_name(key, labels_array)
        tf_idf_labels_synonyms[key] = create_topic_name(key, labels_array_synonyms)
        tf_idf_labels_glove[key] = create_topic_name(key, labels_array_for_glove)

    # print('Regular: ', tf_idf_labels)
    # print('Synonyms: ', tf_idf_labels_synonyms)
    # print('Glove: ', tf_idf_labels_glove)
    return tf_idf_labels, tf_idf_labels_synonyms, tf_idf_labels_glove


def create_random_division(ground_truth_df, random_percent):
    labels = ground_truth_df["label"].to_list()
    rows_indexes = list(range(len(ground_truth_df.index)))  # indexes of list not of df(!) - always start with 0.
    random_amount = int((random_percent / 100) * len(rows_indexes))
    random_indexes = random.sample(rows_indexes, random_amount)
    labels_extracted = ground_truth_df.iloc[random_indexes,]['label'].to_list()
    random.shuffle(labels_extracted)
    for i in random_indexes:
        labels[i] = labels_extracted.pop(0)
    return labels


def random_division(ground_truth_df, random_percent=0):
    new_division_labels = create_random_division(ground_truth_df, random_percent=random_percent)
    topics, topics_synonyms, topics_glove = create_topic_names_using_tf_idf(ground_truth_df['text'].tolist(),
                                                                            new_division_labels)
    return new_division_labels, topics, topics_synonyms, topics_glove


def read_data_from_csv(path_to_csv):
    if not os.path.exists(path_to_csv):
        raise Exception(f'file not exists : {path_to_csv}')
    ground_truth_df = pd.read_csv(path_to_csv, sep='\t', usecols=['label', 'text'])

    # prepare data
    ground_truth_list = ground_truth_df['text'].tolist()
    ground_truth_label_list = ground_truth_df['label'].tolist()
    return ground_truth_list, ground_truth_label_list


def read_glove_model(glove_model_path):
    with open(glove_model_path, 'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], 'float32')
            emmbed_glove_dict[word] = vector
