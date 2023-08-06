from relatedFunctions import extract_topics_labels, calculate_cohesion_score
from utils import read_data_from_csv, create_topic_names_using_tf_idf

correlation_dict = {}
error_precentage = []
total_for_print, nmi_score_list, coherence_score_list, cohesion_score_list = {}, {}, {}, {}
passed, failed = 0, 0


def cohesion_score(path):
    ground_truth_list, ground_truth_label_list = read_data_from_csv(path_to_csv=path)
    print('----------- Starting main pipeline -------------')
    print('There are {} docs in path_to_csv the dataset'.format(len(ground_truth_label_list)))
    topics, _, _ = create_topic_names_using_tf_idf(ground_truth_list, ground_truth_label_list)
    topics_names = extract_topics_labels(topics.values())
    cohesion_score = calculate_cohesion_score(ground_truth_list=ground_truth_list, topics=ground_truth_label_list,
                                              topics_names=topics_names)
    return cohesion_score, topics_names


def add_one(num: int):
    return num + 1
