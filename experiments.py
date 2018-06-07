from pipeline import new_experiment, continue_experiment
from configuration import Configuration


def first_tests():
    conf1 = Configuration()
    conf1.input_set = "wikipedia_chunks"
    new_experiment(conf1)


first_tests()
