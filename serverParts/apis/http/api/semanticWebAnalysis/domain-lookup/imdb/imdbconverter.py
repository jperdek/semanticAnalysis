
import os


def process_name_basics(name_basics_file, output_main_file_csv, output_roles_file, output_title_mappings_file,
                        template_main, template_role, template_mapping,
                        output_main_file_ttl, output_role_file_ttl, output_mapping_file_ttl):
    process_name_basics_file(name_basics_file, output_main_file_csv, output_roles_file, output_title_mappings_file)
    convert_to_ttl(template_main, output_main_file_csv, output_main_file_ttl)
    convert_to_ttl(template_role, output_roles_file, output_role_file_ttl)
    convert_to_ttl(template_mapping, output_title_mappings_file, output_mapping_file_ttl)


def process_name_basics_file(name_basics_file, output_main_file, output_roles_file, output_title_mappings_file,
                             role_predicate_imdb="imdb:hasRole", separator_role=",",
                             mapping_predicate_imdb="imdb:assocTitle", separator_maping=","):
    with open(output_main_file, "w", encoding="utf-8") as output_main:
        with open(output_roles_file, "w", encoding="utf-8") as output_roles:
            with open(output_title_mappings_file, "w", encoding="utf-8") as output_mappings:
                with open(name_basics_file, "r", encoding="utf-8") as input_file:
                    for line in input_file:
                        array = line.split('\t')
                        array[2] = array[2].replace('\\N', '0000')
                        array[3] = array[3].replace('\\N', '0000')
                        roles = array[4].replace('\n', '')  # + namespace_imdb + ':')
                        titles = array[5].replace('\n', '')  # + namespace_imdb + ':')

                        for role in roles.split(','):
                            if role.find('\\N') < 0 and role != "":
                                output_roles.write(array[0] + separator_role + role_predicate_imdb + separator_role +
                                                   role + "\n")
                        for title in titles.split(','):
                            if title.find('\\N') < 0 and title != "":
                                output_mappings.write(array[0] + separator_role + mapping_predicate_imdb +
                                                      separator_maping + title + "\n")

                        output_main.write(",".join(array[:4]) + "\n")


def process_title_crew(title_crew_file, output_directors_csv, output_writers_csv, template_directors, template_writers,
                       output_directors_ttl, output_writers_ttl):
    process_title_crew_file(title_crew_file, output_directors_csv, output_writers_csv)
    convert_to_ttl(template_directors, output_directors_csv, output_directors_ttl)
    convert_to_ttl(template_writers, output_writers_csv, output_writers_ttl)


def process_title_crew_file(title_crew_file, output_directors_csv, output_writers_csv,
                            directors_predicate_imdb="imdb:hasRole", separator_directors=",",
                            writers_predicate_imdb="imdb:assocTitle", separator_writers=","):
    with open(output_directors_csv, "w", encoding="utf-8") as output_directors:
        with open(output_writers_csv, "w", encoding="utf-8") as output_writers:
            with open(title_crew_file, "r", encoding="utf-8") as input_file:
                for line in input_file:
                    array = line.split('\t')
                    directors = array[1].replace('\n', '')  # + namespace_imdb + ':')
                    writers = array[2].replace('\n', '')  # + namespace_imdb + ':')

                    for director in directors.split(','):
                        if director.find('\\N') < 0 and director != "":
                            output_directors.write(array[0] + separator_directors + directors_predicate_imdb +
                                                   separator_directors + director + "\n")
                    for writer in writers.split(','):
                        if writer.find('\\N') < 0 and writer != "":
                            output_writers.write(array[0] + separator_writers + writers_predicate_imdb +
                                                 separator_writers + writer + "\n")


def process_title_basics(title_basics_file, template_title, output_main_file, output_main_file_ttl):
    process_title_basics_file(title_basics_file, output_main_file)
    convert_to_ttl(template_title, output_main_file, output_main_file_ttl, "-Xmx2048m", "|")


def process_title_basics_file(title_basics_file, output_main_file):
    with open(output_main_file, "w", encoding="utf-8") as output_main:
        with open(title_basics_file, "r", encoding="utf-8") as input_file:
            for line in input_file:
                array = line.replace('\\N', '0000').replace('\t', '|').replace('\n', '') + "|\n"
                # genres = array[8].replace('\n', '').split(',')
                output_main.write(array)
                # for genre in genres:
                #    if genre != "":
                #        output_main.write("|".join(array[:8]) + "|" + genre + "|\n")


