def filterInformationList(information_list):

    # remove duplicates
    filtered_list = list(dict.fromkeys(information_list))
    return filtered_list

def cleanLine(line):
    line = line.strip('\n')
    return line


def parse_information(information_text_file_path):
    information_list = []
    with open(information_text_file_path) as fp:
        Lines = fp.readlines()
        for line in Lines:
            cleaned_line = cleanLine(line)
            if len(cleaned_line) != 0:
                information_list.append(cleaned_line)

    information_list_filtered = filterInformationList(information_list)
    print("\n> Entered information items ({} items in total) :".format(len(information_list_filtered)))
    for i in range(len(information_list_filtered)):
        print(" {}.  {}".format(i + 1, information_list_filtered[i]))
    print("\n")
    return information_list_filtered


if __name__ == "__main__":
    information_text_file_path = r"C:\Users\jixin\Documents\GitHub\microt_preprocessing\sample_file\watch_information_sample"
    information_list = parse_information(information_text_file_path)

