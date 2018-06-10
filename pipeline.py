from datetime import datetime
from configuration import Configuration
import os
from file_backlog import FileBacklog


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


def count_messy(files, output_folder, configuration):
    pass


def decorate_clean(the_file, output_folder, configuration):
    open(output_folder + '/decorated' + "/{}.json".format(the_file), 'w+')
    pass


def label_clean(files, output_folder, configuration):
    pass


def count_clean(output_folder, configuration):
    pass
