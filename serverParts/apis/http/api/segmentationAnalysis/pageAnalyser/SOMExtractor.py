
import xml.etree.ElementTree as elementTree
from lxml import etree
from bs4 import BeautifulSoup
import bs4
import os
import json
import re
import random


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


class SOMBeautifulSoup:

    @staticmethod
    def create_dom_beautiful_soup(file_name):
        with open(file_name, "rb") as file:
            parser = BeautifulSoup(file.read().decode('utf-8', 'ignore'), "html.parser")
        return parser

    @staticmethod
    def parse_tree_beautiful_soup(path_category, path_final_tree, domain_only=True):
        root = {}
        whole_count = 0
        for domain in os.listdir(path_category):
            domain_dir = os.path.join(path_category, domain)
            if os.path.isdir(domain_dir):
                for page_name in os.listdir(domain_dir):
                    page = os.path.join(domain_dir, page_name)
                    try:
                        dom = SOMBeautifulSoup.create_dom_beautiful_soup(page)
                        print(page)
                        # print(elementTree.tostring(dom.getroot(), encoding='utf8').decode('utf8'))
                        SOMBeautifulSoup.parse_tree_dom_beautiful_soup(root, dom, 1, page_name)
                    except etree.XMLSyntaxError:
                        continue
                    except UnicodeDecodeError:
                        continue
                    except RecursionError:
                        continue
                    whole_count = whole_count + 1
                    #save_as_json(root, path_final_tree)
                    # return
            if domain_only:
                root['whole_count'] = whole_count
                save_as_json(root, path_final_tree + "_" + domain + ".json")
                root = dict()
                whole_count = 0

        if not domain_only:
            root['whole_count'] = whole_count
            save_as_json(root, path_final_tree)

    @staticmethod
    def create_dom_label_beautiful_soup(order, tag, attrib):
        dom_label = str(order) + "/" + tag
        if len(attrib) != 0:
            dom_label = dom_label + "/" + "".join(str(v) for v in attrib.values())
        return dom_label

    @staticmethod
    def filter_text_in_tree_beautiful_soup(dom):
        insert_text = ""

        if dom.text is not None and re.search(r'^\S+', dom.get_text()):
            insert_text = dom.text

        return insert_text

    @staticmethod
    def check_text_in_list_beutiful_soap(dom):
        xmlstr = str(dom)

        # find all text elements
        array = re.findall(r"(<\s*/?\s*[abiph][1-6]?\s*\\?\s*>|<\s*a\s[^>]*\\?\s*>)", xmlstr)
        array1 = re.findall(r"(<\s*/?\s*[^>]*\s*>)", xmlstr)

        # if len(array) is greater when both find all elements - i applied +2 too
        if len(array) >= len(array1):
            obtained_text = ''.join(dom.get_text())
            return obtained_text
        else:
            return None

    @staticmethod
    def create_new_node_beautiful_soup(dom, file_name):
        element = dict()
        element['tag'] = dom.name
        element['count'] = 1
        insert_text = SOMBeautifulSoup.filter_text_in_tree(dom)
        if insert_text != "":
            element['files'] = []
            # element['files'].append(file_name)
            element['text'] = insert_text
            SOMBeautifulSoup.insert_text_with_file_name(file_name, insert_text, element)
            element['flag'] = True
        else:
            element['flag'] = False
        element['children'] = dict()
        return element

    @staticmethod
    def insert_text_with_file_name(file_name, insert_text, dictionary):
        if 'text' not in dictionary:
            dictionary['text'] = insert_text
            if 'files' not in dictionary:
                dictionary['flag'] = True
                dictionary['files'] = []
            dictionary['files'].append(file_name)
            return

        if dictionary['text'] != insert_text and insert_text != "":
            content = dict()
            content[file_name] = insert_text
            if 'files' not in dictionary:
                dictionary['flag'] = True
                dictionary['files'] = []
            if content not in dictionary['files']:
                dictionary['files'].append(content)
        elif insert_text != "":
            if 'files' not in dictionary:
                dictionary['flag'] = True
                dictionary['files'] = []
            if file_name not in dictionary['files']:
                dictionary['files'].append(file_name)

    @staticmethod
    def filter_text_in_tree(dom):
        insert_text = ""

        if dom.text is not None and re.search(r'^\S+', dom.text):
            insert_text = dom.text
        if dom.tail is not None and re.search(r'^\S+', dom.tail):
            insert_text = insert_text + dom.tail
        return insert_text

    @staticmethod
    def parse_tree_dom_beautiful_soup(dictionary, dom, order, file_name, skip_tags=("br", "hr")):
        # skips None tags and unusual tags
        if dom is None or dom.name in skip_tags:
            return

        # creates label to uniquely describe node
        dom_label = SOMBeautifulSoup.create_dom_label_beautiful_soup(order, dom.name, dom.attrs)

        # if label is in three then counter should be increased
        if dom_label in dictionary:
            dictionary[dom_label]['count'] = dictionary[dom_label]['count'] + 1
            if dictionary[dom_label]['flag']:
                insert_text = SOMBeautifulSoup.filter_text_in_tree_beautiful_soup(dom)
                SOMBeautifulSoup.insert_text_with_file_name(file_name, insert_text, dictionary[dom_label])
                # process_repetition_of_text(insert_text, dom_label, dom, dictionary)
                # dictionary[dom_label]['files'].append(file_name)
        # if label is not in three then it should be added to it
        else:
            dictionary[dom_label] = SOMBeautifulSoup.create_new_node_beautiful_soup(dom, file_name)

        text_in_list = SOMBeautifulSoup.check_text_in_list_beutiful_soap(dom)
        # if only text elements are available up to end of three
        if text_in_list is not None:
            # text should be overwrite because this one will contain much information except the same one
            SOMBeautifulSoup.insert_text_with_file_name(file_name, text_in_list, dictionary[dom_label])

        # if text elements are mixed with another ones for example with divs
        else:
            # prepares for another iteration in both threes
            for order, child in enumerate(dom):
                if isinstance(child, bs4.Tag):
                    # new nodes will be added as children and all settings will be propagated
                    SOMBeautifulSoup.parse_tree_dom_beautiful_soup(dictionary[dom_label]['children'], child, order,
                                                                   file_name, skip_tags=skip_tags)

    @staticmethod
    def parse_tree_beautiful_soup(html_page, page_name="undefined", root=None):
        if root is None:
            root = {}
        try:
            dom = BeautifulSoup(html_page, "html.parser")
            SOMBeautifulSoup.parse_tree_dom_beautiful_soup(root, dom, 1, page_name)
        except etree.XMLSyntaxError as syntax_error:
            return "Error: " + str(syntax_error)
        except UnicodeDecodeError as unicode_error:
            return "Error: " + str(unicode_error)
        except RecursionError as recursion_error:
            return "Error: " + str(recursion_error)
        return root


