from pipeline import new_experiment, continue_experiment
from configuration import Configuration
from labeler import run_labeler


def first_tests():
    conf1 = Configuration()
    conf1.input_set = "wikipedia_chunks"
    new_experiment(conf1)


def test_labeler():
    run_labeler(input_folder=["input/only_blobfish"], output_folder=["output/testing_this_bitch"])


def big_run():
    for i in range(0, 19):
        run_labeler(input_folder=["input/csn_chopped/csn{}".format(i)], output_folder=["output/csn_chopped/csn{}".format(i)])


big_run()
