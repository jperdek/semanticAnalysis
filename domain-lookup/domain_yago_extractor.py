
import fileinput
import domain_wordnet_extractor
import re



def get_all_associated_labels(domain_file, domain_terms_dict, output_file):
    domains = dict()
    i = 0
    j = 0
    with open(output_file, 'w', encoding="utf-8") as output_file_f:
        with open(domain_file, 'r', encoding="utf-8") as f:
            for line in f:
                term_array = [ i.lower() for i in re.split("[\t @\\$%&-*\"'_]", line.split('\t')[3])[:-1]
                               if i and len(i) > 2]
                # print(term_array)
                if term_array is None:
                    continue
                max_length = len(term_array)
                while i < max_length:
                    for domain_term in domain_terms_dict:
                        domain_terms_of_term = domain_term.split('_')
                        j = 0
                        max_length_j = len(domain_terms_of_term)
                        # if max_length <= i + max_length_j:
                        #    continue

                        not_found = False
                        while j < max_length_j:
                            # print(domain_terms_of_term[j] +" "+ term_array[j + i])
                            if domain_terms_of_term[j] != term_array[j + i]:
                                not_found = True
                                break
                            j = j + 1

                        if not not_found:
                            print("FOUND")
                            output_file_f.writeline(line)
                    i = i + 1

    return domains


def get_selected_label(label_name, domain_file, output_file, domain_narrowers_dict, output_produce=False):
    with open(output_file, 'w', encoding="utf-8") as output_file_f:
        with open(domain_file, 'r', encoding="utf-8") as f:
            for line in f:
                print(line)
                result = line.find(label_name)
                if result != -1:
                    print("FOUND: " + line)


def get_unique_values(file_name, delimitor, coll_number, output_file_name="unique_values.txt", save_file=False):
    dictionary = dict()
    with open(file_name, 'r', encoding="utf-8") as f:
        for line in f:
            unique_value_array = line.split(delimitor)
            if len(unique_value_array) > coll_number:
                unique_value = unique_value_array[coll_number]
                dictionary[unique_value] = unique_value

    if save_file:
        with open(output_file_name, "w", encoding="utf-8") as output_file_f:
            for value in dictionary:
                output_file_f.write(value + "\n")
    else:
        for value in dictionary:
            print(value)


def find_unique_predicates_of_facts():
    get_unique_values("D://yago/yagoFacts.tsv", '\t', 2, "./yagoProcessed/yagoFactsPredicates.txt", True)
    get_unique_values("D://yago/yagoDateFacts.tsv", '\t', 2, "./yagoProcessed/yagoDateFactsPredicates.txt", True)
    get_unique_values("D://yago/ttl/yagoLiteralFacts.ttl", '\t', 1, "./yagoProcessed/yagoLiteralFactsPredicates.txt",
                      True)
    get_unique_values("D://yago/ttl/yagoMetaFacts.ttl", '\t', 1, "./yagoProcessed/yagoMetaFactsPredicates.txt", True)


def find_unique_predicates_wikipedia():
    get_unique_values("D://yago/ttl/yagoConteXtFacts_en.ttl", '\t', 1, "./yagoProcessed/yagoConteXtFactsEn.txt", True)


def get_lines_according_word_from_yago(searched_word, output_file, file_paths_dictionary):
    # get_lines_according_word_from_yago_core(searched_word, output_file, file_paths_dictionary)
    get_lines_according_word_from_yago_simpletax(searched_word, output_file, file_paths_dictionary)


def get_lines_according_word_from_yago_core(searched_word, output_file, file_paths_dictionary):
    add_header_to_created_file(output_file)
    get_selected_word_records(searched_word, file_paths_dictionary["core.yagoLabels"], output_file, False)
    get_selected_word_records(searched_word, file_paths_dictionary["core.yagoLiteralFacts"], output_file, False)
    get_selected_word_records(searched_word, file_paths_dictionary["core.yagoFacts"], output_file, False)
    get_selected_word_records(searched_word, file_paths_dictionary["core.yagoDateFacts"], output_file, False)


def get_lines_according_word_from_yago_simpletax(searched_word, output_file, file_paths_dictionary):
    get_selected_word_records(searched_word, file_paths_dictionary["simpletax.yagoSimpleTypes"], output_file, False)
    get_selected_word_records(searched_word, file_paths_dictionary["simpletax.yagoSimpleTaxonomy"], output_file, False)


