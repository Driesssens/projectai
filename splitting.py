import os
from functools import partial


# Quick files were 40 kb over 8 files, so ~5 kb per file, so ~4800 characters

def get_file_name(path):
    return os.path.splitext(os.path.basename(path))[0]


def split_all_on(input_folder, output_folder, splitter):
    for file_name in os.listdir(input_folder):
        splitter(input_file="{}/{}".format(input_folder, file_name), output_folder=output_folder)


def split_on_lines(input_file, output_folder, lines_per_file):
    smallfile = None
    number = 0

    file_name = get_file_name(input_file)

    with open(input_file) as big_file:
        for lineno, line in enumerate(big_file):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                number += 1
                small_filename = '{}/{}_{}.txt'.format(output_folder, file_name, number)
                smallfile = open(small_filename, "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()


def split_on_characters(input_file, output_folder, characters_per_file):
    number = 0
    file_name = get_file_name(input_file)
    previous_batch = []
    current_batch = []

    with open(input_file) as big_file:
        for line in big_file:
            current_batch.append(line)

            if line in ['\n', '\r\n']:
                if sum([len(st) for st in current_batch]) >= characters_per_file:
                    if previous_batch:
                        number += 1
                        small_file_name = '{}/{}_{}.txt'.format(output_folder, file_name, number)
                        with open(small_file_name, "w") as small_file:
                            for write_line in previous_batch:
                                small_file.write(write_line)

                    previous_batch = current_batch
                    current_batch = []

        if sum([len(st) for st in current_batch]) < 0.25 * characters_per_file:
            previous_batch += current_batch
        else:
            small_file_name = '{}/{}_{}.txt'.format(output_folder, file_name, number + 2)
            with open(small_file_name, "w") as small_file:
                for write_line in current_batch:
                    small_file.write(write_line)

        small_file_name = '{}/{}_{}.txt'.format(output_folder, file_name, number + 1)
        with open(small_file_name, "w") as small_file:
            for write_line in previous_batch:
                small_file.write(write_line)


def split_all_on_lines(input_folder, output_folder, lines_per_file):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    split_all_on(input_folder, output_folder, partial(split_on_lines, lines_per_file=lines_per_file))


def split_all_on_characters(input_folder, output_folder, characters_per_file):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    split_all_on(input_folder, output_folder, partial(split_on_characters, characters_per_file=characters_per_file))


# split_all_on_lines("input/sitent_raw_texts", "input/sitent_raw_texts_split_4", 4)
split_all_on_characters("input/children_science_nature_only_content", "input/children_science_nature_4000", 4000)
