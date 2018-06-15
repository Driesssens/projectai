from pipeline import new_experiment, continue_experiment
from configuration import Configuration
from labeler import run_labeler, run_labeler_2
import os


def first_tests():
    conf1 = Configuration()
    conf1.input_set = "wikipedia_chunks"
    new_experiment(conf1)


def test_labeler():
    run_labeler(input_folder=["input/only_blobfish"], output_folder=["output/testing_this_bitch"])


def big_run():
    for i in range(0, 19):
        run_labeler(input_folder=["input/csn_chopped_stripped/csn{}".format(i)], output_folder=["output/csn_chopped_stripped/csn{}".format(i)])


def big_run_2():
    for i in range(0, 19):
        run_labeler_2(input_folder=["input/csn_chopped/csn{}".format(i)], output_folder=["output/csn_chopped/csn{}".format(i)])


def remove_bars():
    for i in range(0, 19):
        folder_name = "input/csn_chopped_stripped/csn{}".format(i)
        for file_name in os.listdir(folder_name):
            with open(folder_name + '/' + file_name, "r+") as open_file:
                text = open_file.read().replace("_", " ")
                open_file.seek(0)
                open_file.write(text)


def remove_quotes():
    for i in range(0, 19):
        folder_name = "output/csn_chopped/csn{}/temp/processed_arff_compatible".format(i)
        for file_name in os.listdir(folder_name):
            with open(folder_name + '/' + file_name, "r+") as open_file:
                text = open_file.read().replace(',QUOTE}', ',"hoidoeikoehahahaha"}')
                open_file.seek(0)
                open_file.write(text)


big_run_2()