def process_with_checking_file(title_basics_file, output_main_file, columns, separator="|", add_separators=False):
    columns = columns - 1
    separators = ""
    if add_separators:
        for i in range(0, columns + 1):
            separators = separators + separator
    with open(output_main_file, "w", encoding="utf-8") as output_main:
        with open(title_basics_file, "r", encoding="utf-8") as input_file:
            for line in input_file:
                processed_line = line.replace('\\N', '0000').replace('\t', separator).replace('\n', '')
                count = processed_line.count(separator)
                if count < columns:
                    print("Line skipped: "+line)
                    continue
                elif count > columns:
                    print("Separator should be changed! " + line)

                processed_line = processed_line + separators + "\n"
                output_main.write(processed_line)


def process_standard_template(source_file, template_file, output_file, output_file_ttl):
    write_with_another_separator(source_file, output_file)
    convert_to_ttl(template_file, output_file, output_file_ttl)


def process_with_checking(title_basics_file, template_title, output_main_file, output_main_file_ttl, columns,
                          another_separator="^"):
    process_with_checking_file(title_basics_file, output_main_file, columns, another_separator, True)
    convert_to_ttl(template_title, output_main_file, output_main_file_ttl, "", another_separator)


def write_with_another_separator(input_file, output_file, first_separator="\t", final_separator=","):
    with open(output_file, "w", encoding="utf-8") as output_file_f:
        with open(input_file, "r", encoding="utf-8") as input_file_f:
            for line in input_file_f:
                output_file_f.write(line.replace('\\N', '0000').replace(first_separator, final_separator))


def convert_to_ttl(template_ttl, csv_file, output_file, memory="", separator=','):
    os.system("java " + memory + " -jar  ../csv2rdf/lib/csv2rdf.jar --separator=\"" + separator + "\" " + template_ttl
              + " " + csv_file + " " + output_file)


def process_imdb_core():
    process_name_basics("d:/dipldatasets/imdb/namebasics.tsv", "d:/dipldatasets/imdb/namebasics.csv",
                        "d:/dipldatasets/imdb/roles.csv", "d:/dipldatasets/imdb/nameTitles.csv",
                        "./templates/nameBasics.ttl", "./templates/roleTemplate.ttl",
                        "./templates/mappingTemplate.ttl", "d:/dipldatasets/imdb/conversion/nameBasics.ttl",
                        "d:/dipldatasets/imdb/conversion/nameRole.ttl",
                        "d:/dipldatasets/imdb/conversion/nameMapping.ttl")
    process_title_crew("d:/dipldatasets/imdb/titlecrew.tsv", "d:/dipldatasets/imdb/directors.csv",
                       "d:/dipldatasets/imdb/writers.csv", "./templates/directorsTemplate.ttl",
                       "./templates/writersTemplate.ttl", "d:/dipldatasets/imdb/conversion/directors.ttl",
                       "d:/dipldatasets/imdb/conversion/writers.ttl")
    process_title_basics("d:/dipldatasets/imdb/titlebasics.tsv", "./templates/titleBasicsTemplate.ttl",
                         "d:/dipldatasets/imdb/titlebasics.csv", "d:/dipldatasets/imdb/conversion/titleBasics.ttl")
    process_standard_template("d:/dipldatasets/imdb/titleprincipals.tsv", "templates/titlePrincipalsTemplate.ttl",
                              "d:/dipldatasets/imdb/titleprincipals.csv",
                              "d:/dipldatasets/imdb/conversion/titlePrincipals.ttl")


def process_imdb_additional_files():
    process_standard_template("d:/dipldatasets/imdb/titleratings.tsv", "templates/titleRatingsTemplate.ttl",
                              "d:/dipldatasets/imdb/titleratings.csv",
                              "d:/dipldatasets/imdb/conversion/titleRatings.ttl")
    process_standard_template("d:/dipldatasets/imdb/titleepisode.tsv", "templates/titleSeriesTemplate.ttl",
                              "d:/dipldatasets/imdb/titleepisode.csv",
                              "d:/dipldatasets/imdb/conversion/titleEpisode.ttl")
    # exception Out of bounds in jar file
    process_with_checking("d:/dipldatasets/imdb/titleakas.tsv", "./templates/titleAkasTemplate.ttl",
                          "d:/dipldatasets/imdb/titleakas.csv", "d:/dipldatasets/imdb/conversion/titleAkas.ttl", 8)


def process_imdb():
    process_imdb_core()
    process_imdb_additional_files()


if __name__ == "__main__":
    process_imdb()
