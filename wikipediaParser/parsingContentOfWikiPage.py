import xml.sax
import json
import re
import copy
import token_indexing as indexing


class XMLHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.currentData = ""
        self.occurences = 0
        self.on_page_to_do = False
        self.prepared_for_indexing = False
        self.page_content = ""
        self.categories = dict()

        self.document_identifier = ""
        self.lang_document_identifier = ""
        self.text_content = ""
        self.indexes = dict()
        self.doc_freq_index = dict()
        self.title = ""

    def setJSON(self, language_shortening, term_end_file, doc_end_file):
        self.language_shortening = language_shortening
        self.language_indexes = []
        self.term_end_file = term_end_file
        self.doc_end_file = doc_end_file

    def startElement(self, tag, attributes):
        self.currentData = tag
        if tag == 'page':
            self.occurences = self.occurences + 1
            self.on_page_to_do = True
            self.text_content = ""

            if self.occurences == 1000:
                with open(self.doc_end_file, "w") as f:
                    f.write(json.dumps(self.doc_freq_index))  # FINAL DUMPING
                with open(self.term_end_file, "w") as f:
                    f.write(json.dumps(self.indexes))  # FINAL DUMPING
                exit(0)

            if self.occurences % 100 == 0:
                print(self.occurences)

    def endElement(self, tag):
        if tag == 'page':
            self.prepared_for_indexing = False
            if self.text_content != "":
                search_result = re.search(r"\[\[Category:([^\]]*)\]\]", self.text_content)
                if search_result:
                    categories_list = search_result.groups()
                    for category in categories_list:
                        if category not in self.categories:
                            self.categories[category] = dict()
                            self.categories[category]["records"] = list()
                        filtered_content = self.filter_page_content(self.text_content)
                        if filtered_content != "":
                            indexing.index_words_term_freq_doc_freq_for_category(self.indexes, self.doc_freq_index, filtered_content, category)
                            #self.categories[category]["records"].append(filtered_content)
                    if filtered_content != "":
                        indexing.index_words_term_freq_doc_freq_tfidf(self.indexes, self.doc_freq_index, filtered_content, self.title)
        self.currentData = ""

    def remove_casual_headings(self, line) -> bool:
        if re.search(r"==\s*References\s*==", line):
            return True
        if re.search(r"==\s*External links\s*==", line):
            return True
        if re.search(r"==\s*Bibliography\s*==", line):
            return True
        if re.search(r"==\s*Further reading\s*==", line):
            return True
        return False

    def filter_page_content(self, content: str):
        final_content = ""
        wikitable = False
        infobox = False
        javascript_script = False
        for line in content.split('\n'):
            if re.search(r"^\s*#\s*[rR][eE][dD][iI][rR][eE][cC][tT]", line):
                break
            if line == "" or len(line) < 2:
                continue
            if line.find("[[") != -1 and line.find("]]") != -1:
                continue
            if line.find("{{") != -1 and line.find("}}") != -1:
                continue
            if line.find("{|") != -1:
                wikitable = True
                continue
            if line.find("|}") != -1:
                wikitable = False
                continue
            if wikitable:
                continue
            if line.find("{{") != -1:
                infobox = True
                continue
            if line.find("}}") != -1:
                infobox = False
                continue
            if infobox:
                continue
            if line.find("<!--") != -1:
                javascript_script = True
                continue
            if line.find("-->") != -1:
                javascript_script = False
                continue
            if javascript_script:
                continue
            if re.search(r"^\s*\|", line) or re.search(r"^\s*\*", line):
                continue
            if re.search(r"===*\s*[^=]*\s*=*==", line):
                continue
            cleaned_content = line
            cleaned_content = cleaned_content .replace("[", "")
            cleaned_content = cleaned_content.replace("]", "")
            final_content = final_content + cleaned_content + "\n"
        return final_content

    def characters(self, content):
        if self.currentData == "title" and self.on_page_to_do \
                and re.search("^MediaWiki:", content) == None:
            self.lang_document_identifier = self.language_shortening
            self.prepared_for_indexing = True
            self.title = content

        if self.currentData == 'text' and self.prepared_for_indexing:
            # print(self.document_identifier+ "< >"+str(len(content)))
            if content != "":
                self.text_content = self.text_content + content

    def endDocument(self):
        print("Occurences: " + str(self.occurences))

        for category in self.categories.keys():
            print(category)

        # SAVE AS JSON FILE
        with open(self.doc_end_file, "w") as f:
            f.write(json.dumps(self.doc_freq_index))  # FINAL DUMPING
        with open(self.term_end_file, "w") as f:
            f.write(json.dumps(self.indexes))  # FINAL DUMPING


def prepare_titles(mapping_file, file_language_shortening, dest_language_shortenings):
    title_indexes = {}
    for dest_language_shortening in dest_language_shortenings:
        title_indexes[dest_language_shortening] = {}

    with open(mapping_file, encoding='utf-8') as indexing_file:
        json_file = json.load(indexing_file)

        for record in json_file[file_language_shortening]:
            for dest_language_shortening in dest_language_shortenings:
                if dest_language_shortening == file_language_shortening and 'id' in record:
                    title_indexes[dest_language_shortening][record['title']] = record['id']
                elif dest_language_shortening in record:
                    title_indexes[dest_language_shortening][record[dest_language_shortening]] = record['id']
    return title_indexes


def parse(language_file: str, language_array_shortenings: ['str'], term_end_file: str, doc_end_file: str):
    indexes = {}
    for dest_language_shortening in language_array_shortenings:
        indexes[dest_language_shortening] = {}
        indexes[dest_language_shortening + "_docs"] = 0

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    xml_handler = XMLHandler()
    xml_handler.setJSON(language_array_shortenings[0], term_end_file, doc_end_file)

    parser.setContentHandler(xml_handler)
    parser.parse(language_file)


if __name__ == "__main__":
    parse('D://wiki/tempexamples4.xml', ["en"], 'skIndexes.json', 'skDocIndexes.json')
