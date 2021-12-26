
def clean(filename: str, new_name: str, clusters: bool = False) -> None:
    with open(filename, "r", encoding="utf-8") as read_file:
        with open(new_name, "w", encoding="utf-8") as write_file:
            for line in read_file:
                line = line.strip()
                data_type, concept_name, data, c_name, arguments_count = line.split('\t')
                if clusters:
                    write_file.write(concept_name + "\t" + data + "\t" + data + "\n")
                else:
                    write_file.write(concept_name + "\t" + data + "\n")


def clean_output_data(filename: str, new_name: str, clusters: bool = False) -> None:
    with open(filename, "r", encoding="utf-8") as read_file:
        with open(new_name, "w", encoding="utf-8") as write_file:
            for line in read_file:
                line = line.strip()
                concept_name, data, arguments_count = line.split('\t')
                if clusters:
                    write_file.write(concept_name + "\t" + data + "\t" + data + "\n")
                else:
                    write_file.write(concept_name + "\t" + data + "\n")

if __name__ == "__main__":
    clean("uncleanedData/data0.txt", "data0.txt", False)
    clean("uncleanedData/clusters0.txt", "clusters0.txt", True)