class SOMLxml:

    @staticmethod
    def create_dom(file_name):
        parser = etree.XMLParser(recover=True)
        return elementTree.parse(file_name, parser)

    @staticmethod
    def parse_tree(path_category, path_final_tree, domain_only=True):
        root = {}
        whole_count = 0
        for domain in os.listdir(path_category):
            domain_dir = os.path.join(path_category, domain)
            if os.path.isdir(domain_dir):
                for page_name in os.listdir(domain_dir):
                    page = os.path.join(domain_dir, page_name)
                    try:
                        dom = SOMLxml.create_dom(page)
                    except etree.XMLSyntaxError:
                        continue
                    print(page)

                    SOMLxml.parse_tree_dom(root, dom.getroot(), 1, page_name)
                    whole_count = whole_count + 1

            if domain_only:
                root['whole_count'] = whole_count
                save_as_json(root, path_final_tree + "_" + domain + ".json")
                root = dict()
                whole_count = 0

        if not domain_only:
            root['whole_count'] = whole_count
            save_as_json(root, path_final_tree)

    @staticmethod
    def create_dom_label(order, tag, attrib):
        dom_label = str(order) + "/" + tag
        if len(attrib) != 0:
            dom_label = dom_label + "/" + "".join(attrib)
        return dom_label

    @staticmethod
    def filter_text_in_tree(dom):
        insert_text = ""

        if dom.text is not None and re.search(r'^\S+', dom.text):
            insert_text = dom.text
        if dom.tail is not None and re.search(r'^\S+', dom.tail):
            insert_text = insert_text + dom.tail
        return insert_text

    @staticmethod
    def check_text_in_list(dom):

        try:
            xmlstr = elementTree.tostring(dom, encoding="utf-8").decode('utf-8')
        except TypeError:
            return None

        # find all text elements
        array = re.findall(r"(<\s*/?\s*[abiph][1-6]?\s*\\?\s*>|<\s*a\s[^>]*\\?\s*>)", xmlstr)
        array1 = re.findall(r"(<\s*/?\s*[^>]*\s*>)", xmlstr)

        # if len(array) is greater when both find all elements - i applied +2 too
        if len(array) >= len(array1):
            obtained_text = ''.join(dom.itertext())
            return obtained_text
        else:
            return None

    @staticmethod
    def create_new_node(dom, file_name):
        element = dict()
        element['tag'] = dom.tag
        element['count'] = 1
        insert_text = SOMLxml.filter_text_in_tree(dom)
        if insert_text != "":
            element['files'] = []
            # element['files'].append(file_name)
            element['text'] = insert_text
            SOMLxml.insert_text_with_file_name(file_name, insert_text, element)
            element['flag'] = True
        else:
            element['flag'] = False
        element['children'] = dict()
        return element

    @staticmethod
    def process_repetition_of_text(insert_text, dom_label, dom, dictionary):
        if insert_text != "":
            # if 'text' in dictionary[dom_label] and dictionary[dom_label]['text'] != insert_text and insert_text is
            #    not None and dictionary[dom_label]['text'] is not None:
            #    print("Difference: " + dictionary[dom_label]['text'] + "<--->" + insert_text)
            dictionary[dom_label]['text'] = dom.text

    @staticmethod
    # remove every line with document.write
    def parse_tree_dom_optional(dictionary, dom, order, file_name, count_threshold=400,
                                reject_to_store=("html", "head", "title"), skip_tags=("br", "hr")):
        # skips None tags and unusual tags
        if dom is None or dom.tag in skip_tags:
            return

        # creates label to uniquely describe node
        dom_label = SOMLxml.create_dom_label(order, dom.tag, dom.attrib)

        # if label is in three then counter should be increased
        if dom_label in dictionary:
            dictionary[dom_label]['count'] = dictionary[dom_label]['count'] + 1
            if dom.tag not in reject_to_store and dictionary[dom_label]['count'] < count_threshold:
                dictionary[dom_label]['files'].append(file_name)
                insert_text = SOMLxml.filter_text_in_tree(dom)
                SOMLxml.process_repetition_of_text(insert_text, dom_label, dom, dictionary)
        # if label is not in three then it should be added to it
        else:
            dictionary[dom_label] = SOMLxml.create_new_node(dom, file_name)

        text_in_list = SOMLxml.check_text_in_list(dom)
        # if only text elements are available up to end of three
        if text_in_list is not None:
            # text should be overwrite because this one will contain much information except the same one
            dictionary[dom_label]['text'] = text_in_list
        # if text elements are mixed with another ones for example with divs
        else:
            # prepares for another iteration in both threes
            for order, child in enumerate(dom):
                if isinstance(child, etree.Element) and not isinstance(child, etree.Entity) and \
                        not isinstance(child, etree.Comment):
                    # new nodes will be added as children and all settings will be propagated
                    SOMLxml.parse_tree_dom_optional(dictionary[dom_label]['children'], child, order, file_name,
                                                    reject_to_store=reject_to_store, skip_tags=skip_tags)

    @staticmethod
    def insert_text_with_file_name(file_name, insert_text, dictionary):
        if 'text' not in dictionary:
            dictionary['text'] = insert_text
            if 'files' not in dictionary:
                dictionary['flag'] = True
                dictionary['files'] = []
            dictionary['files'].append(file_name)
            return

        if dictionary['text'] != insert_text and insert_text != "":
            content = dict()
            content[file_name] = insert_text
            if 'files' not in dictionary:
                dictionary['flag'] = True
                dictionary['files'] = []
            if content not in dictionary['files']:
                dictionary['files'].append(content)
        elif insert_text != "":
            if 'files' not in dictionary:
                dictionary['flag'] = True
                dictionary['files'] = []
            if file_name not in dictionary['files']:
                dictionary['files'].append(file_name)

    @staticmethod
    # remove every line with document.write
    def parse_tree_dom(dictionary, dom, order, file_name, skip_tags=("br", "hr")):
        # skips None tags and unusual tags
        if dom is None or dom.tag in skip_tags:
            return

        # creates label to uniquely describe node
        dom_label = SOMLxml.create_dom_label(order, dom.tag, dom.attrib)

        # if label is in three then counter should be increased
        if dom_label in dictionary:
            dictionary[dom_label]['count'] = dictionary[dom_label]['count'] + 1
            if dictionary[dom_label]['flag']:
                insert_text = SOMLxml.filter_text_in_tree(dom)
                SOMLxml.insert_text_with_file_name(file_name, insert_text, dictionary[dom_label])
                # process_repetition_of_text(insert_text, dom_label, dom, dictionary)
                # dictionary[dom_label]['files'].append(file_name)
        # if label is not in three then it should be added to it
        else:
            dictionary[dom_label] = SOMLxml.create_new_node(dom, file_name)

        text_in_list = SOMLxml.check_text_in_list(dom)
        # if only text elements are available up to end of three
        if text_in_list is not None:
            # text should be overwrite because this one will contain much information except the same one
            SOMLxml.insert_text_with_file_name(file_name, text_in_list, dictionary[dom_label])

        # if text elements are mixed with another ones for example with divs
        else:
            # prepares for another iteration in both threes
            for order, child in enumerate(dom):
                if isinstance(child, etree.Element) and not isinstance(child, etree.Entity) and \
                        not isinstance(child, etree.Comment):
                    # new nodes will be added as children and all settings will be propagated
                    SOMLxml.parse_tree_dom(dictionary[dom_label]['children'], child, order, file_name,
                                           skip_tags=skip_tags)


