#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import nltk
import re
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from matplotlib import gridspec
import seaborn as sns
from collections import OrderedDict


def load_json_data(filename):
    with open(filename, 'r') as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def load_text_data(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def preprocessing(text):
    stemmer = nltk.stem.porter.PorterStemmer()
    text_list = re.findall(
        r"[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", text)    # tokenize
    text_list = [t.lower() for t in text_list]  # transfer to lowercase
    text_list = [stemmer.stem(item) for item in text_list]    # stem
    return text_list


def plot_tfidf_distribution(tfidf_matrix, feature, title):
    top_n_annotate = 5
    n, d = tfidf_matrix.shape
    fig = plt.figure(figsize=(30, 50))
    #max_index = np.argmax(tfidf_matrix,1)
    max_index = np.argsort(-tfidf_matrix, 1)

    for index in range(n):
        ax = fig.add_subplot(10, 4, index + 1)

        # annotate top 5 words
        for i in range(top_n_annotate):
            max_feature_index = max_index[index, i]
            ax.annotate(feature[max_feature_index], xy=(
                max_feature_index, tfidf_matrix[index, max_feature_index]), color='blue')
        ax.plot(tfidf_matrix[index, :], color='black', alpha=0.5)
        ax.set_title(title[index], fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xticks([])
    plt.show()


def plot_tfidf_distribution_seperate(tfidf_matrix, feature, title):
    plot_number = [4, 6, 5, 4, 4, 3, 5, 3, 6]
    size_list = [16, 16, 15, 14, 13] # fontsize for top frequent words
    top_n_annotate = 5
    color_list = sns.dark_palette("navy", reverse=False)
    max_index = np.argsort(-tfidf_matrix, 1)

    for idx, p in enumerate(plot_number):
        plt.figure(figsize=(12, int(round(p / 2.0)) * 3))
        gs = gridspec.GridSpec(int(round(p / 2.0)), 2)
        star_idx = sum(plot_number[0:idx])
        end_idx = sum(plot_number[0:idx + 1])

        plot_idx = 0
        for index in range(star_idx, end_idx):
            ax = plt.subplot(gs[plot_idx])
            plot_idx += 1
            for i in range(top_n_annotate):    # annotate top 5 words
                max_feature_index = max_index[index, i]
                ax.annotate(feature[max_feature_index], xy=(max_feature_index,
                            tfidf_matrix[index, max_feature_index]), color=color_list[i],
                            fontsize=size_list[i], alpha=0.8)
            ax.plot(tfidf_matrix[index, :], color='black', alpha=0.5)
            ax.set_title(title[index], fontsize=14)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_xticks([])
            ax.yaxis.set_ticks_position('left')

        plt.tick_params(
            axis='y',
            which='both',
            left='on',
            right='off'
        )
        plt.savefig('Figure/dist_%s.png' % str(idx))


if __name__ == '__main__':
    train_data = load_json_data("Data/job_description_level2.json")  # dict
    occupation_titles = train_data.keys()
    train_id = train_data.keys()
    vectorizer = TfidfVectorizer(tokenizer=preprocessing, stop_words='english')
    train_tfidf = vectorizer.fit_transform(train_data.values())
    feature_names = vectorizer.get_feature_names()

    plot_tfidf_distribution_seperate(train_tfidf.A, feature_names, occupation_titles)
