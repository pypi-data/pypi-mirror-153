import pandas as pd
from transformers import pipeline
import numpy as np
import random


class ZeroShotClassifier:
    def __init__(self, path_dic_topic_id_to_name, path_df_docs_topics):
        self.model_name = "digitalepidemiologylab/covid-twitter-bert-v2-mnli"
        self.model_name_saveable = "covid-twitter-bert-v2-mnli"
        self.df_docs_topics = pd.read_pickle(path_df_docs_topics)
        self.dic_topic_id_to_name = topic_ind_to_name_pkl_to_dict(path_dic_topic_id_to_name)
        self.classifier = pipeline("zero-shot-classification", model=self.model_name)
        self.docs, self.series_topics = self.get_topics_and_docs_filtered()

    def get_topics_and_docs_filtered(self):
        """
        drops docs that their topic id is not defined in dic_topic_id_to_name
        series topics is topic name for every doc that pass the filter
        returns docs and topics
        """
        series_topics = self.df_docs_topics["topic_ind"].apply(
            lambda x: self.dic_topic_id_to_name.get(x, np.nan)).dropna()
        docs = self.df_docs_topics["content"][series_topics.index].to_list()
        return docs, series_topics

    def zero_shot_to_every_doc_and_every_topic(self, docs, topics, indexes_to_test):
        results = []
        # docs = docs[:4] for test - short the process
        for i, doc in enumerate(docs):
            # print("REAL DOC INDEX =", indexes_to_test[i])
            doc_topics_result = self.classifier(doc, topics, multi_label=True)
            # print(doc_topics_result)
            results.append(doc_topics_result)
        return results

    def get_topics_values_by_names(self, indexes_to_test):
        topic_name_by_doc_ind = self.series_topics.reset_index()
        indexes_real_topic = []
        for ind in indexes_to_test:
            indexes_real_topic.append(
                list(self.dic_topic_id_to_name.values()).index(topic_name_by_doc_ind.loc[ind, "topic_ind"]))
        return indexes_real_topic

    def zero_shot_to_every_doc_and_random_topics(self, docs, topics, indexes_real_topic):
        results = []
        for i, doc in enumerate(docs):
            selected_topics = []
            selected_topics_ind = list(
                set(random.sample(range(len(topics)), int(len(topics) * 0.1))))  # int(len(topics) * 0.2))))
            selected_topics_ind.append(indexes_real_topic[i])
            for top_ind in selected_topics_ind:
                selected_topics.append(topics[top_ind])
            doc_topics_result = self.classifier(doc, selected_topics, multi_label=True)
            # print(doc_topics_result)
            results.append(doc_topics_result)
        return results

    def run_classify(self, path_to_save):
        """
        the function check each document with the other exist topics and save the similarities into csv.
        """
        topics_by_doc = self.series_topics.to_list()  # topic id for every doc
        topic_names = list(self.dic_topic_id_to_name.values())
        # TODO: eden change indexes to test to real doc index
        num_of_docs = len(self.docs)
        print('num_of_docs: ', num_of_docs)
        indexes_to_test_before_validation = [i for i in range(0, num_of_docs, 1)]
        docs_sample = []
        indexes_to_test = []
        for ind in indexes_to_test_before_validation:
            # TODO: remove if use only short documents
            if 500 > len(self.docs[ind].split()) > 3:
                docs_sample.append(self.docs[ind])
                indexes_to_test.append(ind)
        indexes_real_topic = self.get_topics_values_by_names(indexes_to_test)
        results = self.zero_shot_to_every_doc_and_random_topics(docs_sample, topic_names, indexes_real_topic)
        # results = self.zero_shot_to_every_doc_and_every_topic(docs_sample, topic_names, indexes_to_test)
        topic_names_with_ind = [str(i) + "_" + topic_name for i, topic_name in enumerate(topic_names)]
        df = pd.DataFrame(columns=["doc_num", "doc", "real_topic"] + topic_names_with_ind)
        for i, result in enumerate(results):
            real_doc_ind = indexes_to_test[i]
            doc_labels = result["labels"]
            doc_scores = result["scores"]
            doc_dict = {"doc_num": real_doc_ind, "doc": result["sequence"], "real_topic": topics_by_doc[real_doc_ind]}
            for topic_i, spec_topic in enumerate(self.dic_topic_id_to_name.values()):
                if spec_topic in doc_labels:
                    index_of_spec_topic = doc_labels.index(spec_topic)
                    score_spec_topic = doc_scores[index_of_spec_topic]
                    doc_dict[str(topic_i) + "_" + spec_topic] = score_spec_topic
                else:
                    doc_dict[str(topic_i) + "_" + spec_topic] = 0
            df = df.append(doc_dict, ignore_index=True)
        self.save_mnli_scores(df, path_to_save)

    def save_mnli_scores(self, df, path):
        df.to_pickle(path + ".pkl", protocol=4)
        df.to_csv(path + ".csv")


def topic_ind_to_name_pkl_to_dict(path):
    df_temp = pd.read_pickle(path)
    df_temp = df_temp[df_temp['topic_ind'] != -1]  # drops unassigned docs
    return dict(zip(df_temp["topic_ind"].to_list(), df_temp["topic_name"].to_list()))