class PreprocessDataset:

    @staticmethod
    def preprocess_dataset(dataset_dir, dest_path_dir):
        for category in os.listdir(dataset_dir):
            category_dir = os.path.join(dataset_dir, category)
            dest_category_dir = os.path.join(dest_path_dir, category)
            if not os.path.exists(dest_category_dir):
                os.mkdir(dest_category_dir)
            if os.path.isdir(category_dir):
                for domain in os.listdir(category_dir):
                    domain_dir = os.path.join(category_dir, domain)
                    dest_domain_dir = os.path.join(dest_category_dir, domain)
                    if not os.path.exists(dest_domain_dir):
                        os.mkdir(dest_domain_dir)
                    if os.path.isdir(domain_dir):
                        for page_name in os.listdir(domain_dir):
                            page = os.path.join(domain_dir, page_name)
                            dest_page = os.path.join(dest_domain_dir, page_name)
                            if os.path.isfile(page):
                                with open(page, "rb") as file:
                                    with open(dest_page, "w") as dest_file:
                                        for line in file:
                                            try:
                                                line = line.decode("utf-8", errors="ignore")
                                                if line.find(r"document.write") == -1:
                                                    dest_file.write(line)
                                            except UnicodeEncodeError:
                                                pass

    @staticmethod
    def test_file_filter(dest_page):
        with open(dest_page, "rb") as dest_file:
            for line in dest_file:
                try:
                    line = line.decode("utf-8", errors="ignore")
                    if line.find(r"document.write") == -1:
                        pass
                    else:
                        print(line)
                except UnicodeEncodeError:
                    print("Fail")
                    print(line)
    # @staticmethod
    # def test_regex():
    #    string = "<b>Product:</b> this"
    #    array = re.findall(r"\<\s*[^abiph][1-6]?\s*\\?\s*\>", string)


