from pipeline import new_experiment, continue_experiment
from configuration import Configuration
from labeler import run_labeler


def first_tests():
    conf1 = Configuration()
    conf1.input_set = "wikipedia_chunks"
    new_experiment(conf1)


def test_labeler():
    run_labeler(input_folder=["input/only_blobfish"], output_folder=["output/testing_this_bitch"])


test_labeler()