def file_paths_dict():
    file_paths = dict()
    file_paths["core.yagoLabels"] = "D://yago/ttl/yagoLabels.ttl"
    file_paths["core.yagoLiteralFacts"] = "D://yago/ttl/yagoLiteralFacts.ttl"
    file_paths["core.yagoFacts"] = "D://yago/ttl/yagoFacts.ttl"
    file_paths["core.yagoDateFacts"] = "D://yago/ttl/yagoDateFacts.ttl"

    file_paths["simpletax.yagoSimpleTypes"] = "D://yago/ttl/yagoSimpleTypes.ttl"
    file_paths["simpletax.yagoSimpleTaxonomy"] = "D://yago/ttl/yagoSimpleTaxonomy.ttl"

    file_paths["meta.yagoSources"] = "D://yago/ttl/yagoSources.ttl"
    file_paths["meta.yagoMetaFacts"] = "D://yago/ttl/yagoMetaFacts.ttl"
    file_paths["meta.yagoStatistics"] = "D://yago/ttl/yagoStatistics.ttl"
    file_paths["meta.yagoGeonamesTypesSources"] = "D://yago/ttl/geo/yagoGeonamesTypesSources.ttl"

    file_paths["other.contentXFactsEn"] = "D://yago/ttl/yagoSimpleTaxonomy.ttl"
    file_paths["other.redirectLabelsEn"] = "D://yago/ttl/yagoRedirectLabels_en.ttl"
    file_paths["other.typesSources"] = "D://yago/ttl/yagoTypesSources.ttl"

    file_paths["taxonomy.yagoTransitiveType"] = "D://yago/ttl/yagoTransitiveType.ttl"
    file_paths["taxonomy.yagoSchema"] = "D://yago/ttl/yagoSchema.ttl"
    file_paths["taxonomy.yagoTypes"] = "D://yago/ttl/yagoTypes.ttl"
    file_paths["taxonomy.yagoTaxonomy"] = "D://yago/ttl/yagoTaxonomy.ttl"

    file_paths["other.yagoGeonamesEntityIds"] = "D://yago/ttl/yagoGeonamesEntityIds.ttl"
    file_paths["other.yagoPreferredMeanings"] = "D://yago/ttl/yagoPreferredMeanings.ttl"
    file_paths["other.yagoDBpediaInstances"] = "D://yago/ttl/yagoDBpediaInstances.ttl"
    file_paths["other.yagoDBpediaClasses"] = "D://yago/ttl/yagoDBpediaClasses.ttl"
    file_paths["other.yagoWordnetDomainHierarchy"] = "D://yago/ttl/yagoWordnetDomainHierarchy.ttl"
    file_paths["other.yagoWordnetIds"] = "D://yago/ttl/yagoWordnetIds.ttl"
    file_paths["other.yagoWordnetDomains"] = "D://yago/ttl/yagoWordnetDomains.ttl"

    file_paths["wikipedia.yagoWikipediaInfoEn"] = "D://yago/ttl/yagoWikipediaInfo_en.ttl"
    file_paths["wikipedia.yagoInfoboxAttributesEn"] = "D://yago/ttl/yagoInfoboxAttributes_en.ttl"
    file_paths["wikipedia.yagoInfoboxTemplateAttributesEn"] = "D://yago/ttl/yagoInfoboxTemplateAttributes_en.ttl"
    file_paths["wikipedia.yagoInfoboxTemplateSourcesEn"] = "D://yago/ttl/yagoInfoboxTemplateSources_en.ttl"
    file_paths["wikipedia.yagoInfoboxTemplatesEn"] = "D://yago/ttl/yagoInfoboxTemplates_en.ttl"

    file_paths["multilingual.yagoMultilingualClassLabels"] = "D://yago/ttl/yagoMultilingualClassLabels.ttl"

    file_paths["geonames.yagoGeonamesClasses"] = "D://yago/ttl/geo/yagoGeonamesClasses.ttl"
    file_paths["geonames.yagoGeonamesOnlyData"] = "D://yago/ttl/geo/yagoGeonamesOnlyData.ttl"
    file_paths["geonames.yagoGeonamesTypes"] = "D://yago/ttl/geo/yagoGeonamesTypes.ttl"
    file_paths["geonames.yagoGeonamesClasses_old"] = "D://yago/ttl/geo/yagoGeonamesClasses_old.ttl"
    file_paths["geonames.yagoGeonamesGlosses"] = "D://yago/ttl/geo/yagoGeonamesGlosses.ttl"
    file_paths["geonames.yagoGeonamesClassIds"] = "D://yago/ttl/geo/yagoGeonamesClassIds.ttl"

    return file_paths


def get_selected_word_records(searched_word, search_file, output_file, rewrite=True):
    write_string = "a"
    if rewrite:
        write_string = "w"
    with open(output_file, write_string, encoding="utf-8") as output_file_f:
        with open(search_file, 'r', encoding="utf-8") as f:
            for line in f:
                if line.lower().find(searched_word.lower()) >= 0:
                    output_file_f.write(line)


def get_role_index(role):
    if role == "subject":
        return 0
    elif role == "predicate":
        return 1
    elif role == "object":
        return 2


