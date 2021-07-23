import re
import json
import csv_to_ttl
import csvwlib
from cow_csvw.csvw_tool import CSVWConverter

def get_all_wordnet_domains(domain_file, output_file, output_produce=False):
    domains = dict()
    with open(domain_file, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            found_match = re.search(r'<wordnetDomain_([^>]*)>', line)
            if found_match is not None:
                found = found_match.group(1)
                domains[found] = found
    if output_produce:
        save_as_json(list(domains.keys()), output_file)
    return domains


def find_all_narrowers(narrower_file, domains, output_file, output_produce=False):
    with open(narrower_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            found_match = re.search(r'wordnetDomain_([^>]*)>\tskos:narrower\t<wordnetDomain_([^>]*)>', line)
            if found_match is not None and len(found_match.groups()) == 2:
                base_domain = found_match.group(1)
                dest_domain = found_match.group(2)
                if base_domain not in domains:
                    domains[base_domain] = []
                if not isinstance(domains[base_domain], list):
                    domains[base_domain] = []
                domains[base_domain].append(dest_domain)
    if output_produce:
        save_as_json(domains, output_file)
    return domains


def find_yago_labels_and_types(narrower_file, output_file, output_produce=False):
    domains = dict()
    with open(narrower_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            found_match = re.search(r'wordnetDomain_([^>]*)>\t([^\t]*)\t([^\t]*)', line)

            if found_match is not None and len(found_match.groups()) == 3:
                type = found_match.group(2)
                # print(type)
                if type == "rdf:type" or type == "rdfs:label":
                    base_domain = found_match.group(1)
                    dest_domain = found_match.group(3)
                    if base_domain not in domains:
                        domains[base_domain] = dict()

                    if type == "rdf:type":
                        domains[base_domain]["type"] = dest_domain.replace('\"', "").replace("\n", "").replace('\t', "")
                    elif type == "rdfs:label":
                        domains[base_domain]["label"] = dest_domain.replace('\"', "").replace("\n", "").replace('\t', "")
    if output_produce:
        save_as_json(domains, output_file)
    return domains


def find_associated_parts(domain_file, domains, output_file, output_produce=False):
    with open(domain_file, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            found_match = re.search(r'<wordnet_([^0-9]*)([0-9]*)>\t<hasWordnetDomain>\t<wordnetDomain_([^>]*)>', line)
            if found_match is not None and len(found_match.groups()) == 3:
                name_part = found_match.group(1)[:-1]
                id_part = found_match.group(2)
                base_domain = found_match.group(3)
                if base_domain not in domains:
                    domains[base_domain] = dict()
                if not isinstance(domains[base_domain], dict):
                    domains[base_domain] = dict()
                domains[base_domain][name_part] = id_part
    if output_produce:
        save_as_json(domains, output_file)
    return domains


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def create_json_from_wordnet():
    domain_names = get_all_wordnet_domains("D://yago/wordnet/yagoWordnetDomains.tsv",
                                           "../../../../../../output/domain-lookup/wordnet/domains.json", True)
    find_associated_parts("D://yago/wordnet/yagoWordnetDomains.tsv", domain_names,
                          "../../../../../../output/domain-lookup/wordnet/domain-parts.json", True)

    domain_names = get_all_wordnet_domains("D://yago/wordnet/yagoWordnetDomains.tsv",
                                           "../../../../../../output/domain-lookup/wordnet/domains.json", True)
    find_all_narrowers("D://yago/wordnet/yagoWordnetDomainHierarchy.tsv", domain_names,
                       "../../../../../../output/domain-lookup/wordnet/domains-narrowers.json"
                       , True)

    find_yago_labels_and_types("D://yago/ttl/yagoWordnetDomains.ttl",
                               "../../../../../../output/domain-lookup/wordnet/yago_wordnet_assoc.json", True)


def create_json_subclasses():
    domain_parts = load_as_json("../../../../../../output/domain-lookup/wordnet/domain-parts.json")
    get_wordnet_subclasses_from_wiki(domain_parts, ["D://yago/ttl/yagoSimpleTaxonomy.ttl"],
                                     "../../../../../../output/domain-lookup/wordnet/subclasses.json",
                                     True)


def create_ttl_for_domain(domain_name):
    pass


# NOT WORKS
def convert_csv_to_ttl_chosen_files():
    # csv_to_ttl.convert_csv_to_ttl("D://yago/wordnet/yagoWordnetDomains.tsv", "D://yago/wordnet/yagoWordnetDomains.ttl")
    # csvwlib.CSVWConverter.to_rdf('D://yago/wordnet/yagoWordnetDomains.csv', "D://yago/yagoSchema.csv", mode='minimal', format='ttl')
    # csvwlib.CSVWConverter.to_rdf('file:///d://yago/wordnet/test001.csv',mode='minimal', format='ttl')
    # CSVWConverter("D://yago/wordnet/yagoWordnetDomains.tsv", delimiter='\t',  output_format='nt', base="D://yago/yagoSchema.tsv")
    # csvwlib.CSVWConverter.to_rdf('http://w3c.github.io/csvw/tests/test001.csv', format='ttl')
    return 0


def load_domain_parts_wordnet_as_dict(domain_name, domain_parts_file):
    domain_parts = load_as_json(domain_parts_file)
    array = domain_parts[domain_name]
    dictionary = dict()
    for item in array:
        dictionary[item] = "T"
    return dictionary


def load_all_domain_parts_as_dict(domain_parts_file):
    return load_as_json(domain_parts_file)


def get_records_from_selected_domain_and_narrowers(domain_name, narrower_file, domain_file, output_file,
                                                   include_narrowers=True):
    get_selected_wordnet_domain(domain_name, domain_file, output_file)
    if include_narrowers:
        get_selected_wordnet_narrowers(domain_name, narrower_file, output_file, False)


def get_selected_wordnet_domain(domain_name, domain_file, output_file, rewrite=True):
    write_string = "a"
    if rewrite:
        write_string = "w"
    with open(output_file, write_string, encoding="utf-8") as output_file_f:
        with open(domain_file, 'r', encoding="utf-8") as f:
            for line in f:
                found_match = re.search(r'<wordnetDomain_([^>]*)>', line)
                if found_match is not None and domain_name == found_match.group(1):
                    output_file_f.write(line)


def get_selected_wordnet_narrowers(domain_name, narrower_file, output_file, rewrite=True):
    write_string = "a"
    if rewrite:
        write_string = "w"
    with open(output_file, write_string, encoding="utf-8") as output_file_f:
        with open(narrower_file, "r", encoding="utf-8") as f:
            for line in f:
                found_match = re.search(r'wordnetDomain_([^>]*)>\tskos:narrower\t<wordnetDomain_([^>]*)>', line)
                if found_match is not None and len(found_match.groups()) == 2:
                    base_domain = found_match.group(1)
                    dest_domain = found_match.group(2)
                    if base_domain == domain_name or dest_domain == domain_name:
                        output_file_f.write(line)


def get_wordnet_subclasses_from_wiki(domain_parts, taxonomy_file_paths, output_file, rewrite=True, include_not_found=False):
    wordnet_with_subclasses = dict()

    for taxonomy_file_path in taxonomy_file_paths:
        with open(taxonomy_file_path, "r", encoding="utf-8") as f:
            for line in f:
                found_match = re.search(r'(<[^>]*>)\t([^>]*)\t(<[^>]*>)', line)
                if found_match is not None and len(found_match.groups()) == 3:
                    predicate = found_match.group(2)
                    base_domain = found_match.group(1)
                    dest_domain = found_match.group(3)

                    if predicate == "rdfs:subClassOf":
                        base_wordnet = base_domain.find("<wordnet_")
                        dest_wordnet = dest_domain.find("<wordnet_")
                        base_wiki = base_domain.find("<wikicat_")
                        dest_wiki = dest_domain.find("<wikicat_")
                        dest_wordnet_word = None
                        dest_wiki_word = None
                        base_wordnet_word = None
                        base_wiki_word = None

                        if dest_wordnet == 0:
                            result = re.search(r'<wordnet_([^0-9]*)', dest_domain)
                            dest_wordnet_word = result.group(1)[:-1]

                        if base_wordnet == 0:
                            result = re.search(r'<wordnet_([^0-9]*)', base_domain)
                            base_wordnet_word = result.group(1)[:-1]

                        if dest_wiki == 0:
                            result = re.search(r'<wikicat_([^>]*)', dest_domain)
                            dest_wiki_word = result.group(1)[:-1]

                        if base_wiki == 0:
                            result = re.search(r'<wikicat_([^>]*)', base_domain)
                            base_wiki_word = result.group(1)[:-1]

                        if dest_wordnet_word in domain_parts.keys():
                            if category not in wordnet_with_subclasses:
                                wordnet_with_subclasses[category] = domain_parts[category]

                            if dest_wordnet_word not in wordnet_with_subclasses:
                                wordnet_with_subclasses[dest_wordnet_word] = dict()
                            wordnet_with_subclasses[category]["subClasses_wiki"] = []
                            wordnet_with_subclasses[category]["subClasses_wordnet"] = []
                            if base_wiki == 0:
                                wordnet_with_subclasses[category]["subClasses_wiki"].append(base_wiki_word)
                            elif base_wordnet == 0:
                                #print("wordnet - wordnet mapping category! >" + base_domain + "<")

                                wordnet_with_subclasses[category]["subClasses_wordnet"].append(base_wordnet_word)
                        else:
                            if dest_wiki_word is not None:
                                print("Dest wiki cat subclass found!!!")
                                continue

                            if dest_wordnet_word is not None:
                                #print(dest_wordnet_word)
                                #print(base_wiki_word)
                                found_sub = False
                                for category, items in domain_parts.items():
                                    if dest_wordnet_word in items.keys():
                                        found_sub = True
                                        if category not in wordnet_with_subclasses:
                                            wordnet_with_subclasses[category] = dict()

                                        if dest_wordnet_word not in wordnet_with_subclasses[category]:
                                            id = domain_parts[category][dest_wordnet_word]
                                            wordnet_with_subclasses[category][dest_wordnet_word] = dict()
                                            wordnet_with_subclasses[category][dest_wordnet_word]["id"] = id

                                        if base_wiki == 0:
                                            if "subClasses_wiki" not in wordnet_with_subclasses[category][dest_wordnet_word]:
                                                wordnet_with_subclasses[category][dest_wordnet_word][
                                                    "subClasses_wiki"] = []
                                            wordnet_with_subclasses[category][dest_wordnet_word]["subClasses_wiki"]\
                                                .append(base_wiki_word)
                                        elif base_wordnet == 0:
                                            if "subClasses_wordnet" not in wordnet_with_subclasses[category][dest_wordnet_word]:
                                                wordnet_with_subclasses[category][dest_wordnet_word][
                                                    "subClasses_wordnet"] = []
                                            # print("wordnet - wordnet mapping! >" + base_domain + "<")
                                            wordnet_with_subclasses[category][dest_wordnet_word]["subClasses_wordnet"].append(
                                                base_wordnet_word)

                                if not found_sub and include_not_found:
                                    category = dest_wordnet_word

                                    if dest_wordnet_word not in wordnet_with_subclasses:
                                        print("Sub category not found for dest - subject wordnet: " + dest_wordnet_word)
                                        wordnet_with_subclasses[category] = dict()
                                        wordnet_with_subclasses[category][dest_wordnet_word] = dict()
                                        result = re.search(r'<wordnet_[^0-9]*([0-9]*)>', dest_domain)
                                        id = result.group(1)
                                        print(dest_wordnet_word)
                                        wordnet_with_subclasses[category][dest_wordnet_word]['id'] = id

                                    if base_wiki == 0:
                                        if "subClasses_wiki" not in wordnet_with_subclasses[category][dest_wordnet_word]:
                                            wordnet_with_subclasses[category][dest_wordnet_word][
                                                "subClasses_wiki"] = []
                                        wordnet_with_subclasses[category][dest_wordnet_word]["subClasses_wiki"]\
                                            .append(base_wiki_word)
                                    elif base_wordnet == 0:
                                        if "subClasses_wordnet" not in wordnet_with_subclasses[category][dest_wordnet_word]:
                                            wordnet_with_subclasses[category][dest_wordnet_word][
                                                "subClasses_wordnet"] = []
                                        # print("wordnet - wordnet mapping! >" + base_domain + "<")
                                        wordnet_with_subclasses[category][dest_wordnet_word]["subClasses_wordnet"].append(
                                            base_wordnet_word)
    if rewrite:
        save_as_json(wordnet_with_subclasses, output_file)

    return wordnet_with_subclasses


# CREATE JSON ASSOCIATION FROM WORDNET
# create_json_from_wordnet()

create_json_subclasses()

# CREATES TURTLE INFORMATION ASSOCIATED WITH SPECIFIC DOMAIN
# get_records_from_selected_domain_and_narrowers("book_keeping", "D://yago/ttl/yagoWordnetDomainHierarchy.ttl",
#                                               "D://yago/ttl/yagoWordnetDomains.ttl",
#                                               './yagoProcessed/wordnet_book_keeping.ttl')

# convert_csv_to_ttl_chosen_files()