class ExtractFromTree:

    @staticmethod
    def extract_info_from_domain_file(domain_json_file, percentage_chosen, extracted_data, category, add_domain=False,
                                      domain_name=""):
        domain_json = load_as_json(domain_json_file)
        ExtractFromTree.extract_info_from_domain(domain_json, percentage_chosen, extracted_data, category, add_domain,
                                                 domain_name)

    @staticmethod
    def extract_info_from_domain(domain_json, percentage_chosen, file_content, category, add_domain=False,
                                 domain_name=""):
        whole_count = domain_json['whole_count']
        treshold = int(whole_count * percentage_chosen)
        ExtractFromTree.parse_tree_extract(domain_json, file_content, treshold, category, add_domain, domain_name)
        # save_as_json(file_content, "./example.json")

    @staticmethod
    def add_to_file_content(content_string, file_content, file_name, category, add_domain=False, domain_name="",
                            unique_texts=True):
        if add_domain:
            file_name = file_name + "_" + domain_name + "_" + category

        # creates info about new name
        if file_name not in file_content:
            file_content[file_name] = dict()
            file_content[file_name]['text'] = []

        # sets category if is not
        if 'category' not in file_content[file_name]:
            file_content[file_name]['category'] = category

        if not unique_texts or content_string not in file_content[file_name]['text']:
            file_content[file_name]['text'].append(content_string)


    @staticmethod
    def extract_info_for_file(content, file_content, treshold, category, add_domain=False, domain_name=""):
        # get first set content
        if content['count'] < treshold:
            for file_name in content['files']:
                if not isinstance(file_name, dict):
                    ExtractFromTree.add_to_file_content(content['text'], file_content, file_name, category, add_domain,
                                                        domain_name)

        # get unique content below threshold
        for file_dict1 in content['files']:
            if isinstance(file_dict1, dict):
                # only one pair
                for file_name1, text_file1 in file_dict1.items():
                    counter = 0
                    for file_dict2 in content['files']:
                        if isinstance(file_dict2, dict):
                            # only one pair
                            for file_name2, text_file2 in file_dict2.items():
                                if text_file1 == text_file2:
                                    counter = counter + 1
                    if counter < treshold:
                        ExtractFromTree.add_to_file_content(text_file1, file_content, file_name1, category, add_domain,
                                                            domain_name)

    @staticmethod
    def parse_tree_extract(domain_json, file_content, treshold, category, add_domain=False, domain_name=""):
        for name, content in domain_json.items():
            if isinstance(content, dict):
                if 'flag' in content and content['flag']:
                    ExtractFromTree.extract_info_for_file(content, file_content, treshold, category, add_domain,
                                                          domain_name)
                ExtractFromTree.parse_tree_extract(content, file_content, treshold, category, add_domain, domain_name)

    @staticmethod
    def parse_files_from_domain_directory(domain_dir, percentage_chosen, extracted_data, category, add_domain=False,
                                          regex_name=r"\.json_(.*).json$"):
        domain_name = ""
        for file in os.listdir(domain_dir):
            file_path = os.path.join(domain_dir, file)
            if os.path.isfile(file_path):
                print("Processing file: " + file)
                if add_domain:
                    domain_name = re.findall(regex_name, file)[0]
                    print("Digged name: " + str(domain_name))
                ExtractFromTree.extract_info_from_domain_file(file_path, percentage_chosen, extracted_data, category,
                                                              add_domain, domain_name)

    @staticmethod
    def extract_info_from_trees_in_weir_dataset(percentage_chosen, extracted_data_path):
        extracted_data = dict()
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/videogame", percentage_chosen, extracted_data, "videogame")
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/book", percentage_chosen, extracted_data, "book")
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/soccer", percentage_chosen, extracted_data, "soccer")
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/finance", percentage_chosen, extracted_data, "finance")
        save_as_json(extracted_data, extracted_data_path)

    @staticmethod
    def extract_info_from_trees_in_swde_dataset(percentage_chosen, extracted_data_path):
        extracted_data = dict()
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/auto", percentage_chosen, extracted_data, "auto", True)
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/book2", percentage_chosen, extracted_data, "book", True)
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/camera", percentage_chosen, extracted_data, "camera", True)
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/job", percentage_chosen, extracted_data, "job", True)
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/movie", percentage_chosen, extracted_data, "movie", True)
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/nbaplayer", percentage_chosen, extracted_data, "nbaplayer",
                                                          True)
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/restaurant", percentage_chosen, extracted_data,
                                                          "restaurant", True)
        ExtractFromTree.parse_files_from_domain_directory("../../../../../../output/pageAnalyser/university", percentage_chosen, extracted_data,
                                                          "university", True)
        save_as_json(extracted_data, extracted_data_path)


