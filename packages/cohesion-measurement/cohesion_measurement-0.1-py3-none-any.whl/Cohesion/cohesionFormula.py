import math
import pandas as pd


# -------------- Data Info --------------
def data_after_zero_shot_classification(path):
    authorized_columns = ['Unnamed: 0', 'doc', 'real_topic']
    data = pd.read_csv(path)
    topics = data.columns
    topics_without_underscore = []
    for topic in topics:
        if topic in authorized_columns:
            topics_without_underscore.append(topic)
        elif topic == 'doc_num':
            continue
        else:
            split_topic = topic.split('_')
            topics_without_underscore.append([topic, split_topic[1]] if len(split_topic) == 2 else [topic, topic])
    return data, topics_without_underscore


# -------------- helpers functions --------------
def insert_data_to_docs_collection(docs, topics):
    not_allow_topics = ['Unnamed: 0', 'doc', 'real_topic']
    list_to_insert = []
    scores = {}
    for index, row in docs.iterrows():
        for topic in topics:
            if topic not in not_allow_topics:
                scores[topic[1]] = row[topic[0]]
        object_doc = {'index': row['Unnamed: 0'], 'doc': row['doc'], 'real_topic': row['real_topic'],
                      'scores': scores.copy()}
        list_to_insert.append(object_doc)
        scores.clear()
    return list_to_insert


def insert_data_to_topics_collection(topics):
    not_allow_topics = ['Unnamed: 0', 'doc', 'real_topic']
    topics_dict = {}
    for index, topic in enumerate(topics):
        if topic in not_allow_topics:
            continue
        object_score = {'index': index - 3, 'description': topic[1], 'positive': 0, 'negative': 0}
        topics_dict[topic[1]] = object_score
    return topics_dict


# -------------- first insertions --------------

def first_insert_article(path):
    # print('cohesion process 1 - first_insert_article')
    data, topics = data_after_zero_shot_classification(path)
    docs_collection = insert_data_to_docs_collection(data, topics)
    topics_collection = insert_data_to_topics_collection(topics)
    return docs_collection, topics_collection


# -------------- Calculations --------------

def calculate_topics_score(docs_collection, topics_collection):
    # print('cohesion process 2 - calculate_topics_score')
    for index, (topic_name, topic_data) in enumerate(topics_collection.items()):
        positive, positive_length, negative, negative_length, positive_score, negative_score = 0, 0, 0, 0, 0, 0
        for doc in docs_collection:
            topic_doc_score = doc['scores'][topic_name]
            if doc['real_topic'] == topic_name:
                positive += topic_doc_score
                positive_length += 1
            elif topic_doc_score != 0:
                negative += topic_doc_score
                negative_length += 1
        # print('positive_length: ' + str(positive_length) + ', negative length: ' + str(negative_length))
        try:
            positive_score = positive / positive_length
            negative_score = negative / negative_length
        except:
            pass
            # print("Could not access calculate topic: {} division by zero".format(topic_data))
        topics_collection[topic_name]['positive'] = positive_score
        topics_collection[topic_name]['negative'] = negative_score
    return topics_collection


# -------------- Cohesion --------------
def calculate_topics_cohesion(topics_with_scores):
    # print('cohesion process 3 - calculate_topics_cohesion')
    positive, negative = 0, 0
    for index, (topic_name, topic_data) in enumerate(topics_with_scores.items()):
        positive += topic_data['positive']
        negative += topic_data['negative']
    # print('positive: ' + str(positive/(index + 1)) + ', negative: ' + str(negative/(index + 1)))
    score = (positive / (len(topics_with_scores) + 1)) - (negative / (len(topics_with_scores) + 1))
    return math.sqrt((score + 1)/2)


def main_calculate_cohesion(path):
    # print('Start calculate cohesion')
    docs_col, topic_col = first_insert_article(path)
    topics_with_scores = calculate_topics_score(docs_col, topic_col)
    score = calculate_topics_cohesion(topics_with_scores)
    # print('cohesion score - ' + str(score))
    return score
