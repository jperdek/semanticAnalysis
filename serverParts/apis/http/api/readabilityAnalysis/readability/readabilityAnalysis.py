
from nltk.tokenize import sent_tokenize
from readability import Readability
from readability.exceptions import ReadabilityException
import json


def check_readability_nltk(text):
    sentences = sent_tokenize(text)
    print(len(sentences))


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def readability_analysis_weir():
    ReadabilityAnalyser.check_readability_from_file("d:\\dipldatasets\\weir\\output_beautifulsoap_processed.json",
                                                    "d:\\dipldatasets\\weir\\weir_beutif_readability.json")
    print('here')
    ReadabilityAnalyser.check_readability_from_file("../../../../../../output/pageAnalyser/CETD/extractor.json",
                                                    "d:\\dipldatasets\\weir\\weir_extractor_readability.json")
    ReadabilityAnalyser.check_readability_from_file("../../../../../../output/pageAnalyser/CETD/edgareExtractor.json",
                                                    "d:\\dipldatasets\\weir\\weir_edgareExtractor_readability.json")
    ReadabilityAnalyser.check_readability_from_file("../../../../../../output/pageAnalyser/CETD/variantExtractor.json",
                                                    "d:\\dipldatasets\\weir\\weir_variantExtractor_readability.json")
    ReadabilityAnalyser.check_readability_from_file("../../../../../../output/pageAnalyser/plain_text.json",
                                                    "d:\\dipldatasets\\weir\\plain_text_readability.json")


def readability_statistics_from_analysis_weir():
    analyser = ReadabilityAnalyser("")
    categories = ['book', 'soccer', 'finance', 'videogame']
    ReadabilityAnalyser.analyse_readability_file_save_results(analyser, "d:\\dipldatasets\\weir\\weir_beutif_"
                                                                        "readability.json",
                                                              "d:\\dipldatasets\\weir\\weir_beutif_readability_"
                                                              "statistics.json", categories)
    print('here')
    ReadabilityAnalyser.analyse_readability_file_save_results(analyser, "d:\\dipldatasets\\weir\\weir_extractor_"
                                                                        "readability.json",
                                                              "d:\\dipldatasets\\weir\\weir_extractor_readability_"
                                                              "statistics.json", categories)
    ReadabilityAnalyser.analyse_readability_file_save_results(analyser, "d:\\dipldatasets\\weir\\weir_edgareExtractor_"
                                                                        "readability.json",
                                                              "d:\\dipldatasets\\weir\\weir_edgareExtractor_readabil"
                                                              "ity_statistics.json", categories)
    ReadabilityAnalyser.analyse_readability_file_save_results(analyser, "d:\\dipldatasets\\weir\\weir_variantExtractor_"
                                                                        "readability.json",
                                                              "d:\\dipldatasets\\weir\\weir_variantExtractor_readabili"
                                                              "ty_statistics.json", categories)
    ReadabilityAnalyser.analyse_readability_file_save_results(analyser, "d:\\dipldatasets\\weir\\plain_text_"
                                                                        "readability.json",
                                                              "d:\\dipldatasets\\weir\\plain_text_readability_"
                                                              "statistics.json", categories)