class ProcessWeirLxml:

    @staticmethod
    def parse_weir_dataset():
        ProcessWeirLxml.create_trees_for_domain_in_weir_dataset()
        ExtractFromTree.extract_info_from_trees_in_weir_dataset(0.2,
                                                                "d:\\dipldatasets\\weir\\output_beautifulsoap.json")

    @staticmethod
    def create_trees_for_domain_in_weir_dataset():
        SOMLxml.parse_tree("d:\\dipldatasets\\weir\\prepdataset\\videogame",
                           "../output/pageAnalyser/videogame/tree_videogame.json")
        SOMLxml.parse_tree("d:\\dipldatasets\\weir\\prepdataset\\book", "../output/pageAnalyser/book/tree_book.json")
        SOMLxml.parse_tree("d:\\dipldatasets\\weir\\prepdataset\\soccer",
                           "../output/pageAnalyser/soccer/tree_soccer.json")
        SOMLxml.parse_tree("d:\\dipldatasets\\weir\\prepdataset\\finance",
                           "../output/pageAnalyser/finance/tree_finance.json")


class ProcessWeirBeautifulSoup:

    @staticmethod
    def parse_weir_dataset_beautifulsoup():
        ProcessWeirBeautifulSoup.create_trees_for_domain_in_weir_dataset_beautiful_soup()
        ExtractFromTree.extract_info_from_trees_in_weir_dataset(0.2,
                                                                "d:\\dipldatasets\\weir\\output_beautifulsoap.json")

    @staticmethod
    def create_trees_for_domain_in_weir_dataset_beautiful_soup():
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\weir\\prepdataset\\videogame",
                                                   "../output/pageAnalyser/videogame/tree_videogame.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\weir\\prepdataset\\book",
                                                   "../output/pageAnalyser/book/tree_book.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\weir\\prepdataset\\soccer",
                                                   "../output/pageAnalyser/soccer/tree_soccer.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\weir\\prepdataset\\finance",
                                                   "../output/pageAnalyser/finance/tree_finance.json")


