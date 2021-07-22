import json
import random
from nltk.corpus import wordnet


class SemcorAnalyser:

    @staticmethod
    def load_as_json(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def __init__(self, path_to_hierarchy = "../domain-lookup/wordnet/domain-parts.json",
                 path_to_semcor_frequencies = "semcor_frequencies.json"):
        self.domain_hierarchy = self.load_as_json(path_to_hierarchy)
        self.semcor_frequencies = self.load_as_json(path_to_semcor_frequencies)
        self.vector_for_domain_synset = self.create_vector_for_domain()

    def __init__(self, loaded_hierarchy, loaded_semcor_frequencies, load_files):
        self.domain_hierarchy = loaded_hierarchy
        self.semcor_frequencies = loaded_semcor_frequencies
        self.vector_for_domain_synset = self.create_vector_for_domain()

    def create_vector_for_domain(self):
        new_vector = dict()
        for category_name, subcategory_dict in self.domain_hierarchy.items():
            new_vector[category_name] = 0
        return new_vector

    # slower function - can be enhanced using already calculated values
    def get_probability(self, word, normal_dist_value=1, debug=False, describe=False):
        domain_vector = self.create_vector_for_domain()
        total_category_sum = 0
        for lemma in wordnet.lemmas(word):
            lemma_name = lemma.name()
            lemma_synset = lemma.synset()
            synset_name = lemma_synset.name()
            if lemma_name not in self.semcor_frequencies:
                if debug:
                    print("Lemma not found: ", lemma_name)
                break

            if synset_name not in self.semcor_frequencies[lemma_name]:
                if debug:
                    print("Synset name not found: ", synset_name)
                break

            # CLASSIFY ONLY ACCORDING CATEGORY
            if "category" in self.semcor_frequencies[lemma_name][synset_name]:
                if describe:
                    print("Lemma name: ", lemma_name, " category: ", self.semcor_frequencies[lemma_name][synset_name][
                        "category"])

                category_name = self.semcor_frequencies[lemma_name][synset_name]["category"]
                if category_name not in domain_vector:
                    if debug:
                        print("Category with name: ", category_name, " not exists!")
                    continue
                # ADDS TO CERTAIN CATEGORY
                domain_vector[category_name] = domain_vector[category_name] + self.semcor_frequencies[lemma_name][
                    synset_name]["count"]
                # ADDS TO TOTAL CATEGORY SUM
                total_category_sum = total_category_sum + self.semcor_frequencies[lemma_name][synset_name]["count"]

        for category_name in domain_vector.keys():
            if total_category_sum != 0:
                domain_vector[category_name] = domain_vector[category_name] / total_category_sum
                domain_vector[category_name] = domain_vector[category_name] * normal_dist_value
            else:
                domain_vector[category_name] = 0
        return domain_vector

    def count_vectors(self, vector1, vector2):
        if len(vector1) != len(vector2):
            print("Error: vectors differ in lenght!")
            return None
        for category_name in self.domain_hierarchy.keys():
            vector1[category_name] = vector1[category_name] + vector2[category_name]
        return vector1

    @staticmethod
    def print_domain_vector_results(domain_vector):
        for category_name, value in domain_vector.items():
            if value > 0:
                print("Category: ", category_name, " value: ", value)

    def analyse_text_semcor(self, text, k, repeat=2, use_normal_dist=False, debug=False, describe=False):
        dest_text_domain_vector = self.create_vector_for_domain()
        words_text = text.split()
        length_text = len(words_text)
        print(type(length_text))
        print(type(k))
        for time in range(0, repeat):
            for i in range(0, length_text - k + 1):
                for j in range(i - k, i + k):
                    if j < 0 or j > length_text:
                        continue
                    if use_normal_dist:
                        random_normal_distribution = random.gauss(i, k*k)
                    else:
                        random_normal_distribution = 1

                    dest_text_domain_vector = self.count_vectors(dest_text_domain_vector, self.get_probability(
                        words_text[j], random_normal_distribution, debug, describe))
        self.print_domain_vector_results(dest_text_domain_vector)


if __name__ == "__main__":
    semcorAnalyser = SemcorAnalyser("../domain-lookup/wordnet/domain-parts.json", "semcor_frequencies.json")
    semcorAnalyser.analyse_text_semcor("A compound capable of transferring a hydrogen ion in solution", 6)