class ReadabilityAnalyser:

    def __init__(self, text):
        self.readability = Readability(text)
        self.FLESCH_KINCAID = ['score', 'grade_level']
        self.FLESCH_EASE = ['score', 'ease', 'grade_level']
        self.DALE_CHALL = ['score', 'grade_level']
        self.ARI = ['score', 'grade_level', 'ages']
        self.CLI = ['score', 'grade_level']
        self.GUNNING_FOG = ['score', 'grade_level']
        self.SMOG = ['score', 'grade_level']
        self.SPACHE = ['score', 'grade_level']
        self.LINSEAR_WRITE = ['score', 'grade_level']
        self.values_index = self.initialize_value_index_array()

    def initialize_value_index_array(self):
        values_index = dict()
        values_index["flesch_kincaid"] = self.FLESCH_KINCAID
        values_index["flesch_ease"] = self.FLESCH_EASE
        values_index["dale_chall"] = self.DALE_CHALL
        values_index["ari"] = self.ARI
        values_index["cli"] = self.CLI
        values_index["gunning_fog"] = self.GUNNING_FOG
        values_index["smog_all"] = self.SMOG
        values_index["smog"] = self.SMOG
        values_index["spache"] = self.SPACHE
        values_index["linsear_write"] = self.LINSEAR_WRITE
        return values_index

    def flesch_kincaid(self, content, error_ignore=True):
        try:
            record = dict()
            fk = self.readability.flesch_kincaid()
            record['score'] = fk.score
            record['grade_level'] = fk.grade_level
            content["flesch_kincaid"] = record
        except ReadabilityException as e:
            if not error_ignore:
                content["flesch_kincaid"] = str(e)
                print(e)

    def flesch_ease(self, content, error_ignore=True):
        try:
            record = dict()
            flesch_ease = self.readability.flesch()
            record['score'] = flesch_ease.score
            record['ease'] = flesch_ease.ease
            record['grade_levels'] = flesch_ease.grade_levels
            content['flesch_ease'] = record
        except ReadabilityException as e:
            if not error_ignore:
                content['flesch_ease'] = str(e)
                print(e)

    def dale_chall(self, content, error_ignore=True):
        try:
            record = dict()
            dale_chall = self.readability.dale_chall()
            record['score'] = dale_chall.score
            record['grade_level'] = dale_chall.grade_levels
            content['dale_chall'] = record
        except ReadabilityException as e:
            if not error_ignore:
                content['dale_chall'] = str(e)
                print(e)

    def automated_readability_index(self, content, error_ignore=True):
        try:
            record = dict()
            ari = self.readability.ari()
            record['score'] = ari.score
            record['grade_level'] = ari.grade_levels
            record['ages'] = ari.ages
            content['ari'] = record
        except ReadabilityException as e:
            if not error_ignore:
                content['ari'] = str(e)
                print(e)

    def coleman_liau_index(self, content, error_ignore=True):
        try:
            record = dict()
            coleman_liau = self.readability.coleman_liau()
            record['score'] = coleman_liau.score
            record['grade_level'] = coleman_liau.grade_level
            content['cli'] = record
            print(record)
        except ReadabilityException as e:
            print(e)
            if not error_ignore:
                content['cli'] = str(e)
                print(e)

    def gunning_fog_index(self, content, error_ignore=True):
        try:
            record = dict()
            gunning_fog = self.readability.gunning_fog()
            record['score'] = gunning_fog.score
            record['grade_level'] = gunning_fog.grade_level
            content['gunning_fog'] = record
        except ReadabilityException as e:
            if not error_ignore:
                content['gunning_fog'] = str(e)
                print(e)

    def smog(self, content, all_sentences=False, error_ignore=True):
        record = dict()
        try:
            if all_sentences:
                smog = self.readability.smog(all_sentences=all_sentences)
                record['score'] = smog.score
                record['grade_level'] = smog.grade_level
                content['smog_all'] = record
            else:
                smog = self.readability.smog()
                record['score'] = smog.score
                record['grade_level'] = smog.grade_level
                content['smog'] = record
        except ReadabilityException as e:
            print(e)
            print(error_ignore)
            if not error_ignore:
                if all_sentences:
                    content['smog_all'] = str(e)
                else:
                    content['smog'] = str(e)
                print(e)

    def spache_readability_formula(self, content, error_ignore=True):
        try:
            record = dict()
            spache = self.readability.spache()
            record['score'] = spache.score
            record['grade_level'] = spache.grade_level
            content['spache'] = record
        except ReadabilityException as e:
            if not error_ignore:
                content['spache'] = str(e)
                print(e)

    def linsear_write(self, content, error_ignore=True):
        try:
            record = dict()
            linsear_write = self.readability.linsear_write()
            record['score'] = linsear_write.score
            record['grade_level'] = linsear_write.grade_level
            content['linsear_write'] = record
        except ReadabilityException as e:
            if not error_ignore:
                content['linsear_write'] = str(e)
                print(e)

    @staticmethod
    def check_readability_from_file(input_json_file, output_json_file):
        result = []
        json_file = load_as_json(input_json_file)
        for record in json_file:
            analyser = ReadabilityAnalyser(record['text'])
            analysed_file_record = dict()
            analysed_file_record['file'] = record['file']
            analysed_file_record['category'] = record['category']
            analyser.flesch_kincaid(analysed_file_record)
            analyser.flesch_ease(analysed_file_record)
            analyser.dale_chall(analysed_file_record)
            analyser.automated_readability_index(analysed_file_record)
            analyser.coleman_liau_index(analysed_file_record)
            analyser.gunning_fog_index(analysed_file_record)
            analyser.smog(analysed_file_record)
            analyser.smog(analysed_file_record, True)
            analyser.spache_readability_formula(analysed_file_record)
            analyser.linsear_write(analysed_file_record)
            result.append(analysed_file_record)
        save_as_json(result, output_json_file)

    def check_readability(self, use_methods=None, errors_included=True):
        result_analysis = dict()
        if use_methods is None or 'flesch_kincaid' in use_methods:
            self.flesch_kincaid(result_analysis, error_ignore=not errors_included)
        if use_methods is None or 'flesch_ease' in use_methods:
            self.flesch_ease(result_analysis, error_ignore=not errors_included)
        if use_methods is None or 'dale_chall' in use_methods:
            self.dale_chall(result_analysis, error_ignore=not errors_included)
        if use_methods is None or 'ari' in use_methods:
            self.automated_readability_index(result_analysis, error_ignore=not errors_included)
        if use_methods is None or 'cli' in use_methods:
            self.coleman_liau_index(result_analysis, error_ignore=not errors_included)
        if use_methods is None or 'gunning_fog' in use_methods:
            self.gunning_fog_index(result_analysis, error_ignore=not errors_included)
        if use_methods is None or 'smog' in use_methods:
            self.smog(result_analysis, error_ignore=not errors_included)
        if use_methods is None or 'smog_all' in use_methods:
            self.smog(result_analysis, True, error_ignore=not errors_included)
        if use_methods is None or 'spache' in use_methods:
            self.spache_readability_formula(result_analysis, error_ignore=not errors_included)
        if use_methods is None or 'linsear_write' in use_methods:
            self.linsear_write(result_analysis, error_ignore=not errors_included)
        return result_analysis

    @staticmethod
    def initialize_basic_dict(categories, values, process_category=True):
        record = dict()
        for value in values:
            record = ReadabilityAnalyser.initialize_dict(record, value)
        if process_category:
            for category in categories:
                record[category] = ReadabilityAnalyser.initialize_basic_dict(categories, values, False)
        return record

    @staticmethod
    def initialize_dict(record, value):
        record['min_' + value] = 999999999
        record['max_' + value] = -999999999
        record['sum_' + value] = 0
        record['avg_' + value] = 0
        record['freq_' + value] = 0
        record['skipped_' + value] = 0
        return record

    def initialize_values(self, statistic, categories):
        statistic["flesch_kincaid"] = self.initialize_basic_dict(categories, self.FLESCH_KINCAID)
        statistic["flesch_ease"] = self.initialize_basic_dict(categories, self.FLESCH_EASE)
        statistic["dale_chall"] = self.initialize_basic_dict(categories, self.DALE_CHALL)
        statistic["ari"] = self.initialize_basic_dict(categories, self.ARI)
        statistic["cli"] = self.initialize_basic_dict(categories, self.CLI)
        statistic["gunning_fog"] = self.initialize_basic_dict(categories, self.GUNNING_FOG)
        statistic["smog_all"] = self.initialize_basic_dict(categories, self.SMOG)
        statistic["smog"] = self.initialize_basic_dict(categories, self.SMOG)
        statistic["spache"] = self.initialize_basic_dict(categories, self.SPACHE)
        statistic["linsear_write"] = self.initialize_basic_dict(categories, self.LINSEAR_WRITE)
        statistic['indexes'] = ["flesch_kincaid", "flesch_ease", "dale_chall", "ari", "cli", "gunning_fog", "smog_all",
                                "smog", "spache", "linsear_write"]
        statistic['categories'] = categories

    @staticmethod
    def fill_min_max_sum_category(index, value_index, statistics, readability_index, category):
        if index[value_index] < statistics[readability_index][category]['min_' + value_index]:
            statistics[readability_index][category]['min_' + value_index] = index[value_index]
        if index[value_index] > statistics[readability_index][category]['max_' + value_index]:
            statistics[readability_index][category]['max_' + value_index] = index[value_index]
        statistics[readability_index][category]['sum_' + value_index] = \
            statistics[readability_index][category]['sum_' + value_index] + index[value_index]

    @staticmethod
    def fill_min_max_sum_category_value(value, value_index, statistics, readability_index, category):
        if value < statistics[readability_index][category]['min_' + value_index]:
            statistics[readability_index][category]['min_' + value_index] = value
        if value > statistics[readability_index][category]['max_' + value_index]:
            statistics[readability_index][category]['max_' + value_index] = value
        statistics[readability_index][category]['sum_' + value_index] = \
            statistics[readability_index][category]['sum_' + value_index] + value

    @staticmethod
    def fill_min_max_sum(index, value_index, statistics, readability_index):
        if index[value_index] < statistics[readability_index]['min_' + value_index]:
            statistics[readability_index]['min_' + value_index] = index[value_index]
        if index[value_index] > statistics[readability_index]['max_' + value_index]:
            statistics[readability_index]['max_' + value_index] = index[value_index]
        statistics[readability_index]['sum_' + value_index] = \
            statistics[readability_index]['sum_' + value_index] + index[value_index]

    @staticmethod
    def fill_min_max_sum_value(value, value_index, statistics, readability_index):
        if value < statistics[readability_index]['min_' + value_index]:
            statistics[readability_index]['min_' + value_index] = value
        if value > statistics[readability_index]['max_' + value_index]:
            statistics[readability_index]['max_' + value_index] = value
        statistics[readability_index]['sum_' + value_index] = \
            statistics[readability_index]['sum_' + value_index] + value

    @staticmethod
    def cast_to_float(value):
        try:
            return float(value)
        except ValueError:
            return None
        except TypeError:
            return None

    def record_analysis(self, record, statistics):
        for readability_index in statistics['indexes']:
            if 'category' in record:
                category = record['category']
                if readability_index in record:
                    index = record[readability_index]
                    for value_index in self.values_index[readability_index]:
                        if value_index in index:
                            obtained_value = ReadabilityAnalyser.cast_to_float(index[value_index])

                            if obtained_value is not None:
                                index[value_index] = obtained_value
                                ReadabilityAnalyser.fill_min_max_sum_category(index, value_index, statistics,
                                                                              readability_index, category)
                                if 'freq_' + value_index not in statistics[readability_index][category]:
                                    statistics[readability_index][category]['freq_' + value_index] = 0
                                statistics[readability_index][category]['freq_' + value_index] = \
                                    statistics[readability_index][category]['freq_' + value_index] + 1
                            elif isinstance(index[value_index], list):
                                for rec in index[value_index]:

                                    if value_index not in statistics[readability_index][category]:
                                        statistics[readability_index][category][value_index] = dict()
                                    if isinstance(rec, str):
                                        if 'freq_' + rec not in statistics[readability_index][category][value_index]:
                                            statistics[readability_index][category][value_index]['freq_' + rec] = 0
                                        statistics[readability_index][category][value_index]['freq_' + rec] = \
                                            statistics[readability_index][category][value_index]['freq_' + rec] + 1
                                    else:
                                        ReadabilityAnalyser.fill_min_max_sum_category_value(rec,
                                                                                            value_index, statistics,
                                                                                            readability_index,
                                                                                            category)
                                        if 'freq_' + value_index not in \
                                                statistics[readability_index][category][value_index]:
                                            statistics[readability_index][category]['freq_' + value_index] = 0
                                        statistics[readability_index][category]['freq_' + value_index] = \
                                            statistics[readability_index][category]['freq_' + value_index] + 1
                            elif isinstance(index[value_index], str):
                                rec = index[value_index]
                                if value_index not in statistics[readability_index][category]:
                                    statistics[readability_index][category][value_index] = dict()
                                if 'freq_' + rec not in statistics[readability_index][category][value_index]:
                                    statistics[readability_index][category][value_index]['freq_' + rec] = 0
                                statistics[readability_index][category][value_index]['freq_' + rec] = \
                                    statistics[readability_index][category][value_index]['freq_' + rec] + 1
                            else:
                                print("Uncategorized: " + str(index[value_index]))

                            statistics[readability_index][category]['freq_' + value_index] = \
                                statistics[readability_index][category]['freq_' + value_index] + 1
                        else:
                            statistics[readability_index][category]['skipped_' + value_index] = \
                                statistics[readability_index][category]['skipped_' + value_index] + 1
                else:
                    for value_index in self.values_index[readability_index]:
                        statistics[readability_index][category]['skipped_' + value_index] = \
                            statistics[readability_index][category]['skipped_' + value_index] + 1
            else:
                print("THIS: " + record)

            if readability_index in record:
                index = record[readability_index]
                for value_index in self.values_index[readability_index]:
                    if value_index in index:
                        obtained_value = ReadabilityAnalyser.cast_to_float(index[value_index])

                        if obtained_value is not None:
                            index[value_index] = float(index[value_index])
                            ReadabilityAnalyser.fill_min_max_sum(index, value_index, statistics, readability_index)
                            if 'freq_' + value_index not in statistics[readability_index]:
                                statistics[readability_index]['freq_' + value_index] = 0
                            statistics[readability_index]['freq_' + value_index] = \
                                statistics[readability_index]['freq_' + value_index] + 1
                        elif isinstance(index[value_index], list):
                            for rec in index[value_index]:
                                if value_index not in statistics[readability_index]:
                                    statistics[readability_index][value_index] = dict()

                                if isinstance(rec, str):
                                    # print(value_index + " " + str(index[value_index]))
                                    if 'freq_' + rec not in statistics[readability_index][value_index]:
                                        statistics[readability_index][value_index]['freq_' + rec] = 0
                                    statistics[readability_index][value_index]['freq_' + rec] = \
                                        statistics[readability_index][value_index]['freq_' + rec] + 1
                                else:
                                    ReadabilityAnalyser.fill_min_max_sum_value(rec, value_index, statistics,
                                                                               readability_index)
                                    if 'freq_' + value_index not in statistics[readability_index][value_index]:
                                        statistics[readability_index]['freq_' + value_index] = 0
                                    statistics[readability_index]['freq_' + value_index] = \
                                        statistics[readability_index]['freq_' + value_index] + 1
                        elif isinstance(index[value_index], str):
                            rec = index[value_index]
                            if value_index not in statistics[readability_index]:
                                statistics[readability_index][value_index] = dict()
                            if 'freq_' + rec not in statistics[readability_index][value_index]:
                                statistics[readability_index][value_index]['freq_' + rec] = 0
                            statistics[readability_index][value_index]['freq_' + rec] = \
                                statistics[readability_index][value_index]['freq_' + rec] + 1
                        else:
                            print("Uncategorized: " + str(index[value_index]))

                        statistics[readability_index]['freq_' + value_index] = \
                            statistics[readability_index]['freq_' + value_index] + 1
                    else:
                        statistics[readability_index]['skipped_' + value_index] = \
                            statistics[readability_index]['skipped_' + value_index] + 1
            else:
                for value_index in self.values_index[readability_index]:
                    statistics[readability_index]['skipped_' + value_index] = \
                        statistics[readability_index]['skipped_' + value_index] + 1

    def count_average(self, statistics):
        for readability_index in statistics['indexes']:
            for value_index in self.values_index[readability_index]:
                if statistics[readability_index]['sum_' + value_index] != 0:
                    statistics[readability_index]['avg_' + value_index] = \
                        statistics[readability_index]['sum_' + value_index] / statistics[readability_index][
                            'freq_' + value_index]
                else:
                    statistics[readability_index]['sum_' + value_index] = 0
                for category in statistics['categories']:
                    if statistics[readability_index][category]['sum_' + value_index] != 0:
                        statistics[readability_index][category]['avg_' + value_index] = \
                            statistics[readability_index][category]['sum_' + value_index] / \
                            statistics[readability_index][category]['freq_' + value_index]
                    else:
                        statistics[readability_index][category]['sum_' + value_index] = 0

    def analyse_readability_file(self, readability_file, categories):
        statistic = dict()
        self.initialize_values(statistic, categories)

        file = load_as_json(readability_file)
        for record in file:
            self.record_analysis(record, statistic)

        self.count_average(statistic)
        return statistic

    def analyse_readability_file_save_results(self, readability_file, output_statistics_file, categories):
        statistics = self.analyse_readability_file(readability_file, categories)
        save_as_json(statistics, output_statistics_file)


def readability_analysis_of_weir():
    # readability_analysis_weir()
    readability_statistics_from_analysis_weir()


if __name__ == "__main__":
    readability_analysis_of_weir()