class ProcessSwdeBeautifulSoup:

    @staticmethod
    def parse_swde_dataset_beautifulsoup():
        # ProcessSwdeBeautifulSoup.create_trees_for_domain_in_swde_dataset_beautiful_soup()
        ExtractFromTree.extract_info_from_trees_in_swde_dataset(
            0.2, "d:\\dipldatasets\\swde\\output_beautifulsoap_swde.json")

    @staticmethod
    def create_trees_for_domain_in_swde_dataset_beautiful_soup():
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\swde\\dataset\\auto",
                                                   "../output/pageAnalyser/auto/tree_auto.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\swde\\dataset\\book",
                                                   "../output/pageAnalyser/book/tree_book2.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\swde\\dataset\\camera",
                                                   "../output/pageAnalyser/camera/tree_camera.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\swde\\dataset\\job",
                                                   "../output/pageAnalyser/job/tree_job.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\swde\\dataset\\movie",
                                                   "../output/pageAnalyser/movie/tree_movie.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\swde\\dataset\\nbaplayer",
                                                   "../output/pageAnalyser/nbaplayer/nbaplayer.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\swde\\dataset\\restaurant",
                                                   "../output/pageAnalyser/restaurant/tree_restaurant.json")
        SOMBeautifulSoup.parse_tree_beautiful_soup("d:\\dipldatasets\\swde\\dataset\\university",
                                                   "../output/pageAnalyser/university/tree_university.json")
        

