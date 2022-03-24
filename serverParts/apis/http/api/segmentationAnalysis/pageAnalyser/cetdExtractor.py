try:
    from segmentationAnalysis.pageAnalyser.CETD.extractor import Extractor, EDGARExtractor, VariantExtractor
except ImportError:
    from apis.http.api.segmentationAnalysis.pageAnalyser.CETD.extractor import Extractor, EDGARExtractor, VariantExtractor
import os
import json


def example_test():
    ext1 = Extractor()
    ext2 = EDGARExtractor()
    ext3 = VariantExtractor()

    with open('../../../../../../output/pageAnalyser/CETD/nyt_html_sample.html', 'rb').read().decode('utf-8', errors='ignore') as file:
        sample = file.read().decode("utf-8", errors="ignore")
        extracted = ext1.extract_content(sample)
        print(extracted)

    with open('d:\\dipldatasets\\divided\\book\\bookmooch.com\\test\\0001050052.html', 'rb') as file:
        sample = file.read().decode('utf-8', errors='ignore')
        extracted1 = ext1.extract_content(sample)
        print(extracted1)
        extracted2 = ext2.extract_content(sample)
        print(extracted2)
        extracted3 = ext3.extract_content(sample)
        print(extracted3)


def apply_segmentation(html_page, methods=None, normal=None, edgare=None, variant=None):
    results = dict()
    if methods is None or 'normal' in methods:
        if normal is None:
            ext1 = Extractor()
        else:
            ext1 = normal
        try:
            results['normal'] = ext1.extract_content(html_page)
        except Exception as e:
            results['normal'] = "Error: " + str(e)
    if methods is None or 'edgare' in methods:
        if edgare is None:
            ext2 = EDGARExtractor()
        else:
            ext2 = edgare
        try:
            results['edgare'] = ext2.extract_content(html_page)
        except Exception as e:
            results['edgare'] = "Error: " + str(e)
    if methods is None or 'variant' in methods:
        if variant is None:
            ext3 = VariantExtractor()
        else:
            ext3 = variant
        try:
            results['variant'] = ext3.extract_content(html_page)
        except Exception as e:
            results['variant'] = "Error: " + str(e)

    if methods is not None:
        for method in methods:
            if method not in ['normal', 'edgare', 'variant']:
                results[method] = "Error: unknown method!"
    return results


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def create_records_and_store_according_category(categories_dir, extractor, path_to_save, after_category=False):
    result_info = []
    skipped = 0
    array = []
    for category in os.listdir(categories_dir):
        category_dir = os.path.join(categories_dir, category)
        if os.path.isdir(category_dir):
            for domain in os.listdir(category_dir):
                domain_dir = os.path.join(category_dir, domain)
                for web_page_name in os.listdir(domain_dir):
                    web_page = os.path.join(domain_dir, web_page_name)
                    with open(web_page, "rb") as file:
                        sample = file.read().decode(encoding="utf-8", errors='ignore')
                        try:
                            extracted = extractor.extract_content(sample)
                            record = dict()
                            record['file'] = web_page_name
                            record['text'] = extracted
                            record['category'] = category
                            result_info.append(record)
                        except TypeError:
                            skipped = skipped + 1
                        except AttributeError:
                            skipped = skipped + 1
                        except KeyError:
                            skipped = skipped + 1
                        except ZeroDivisionError:
                            skipped = skipped + 1
                        except PermissionError:
                            skipped = skipped + 1
                        except Exception as e:
                            print(e)
                            array.append(e)
                            skipped = skipped + 1
        if after_category:
            print("Skipped records: " + str(skipped))
            skipped = 0
            save_as_json(result_info, path_to_save + category + ".json")
            result_info = []
            print(array)

    if not after_category:
        print("Skipped records: " + str(skipped))
        save_as_json(result_info,  path_to_save)
        print(array)


def create_records_extractors(path_to_dataset, path_to_save):
    create_records_and_store_according_category(path_to_dataset, Extractor(), path_to_save + "/extractor.json")
    create_records_and_store_according_category(path_to_dataset, VariantExtractor(), path_to_save +
                                                "/variantExtractor.json", False)
    create_records_and_store_according_category(path_to_dataset, EDGARExtractor(), path_to_save +
                                                "/edgareExtractor.json", False)


if __name__ == "__main__":
    create_records_extractors("D:\\dipldatasets\\weir\\dataset", "CETD")
