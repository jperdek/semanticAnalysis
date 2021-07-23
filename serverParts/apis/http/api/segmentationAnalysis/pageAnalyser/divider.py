import os
import shutil
import random


def divide_dataset_in_ration(path_to_files, path_to_division, percent_to_train, separator="/"):
    category_dir = path_to_files.split(separator)[-1]
    new_category_dir = os.path.join(path_to_division, category_dir)
    # CREATES BASE DIR
    if not os.path.exists(new_category_dir):
        os.mkdir(new_category_dir)
    # FOR EACH ASSOCIATED DATASET TO BASE CATEGORY
    for directory in os.listdir(path_to_files):
        actual_processed_dir = os.path.join(path_to_files, directory)
        if os.path.isdir(actual_processed_dir):
            specific_set = os.path.join(new_category_dir, directory.split(separator)[-1])
            test_set = os.path.join(specific_set, "test")
            train_set = os.path.join(specific_set, "train")

            # CREATES MAIN FOLDER AND TEST AND TRAIN FOLDERS INSIDE IF NOT EXISTS
            if not os.path.exists(specific_set):
                os.mkdir(specific_set)
            if not os.path.exists(train_set):
                os.mkdir(train_set)
            if not os.path.exists(test_set):
                os.mkdir(test_set)

            files = [file for file in os.listdir(actual_processed_dir) if os.path.isfile(os.path.join(
                actual_processed_dir, file))]
            number_train = int((len(files) / 100.0) * percent_to_train)
            number_test = len(files) - number_train

            print("Number to test:" + str(number_test))
            print("Number to train: " + str(number_train))

            # shuffle files to randomize dicision
            random.shuffle(files)
            # COPY OF TRAIN FILES
            for i in range(0, number_train):
                shutil.copyfile(os.path.join(actual_processed_dir, files[i]), os.path.join(train_set, files[i]))
            # COPY OF TEST FILES
            for i in range(number_train, number_train + number_test):
                shutil.copyfile(os.path.join(actual_processed_dir, files[i]), os.path.join(test_set, files[i]))


def divide_dataset_in_ration_write_to_file(path_to_files, path_to_division, percent_to_train, train_info_file,
                                           test_info_file, separator="\\", write_string="a"):
    category_dir = path_to_files.split(separator)[-1]
    new_category_dir = os.path.join(path_to_division, category_dir)
    # CREATES BASE DIR
    if not os.path.exists(new_category_dir):
        os.mkdir(new_category_dir)
    with open(train_info_file, write_string, encoding="utf-8") as train_file:
        with open(test_info_file,  write_string, encoding="utf-8") as test_file:
            # FOR EACH ASSOCIATED DATASET TO BASE CATEGORY
            for directory in os.listdir(path_to_files):
                actual_processed_dir = os.path.join(path_to_files, directory)
                if os.path.isdir(actual_processed_dir):
                    specific_set = os.path.join(new_category_dir, directory.split(separator)[-1])
                    test_set = os.path.join(specific_set, "test")
                    train_set = os.path.join(specific_set, "train")

                    # CREATES MAIN FOLDER AND TEST AND TRAIN FOLDERS INSIDE IF NOT EXISTS
                    if not os.path.exists(specific_set):
                        os.mkdir(specific_set)
                    if not os.path.exists(train_set):
                        os.mkdir(train_set)
                    if not os.path.exists(test_set):
                        os.mkdir(test_set)

                    files = [file for file in os.listdir(actual_processed_dir) if os.path.isfile(os.path.join(
                        actual_processed_dir, file))]
                    number_train = int((len(files) / 100.0) * percent_to_train)
                    number_test = len(files) - number_train

                    print("Number to test:" + str(number_test))
                    print("Number to train: " + str(number_train))

                    # shuffle files to randomize dicision
                    random.shuffle(files)
                    # COPY OF TRAIN FILES
                    for i in range(0, number_train):
                        shutil.copyfile(os.path.join(actual_processed_dir, files[i]), os.path.join(train_set, files[i]))
                        train_file.write(os.path.join(train_set, files[i]) + "\t" + category_dir + "\n")
                    # COPY OF TEST FILES
                    for i in range(number_train, number_train + number_test):
                        shutil.copyfile(os.path.join(actual_processed_dir, files[i]), os.path.join(test_set, files[i]))
                        test_file.write(os.path.join(test_set, files[i]) + '\t' + category_dir + "\n")


def divide_dataset():
    divide_dataset_in_ration("d://dipldatasets/weir/dataset/videogame", "d://dipldatasets/divided", 80)
    divide_dataset_in_ration("d://dipldatasets/weir/dataset/soccer", "d://dipldatasets/divided", 80)
    divide_dataset_in_ration("d://dipldatasets/weir/dataset/finance", "d://dipldatasets/divided", 80)
    divide_dataset_in_ration("d://dipldatasets/weir/dataset/book", "d://dipldatasets/divided", 80)


def divide_dataset_and_prepare_list():
    divide_dataset_in_ration_write_to_file("d:\\dipldatasets\\weir\\dataset\\videogame", "d:\\dipldatasets\\divided",
                                           80, "../../../../../../output/pageAnalyser/train.tsv", "../output/pageAnalyser/test.tsv",
                                           write_string="w"
                                           )
    divide_dataset_in_ration_write_to_file("d:\\dipldatasets\\weir\\dataset\\soccer", "d:\\dipldatasets\\divided",
                                           80, "../../../../../../output/pageAnalyser/train.tsv", "../output/pageAnalyser/test.tsv")
    divide_dataset_in_ration_write_to_file("d:\\dipldatasets\\weir\\dataset\\finance", "d:\\dipldatasets\\divided",
                                           80, "../../../../../../output/pageAnalyser/train.tsv", "../output/pageAnalyser/test.tsv")
    divide_dataset_in_ration_write_to_file("d:\\dipldatasets\\weir\\dataset\\book", "d:\\dipldatasets\\divided",
                                           80, "../../../../../../output/pageAnalyser/train.tsv", "../output/pageAnalyser/test.tsv")


if __name__ == "__main__":
    divide_dataset_and_prepare_list()