class DivideDataset:

    @staticmethod
    def get_number_samples_for_category(input_dataset, category_name):
        sample_occurence = dict()
        for file_name, content in input_dataset.items():
            if category_name in content:
                if content[category_name] not in sample_occurence:
                    sample_occurence[content[category_name]] = 0
                sample_occurence[content[category_name]] = sample_occurence[content[category_name]] + 1
        print(sample_occurence)
        return sample_occurence

    @staticmethod
    def find_min_samples(sample_occurence):
        if len(sample_occurence) > 0:
            minimum = list(sample_occurence.values())[0]
            for category, occurence in sample_occurence.items():
                if occurence < minimum:
                    minimum = occurence
            return minimum
        return 0

    @staticmethod
    def get_text_as_category_records(input_dataset, category_name='category', text_name='text', method="join"):
        category_records = dict()
        for file_name, content in input_dataset.items():
            if category_name in content:
                if content[category_name] not in category_records:
                    category_records[content[category_name]] = []
                if method == "join":
                    category_records[content[category_name]].append(" ".join(content[text_name]))
                else:
                    category_records[content[category_name]].extend(content[text_name])
        return category_records

    @staticmethod
    def create_new_record(category, content, category_name="category", text_name="text"):
        record = dict()
        record[category_name] = category
        record[text_name] = content
        return record

    def divide_to_parts_according_category(self, json_input_file, number_train, number_test, train_output_file,
                                           test_output_file, category_name='category', text_name='text', method="join"):
        train_output = []
        test_output = []

        category_records = self.get_text_as_category_records(json_input_file, category_name, text_name, method)
        for category, content_list in category_records.items():
            random.shuffle(content_list)
        for category, content_list in category_records.items():
            for content in content_list[:number_train]:
                train_output.append(self.create_new_record(category, content, category_name, text_name))
            for content in content_list[number_train:number_test + number_train]:
                test_output.append(self.create_new_record(category, content, category_name, text_name))
        save_as_json(train_output, train_output_file)
        save_as_json(test_output, test_output_file)

    def divide_to_parts_according_percentage(self, json_input_file, train_percentage, train_output_file,
                                             test_output_file, category_name='category', text_name='text',
                                             method="join"):
        train_output = []
        test_output = []

        category_records = self.get_text_as_category_records(json_input_file, category_name, text_name, method)
        for category, content_list in category_records.items():
            random.shuffle(content_list)
        for category, content_list in category_records.items():
            number_train = int(len(content_list) * train_percentage)
            number_test = len(content_list) - number_train

            for content in content_list[:number_train]:
                train_output.append(self.create_new_record(category, content, category_name, text_name))
            for content in content_list[number_train:number_test + number_train]:
                test_output.append(self.create_new_record(category, content, category_name, text_name))
        save_as_json(train_output, train_output_file)
        save_as_json(test_output, test_output_file)

    @staticmethod
    def convert_to_dict_records(json_dataset):
        converted_dataset = dict()
        for item in json_dataset:
            record = dict()
            record['text'] = [item['text']]
            record['category'] = item['category']
            converted_dataset[item['file']] = record
        return converted_dataset

    def divide_dataset_json(self, json_input_file_path, train_output_file, test_output_file, train_percentage=0.8,
                            method="min_whole", is_in_dict=True):
        input_dataset = load_as_json(json_input_file_path)
        if not is_in_dict:
            input_dataset = self.convert_to_dict_records(input_dataset)
        samples_occurence = self.get_number_samples_for_category(input_dataset, 'category')
        if method == "min_whole":
            from_each = self.find_min_samples(samples_occurence)
            print("Min from each category is: " + str(from_each))
            number_train = int(from_each * train_percentage)
            number_test = from_each - number_train
            self.divide_to_parts_according_category(input_dataset, number_train, number_test,
                                                    train_output_file, test_output_file)
        else:
            self.divide_to_parts_according_percentage(input_dataset, train_percentage, train_output_file,
                                                      test_output_file)


