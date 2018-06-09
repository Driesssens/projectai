import subprocess
import shutil
import datetime
import os

directory = os.path.dirname(__file__)


def relative_path(parts):
    return os.path.join(*parts)


def path(parts):
    return os.path.join(directory, relative_path(parts))


def header_name(the_task):
    return 'trainHeaderFiltered_{}{}.arff'.format(the_task, celex)


def header_path(the_task):
    return ['models', header_name(the_task)]


crfpp_install_dir = ['resources', 'CRF++-0.58']
pretrained_system_dir = ['resources', 'pretrained_system']
feature_extraction_jar_path = pretrained_system_dir + ['jars', 'de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-featureExtraction.jar']
arff_compatible_jar_path = pretrained_system_dir + ['jars', 'de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-arffCompatible.jar']
experimenter_jar_path = pretrained_system_dir + ['jars', 'de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-experimenter.jar']
collect_predictions_jar_path = pretrained_system_dir + ['jars', 'de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-collectPredictions.jar']
xml_writer_jar_path = pretrained_system_dir + ['jars', 'de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-xmlWriter.jar']

configs_dir = pretrained_system_dir + ['models', 'configs']
countability_path = pretrained_system_dir + ['resources', 'countability', 'webcelex_countabilityNouns.txt']
wordnet_dir = pretrained_system_dir + ['resources', 'wordnet3.0']
# input_dir = pretrained_system_dir + ['sample_data', 'raw_text']
gold_standard_dir = pretrained_system_dir + ['sample_data', 'gold_standard']

celex = "_webCelex"
lang = "en_US.utf8"
stamp = '{date:%Y-%m-%d_%H-%M-%S}'.format(date=datetime.datetime.now())


def run_labeler(input_folder, output_folder):
    def predictions_path(the_task):
        return output_folder + [the_task, 'crfpp', 'predictions.csv']

    xmi_output_folder = output_folder + ['temp', 'processed_xmi']
    xmi_output_final_folder = output_folder + ['temp', 'processed_xmi_final']
    arff_folder = output_folder + ['temp', 'processed_arff']
    arff_compatible_folder = output_folder + ['temp', 'processed_arff_compatible']
    xml_output_folder = output_folder + ['labeled_text']

    # Your text data (in raw text format)
    # (The sample data are some texts from our held-out test set.)
    # ! cp models/configs/* experiment_folder
    # SKIP FOR NOW - MANUALLY PLACE IN /sample_data

    # tasks = ["class_sitent_type", "class_main_referent", "class_habituality", "class_aspectual_class"]
    tasks = ["class_sitent_type"]

    task = "class_sitent_type"

    # ! java -jar jars/de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-featureExtraction.jar -input $INPUT -output $XMI_OUTPUT -countability $COUNTABILITY_PATH -arff $ARFF -task $TASK

    subprocess.call(["java",
                     "-jar", path(feature_extraction_jar_path),
                     "-input", relative_path(input_folder),
                     "-output", relative_path(xmi_output_folder),
                     # "-annotations", relative_path(gold_standard_dir),
                     "-countability", relative_path(countability_path),
                     "-arff", relative_path(arff_folder),
                     "-task", task])

    # copy XMI
    # ! mkdir output_xmi_final
    # ! cp -rf xmi_output + "/*" output_xmi_final

    shutil.copytree(path(xmi_output_folder), path(xmi_output_final_folder))

    for task in tasks:
        print task
        experiment_config = "config_{}.xml".format(task)
        # ! cp experiment_config $EXPERIMENT_FOLDER/
        shutil.copyfile(path(configs_dir + [experiment_config]), path(output_folder + [experiment_config]))

        predicted_feature_name = "predicted_{}".format(task)
        # print model
        print predicted_feature_name

        # Step 2: make the ARFF files compatible so Weka can process them
        # (copy the ARFF file containing the header for the training data to the ARFF directory)

        # ! cp models/trainHeaderFiltered_$TASK$CELEX.arff $ARFF/
        shutil.copyfile(path(header_path(task)), path(arff_folder + [header_name(task)]))

        # ! java -jar jars/de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-arffCompatible.jar -input $ARFF -output $ARFF"_compatible" -sparse -classAttribute $TASK
        subprocess.call(["java",
                         "-jar", path(arff_compatible_jar_path),
                         "-input", relative_path(arff_folder),
                         "-output", relative_path(arff_compatible_folder),
                         "-sparse",
                         "-classAttribute", task])

        print "TASK 2 DONE!!!!!"

        # ! rm $ARFF/trainHeaderFiltered_$TASK$CELEX.arff
        # ! rm $ARFF"_compatible"/trainHeaderFiltered_$TASK$CELEX.arff
        # SKIP THIS FOR NOW - NOT SURE IF NECESSARY?

        # Step 3: run system: filter text data according to configured features, classify instances.
        # ! 	java -jar jars/de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-experimenter.jar $EXPERIMENT_FOLDER/$EXPERIMENT_CONFIG $CRFPP_INSTALL_DIR $TASK $MODEL models/trainHeaderFiltered_$TASK$CELEX.arff
        subprocess.call(["java",
                         "-jar", path(experimenter_jar_path),
                         relative_path(output_folder + [experiment_config]),  # $EXPERIMENT_FOLDER/$EXPERIMENT_CONFIG
                         relative_path(crfpp_install_dir),  # $CRFPP_INSTALL_DIR
                         task,  # $TASK
                         "",  # $MODEL
                         relative_path(header_path(task))  # models/trainHeaderFiltered_$TASK$CELEX.arff
                         ])
        print "END OF TASK 3!!!!!"

        # Step 4: add predictions to XMI
        # ! java - jar jars/de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-collectPredictions.jar -input $OUTPUT_XMI_FINAL -outputXmi $OUTPUT_XMI_FINAL -featureName $PREDICTED_FEATURE_NAME -predictions $EXPERIMENT_FOLDER/$TASK/crfpp/predictions.csv
        subprocess.call(["java",
                         "-jar", path(collect_predictions_jar_path),
                         "-input", relative_path(xmi_output_final_folder),
                         "-outputXmi", relative_path(xmi_output_final_folder),
                         "-featureName", predicted_feature_name,
                         "-predictions", relative_path(predictions_path(task)),
                         ])

    # Step 4: output in XML format (XMI with predictions can be found at  ..)
    # ! echo "Writing XML files ..."
    # ! mkdir $XML_OUTPUT
    # ! java -jar jars/de.uni-saarland.coli.sitent-0.0.1-SNAPSHOT-xmlWriter.jar -input $OUTPUT_XMI_FINAL -output $XML_OUTPUT
    print "Writing XML files..."
    os.makedirs(path(xml_output_folder))
    subprocess.call(["java",
                     "-jar", path(xml_writer_jar_path),
                     "-input", relative_path(xmi_output_final_folder),
                     "-output", relative_path(xml_output_folder),
                     ])