def find_in_file_according_role(searched_parts, role, search_file, output_file,
                                store_subject=False, store_predicate=False, store_object=False, rewrite=True):
    store_dict = dict();
    store_dict['subjects'] = []
    store_dict['objects'] = []
    store_dict['predicates'] = []

    write_string = "a"
    if rewrite:
        write_string = "w"
    role_index = get_role_index(role)
    with open(output_file, write_string, encoding="utf-8") as output_file_f:
        with open(search_file, 'r', encoding="utf-8") as f:
            for line in f:
                triple = line.split('\t')
                if len(triple) != 3:
                    continue
                for searched_part in searched_parts:
                    if searched_part.lower() == triple[role_index].lower():
                        if store_subject:
                            store_dict['subjects'].append(triple[0])
                        if store_predicate:
                            store_dict['predicates'].append(triple[1])
                        if store_object:
                            store_dict['objects'].append(triple[2])
                        output_file_f.write(line)
    return store_dict


def add_header_to_created_file(output_file):
    with open(output_file, "w", encoding="utf-8") as output_file_f:
        output_file_f.write("@base <http://yago-knowledge.org/resource/> .\n")
        output_file_f.write("@prefix dbp: <http://dbpedia.org/ontology/> .\n")
        output_file_f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
        output_file_f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
        output_file_f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
        output_file_f.write("@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n")
        output_file_f.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")


def book_retrieval_strategy1(file_paths_dictionary):
    output_file = "yagoProcessed/book_strategy1.ttl"
    add_header_to_created_file(output_file)
    #rdfs:type WIKI WORDNET
    found_dict1 = find_in_file_according_role(["<Single-entry_bookkeeping_system>"], "subject",
                                              file_paths_dictionary["taxonomy.yagoTransitiveType"],
                                              output_file, store_subject=False, store_predicate=False,
                                              store_object=True, rewrite=False)
    print(found_dict1['objects'])
    found_wordnet = find_in_file_according_role(found_dict1['objects'], "subject",
                                                file_paths_dictionary["other.yagoWordnetDomains"], output_file,
                                                store_subject=False, store_predicate=False, store_object=True,
                                                rewrite=False)
    find_in_file_according_role(found_wordnet['objects'], "subject",
                                file_paths_dictionary["other.yagoWordnetDomainHierarchy"],
                                output_file, store_subject=False, store_predicate=False, store_object=False,
                                rewrite=False)
    find_in_file_according_role(found_wordnet['objects'], "subject", file_paths_dictionary["other.yagoWordnetDomains"],
                                output_file, store_subject=False, store_predicate=False, store_object=False,
                                rewrite=False)


# domain_terms_dict = domain_wordnet_extractor.load_domain_parts_wordnet_as_dict("book_keeping", "./wordnet/domain-parts.json")
# print(domain_terms_dict)
#get_all_associated_labels("D://yago/yagoLabels.tsv", domain_terms_dict, "./yagoProcessed/labels_book_keeping.txt", dict(),
#                          False)
# get_selected_label("id_6B9z6YiJIa_wda_Of!esIyBbW", "D://yago/ttl/yagoLabels.ttl", "./yagoProcessed/labels.txt", dict(), False)
# get_selected_label("bookkeeping", "D://yago/ttl/yagoRedirectLabels_en.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("bookkeeping", "D://yago/ttl/yagoTypes.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("bookkeeping", "D://yago/ttl/yagoTransitiveType.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("book_keeping", "D://yago/ttl/yagoTypesSources.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("bookkeeping", "D://yago/ttl/yagoTypesSources.ttl", "./yagoProcessed/labels.txt", dict(), False)

#get_selected_label("book_keeping", "D://yago/ttl/yagoLabels.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("bookkeeping", "D://yago/ttl/yagoSimpleTypes.ttl", "./yagoProcessed/labels.txt", dict(), False)
# get_selected_label("bookkeeping", "D://yago/ttl/yagoSimpleTypes.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("bookkeeping", "D://yago/ttl/geo/yagoGeonamesOnlyData.ttl", "./yagoProcessed/labels.txt", dict(), False)
# get_selected_label("bookkeeping", "D://yago/ttl/yagoSources.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("bookkeeping", "D://yago/ttl/yagoInfoboxAttributes_en.ttl", "./yagoProcessed/labels.txt", dict(), False)
# get_selected_label("bookkeeping", "D://yago/ttl/yagoWikipediaInfo_en.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("bookkeeping", "D://yago/ttl/yagoFacts.ttl", "./yagoProcessed/labels.txt", dict(), False)
#get_selected_label("bookkeeping", "D://yago/ttl/yagoConteXtFacts_en.ttl", "./yagoProcessed/labels.txt", dict(), False)

#find_unique_predicates_wikipedia()
#find_unique_predicates_of_facts()
# get_lines_according_word_from_yago("bookkeeping", "./yagoProcessed/yago_bookkepping.txt", file_paths_dict())
book_retrieval_strategy1(file_paths_dict())