def divide_dataset_weir():
    divide = DivideDataset()
    divide.divide_dataset_json("d:\\dipldatasets\\weir\\output_beautifulsoap.json",
                               "./train_beautifulsoup.json", "test_beautifulsoup.json",
                               train_percentage=0.8, method="min_whole")
    divide.divide_dataset_json("d:\\dipldatasets\\weir\\output_beautifulsoap.json",
                               "./train_beautifulsoup_whole.json", "test_beautifulsoup_whole.json",
                               train_percentage=0.8, method="whole")


def divide_dataset_swde():
    divide = DivideDataset()
    divide.divide_dataset_json("d:\\dipldatasets\\swde\\output_beautifulsoap_swde.json",
                               "./train_beautifulsoup_swde.json", "test_beautifulsoup_swde.json",
                               train_percentage=0.8, method="min_whole")
    divide.divide_dataset_json("d:\\dipldatasets\\swde\\output_beautifulsoap_swde.json",
                               "./train_beautifulsoup_swde_whole.json", "test_beautifulsoup_swde_whole.json",
                               train_percentage=0.8, method="whole")


def divide_cetd_dataset():
    divide = DivideDataset()
    divide.divide_dataset_json("./CETD/extractor.json",
                               "./train_cetd_extractor.json", "test_cetd_extractor.json",
                               train_percentage=0.8, method="min_whole", is_in_dict=False)
    divide.divide_dataset_json("./CETD/edgareExtractor.json",
                               "./train_cetd__edgare_extractor.json", "test_cetd_edgare_extractor.json",
                               train_percentage=0.8, method="min_whole", is_in_dict=False)
    divide.divide_dataset_json("./CETD/variantExtractor.json",
                               "./train_cetd_variant_extractor.json", "test_cetd_variant_extractor.json",
                               train_percentage=0.8, method="min_whole", is_in_dict=False)
    divide.divide_dataset_json("./CETD/extractor.json",
                               "./train_cetd_extractor_whole.json", "test_cetd_extractor_whole.json",
                               train_percentage=0.8, method="whole", is_in_dict=False)
    divide.divide_dataset_json("./CETD/edgareExtractor.json",
                               "./train_cetd__edgare_extractor_whole.json", "test_cetd_edgare_extractor_whole.json",
                               train_percentage=0.8, method="whole", is_in_dict=False)
    divide.divide_dataset_json("./CETD/variantExtractor.json",
                               "./train_cetd_variant_extractor_whole.json", "test_cetd_variant_extractor_whole.json",
                               train_percentage=0.8, method="whole", is_in_dict=False)


def process_weir_som_lxml():
    PreprocessDataset.preprocess_dataset("d:\\dipldatasets\\weir\\dataset\\", "d:\\dipldatasets\\weir\\prepdataset\\")
    ProcessWeirLxml.parse_weir_dataset()


def process_weir_som():
    # process_weir_som_lxml()
    ProcessWeirBeautifulSoup.parse_weir_dataset_beautifulsoup()
    divide_dataset_weir()


def process_swde_som():
    ProcessSwdeBeautifulSoup.parse_swde_dataset_beautifulsoup()
    divide_dataset_swde()


def divide_plain_text():
    divide = DivideDataset()
    divide.divide_dataset_json("./plain_text.json",
                               "./train_plain.json", "test_plain.json",
                               train_percentage=0.8, method="min_whole", is_in_dict=False)
    divide.divide_dataset_json("./plain_text.json",
                               "./train_plain_whole.json", "test_plain_whole.json",
                               train_percentage=0.8, method="whole", is_in_dict=False)


if __name__ == "__main__":
    # test_file_filter("d:\\dipldatasets\\weir\\dataset\\videogame\\games.teamxbox.com\\1000_Marble-Blast.html")
    # process_weir_som()
    # divide_cetd_dataset()
    # divide_plain_text()
    process_swde_som()
