from sklearn.metrics import normalized_mutual_info_score
from src.Cohesion.cohesionFormula import main_calculate_cohesion
import os
from utils import tokenizer, docs_to_groups, create_input_to_mnli_topics_content, create_topic_id_topic_value
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel

from zeroShotClassifier import ZeroShotClassifier


def get_coherence(docs_list: list, topics_names: list):
    # Evaluate
    texts = [tokenizer(t) for t in docs_list]
    word2id = Dictionary(texts)
    coherence_model = CoherenceModel(topics=topics_names,
                                     texts=texts,
                                     dictionary=word2id,
                                     coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    return coherence_score


def extract_topics_labels(model, model_config=False):
    topics_info = model.get_topic_info()['Name'].tolist() if model_config else model
    topics_names = list(map(lambda x: x.split('_')[1:], topics_info))
    return topics_names


def calculate_nmi_score(ground_truth_label, new_division_labels):
    score = normalized_mutual_info_score(ground_truth_label, new_division_labels)
    # print('nmi score: ' + str(score))
    return score


def calculate_coherence_score(ground_truth_list, topics_names):
    score = get_coherence(docs_list=ground_truth_list, topics_names=topics_names)
    # print('coherence score: ' + str(score))
    return score


def calculate_cohesion_score(ground_truth_list, topics, topics_names):
    # prepare pickles files
    # print('prepare pickles files...')
    path_to_save = os.getcwd() + '\\..\\Cohesion\\CohesionDatasets\\doc_topic_mnli_results'
    topic_id_content = os.getcwd() + '\\..\\Cohesion\\CohesionDatasets\\topic_id_content.pkl'
    topic_id_value_map = os.getcwd() + '\\..\\Cohesion\\CohesionDatasets\\topic_id_topic_value_map.pkl'

    clusters_docs = docs_to_groups(ground_truth_list, topics)
    create_input_to_mnli_topics_content(clusters_docs, topic_id_content)
    create_topic_id_topic_value(sorted(clusters_docs.keys()), topics_names, topic_id_value_map)

    # create csv with mnli score
    # print('create csv with mnli score...')
    zero_shot_classifier = ZeroShotClassifier(topic_id_value_map, topic_id_content)
    # print('Run classify...')
    zero_shot_classifier.run_classify(path_to_save=path_to_save)
    # print('finish Run classify...!!!!!!!!!!!!!!!!!!')

    # calculate cohesion
    # print('calculate cohesion...')
    return main_calculate_cohesion(path=path_to_save + '.csv')
