from datetime import datetime
from configuration import Configuration
import os
import io
from file_backlog import FileBacklog
from collections import Counter
from itertools import combinations
from math import log
from scipy.sparse import csc_matrix
from pprint import pformat
from scipy.sparse.linalg import svds
import numpy as np
from functools import partial
from file_backlog import name
import spacy
import xml.etree.ElementTree as xml
from spacy import symbols


def new_experiment(configuration):
    starting_time = datetime.now()
    experiment_name = "{}_{}".format(starting_time.strftime('%Y%m%d%H%M%S'), configuration.input_set)
    output_folder = 'output/{}'.format(experiment_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    configuration.store(output_folder)

    continue_experiment(experiment_name, configuration)


def continue_experiment(experiment_name, configuration=None):
    output_folder = 'output/{}'.format(experiment_name)

    if configuration is None:
        configuration = Configuration.from_json(output_folder)

    if configuration.style == Configuration.CLEAN:
        clean_experiment(experiment_name, configuration)
    elif configuration.style == Configuration.MESSY:
        messy_experiment(experiment_name, configuration)


def messy_experiment(experiment_name, configuration):
    output_folder = 'output/{}'.format(experiment_name)

    # if not os.path.exists(output_folder + "/matrices"):
    #     if not os.path.exists(output_folder + "/labeled"):
    #         os.makedirs(output_folder + "/labeled")
    #
    #     files = FileBacklog(output_folder + "/labeled", configuration).backlog
    #     label_messy(files, output_folder, configuration)

    if not os.path.exists(output_folder + "/done"):
        count_messy(output_folder, configuration)

    open(output_folder + '/done', 'w+')


def clean_experiment(experiment_name, configuration):
    output_folder = 'output/{}'.format(experiment_name)

    if not os.path.exists(output_folder + "/labeled"):
        if not os.path.exists(output_folder + "/decorated"):
            os.makedirs(output_folder + "/decorated")

        for the_file in FileBacklog(output_folder + "/decorated", configuration):
            decorate_clean(the_file, output_folder, configuration)

    if not os.path.exists(output_folder + "/matrices"):
        if not os.path.exists(output_folder + "/labeled"):
            os.makedirs(output_folder + "/labeled")

        files = FileBacklog(output_folder + "/labeled", configuration).backlog
        label_clean(files, output_folder, configuration)

    if not os.path.exists(output_folder + "/done"):
        count_clean(output_folder, configuration)

    open(output_folder + '/done', 'w+')


def label_messy(files, output_folder, configuration):
    pass


def is_nsubj(word):
    if word.dep_ == symbols.root:
        return False
    elif word.dep == symbols.nsubj:
        return True
    else:
        return is_nsubj(word.head)


def count_messy(output_folder, configuration):
    full_unigram = Counter()
    full_bigram = Counter()
    weak_generic_unigram = Counter()
    weak_generic_bigram = Counter()
    weak_noun_unigram = Counter()
    weak_noun_bigram = Counter()
    strong_generic_unigram = Counter()
    strong_generic_bigram = Counter()
    strong_noun_unigram = Counter()
    strong_noun_bigram = Counter()

    nlp = spacy.load('en_core_web_sm')

    for file_name in map(name, os.listdir('input/{}'.format(configuration.input_set))):
        with io.open('input/{}/{}.txt'.format(configuration.input_set, file_name), encoding='utf-8') as txt_file:
            document = nlp(txt_file.read())
            for sentence in document.sents:
                for word in sentence:
                    full_unigram[word.lemma_] += 1
                    for other in sentence:
                        if word is not other:
                            full_bigram[(word.lemma_, other.lemma_)] += 1

                xml_root = xml.parse('messy_labeled/{}/{}.xml'.format(configuration.input_set, file_name)).getroot()

                labels = [child[-1].attrib['seType'] for child in xml_root if (int(child.attrib['begin']) >= sentence.start_char) and (int(child.attrib['end']) <= sentence.end_char)]

                if 'GENERIC_SENTENCE' in labels:
                    set_of_labels = set(labels)
                    only_generic = len(set_of_labels) == 1 and set_of_labels.pop() == 'GENERIC_SENTENCE'

                    for word in sentence:
                        is_nsubj_indeed = is_nsubj(word)

                        weak_generic_unigram[word.lemma_] += 1

                        if is_nsubj_indeed:
                            weak_noun_unigram[word.lemma_] += 1

                        for other in sentence:
                            if word is not other:
                                weak_generic_bigram[(word.lemma_, other.lemma_)] += 1

                                if is_nsubj_indeed:
                                    weak_noun_bigram[(word.lemma_, other.lemma_)] += 1

                        if only_generic:
                            strong_generic_unigram[word.lemma_] += 1

                            if is_nsubj_indeed:
                                strong_noun_unigram[word.lemma_] += 1

                            for other in sentence:
                                if word is not other:
                                    strong_generic_bigram[(word.lemma_, other.lemma_)] += 1

                                    if is_nsubj_indeed:
                                        strong_noun_bigram[(word.lemma_, other.lemma_)] += 1


def decorate_clean(the_file, output_folder, configuration):
    open(output_folder + '/decorated' + "/{}.json".format(the_file), 'w+')
    pass


def label_clean(files, output_folder, configuration):
    pass


def count_clean(output_folder, configuration):
    pass
