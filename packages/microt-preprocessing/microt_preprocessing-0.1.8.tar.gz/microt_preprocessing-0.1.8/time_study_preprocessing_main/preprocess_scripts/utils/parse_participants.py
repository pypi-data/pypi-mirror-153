suffix = "@timestudy_com"


def filterParticipantList(p_id_list):
    filtered_list = []

    # check suffix
    for p_id in p_id_list:
        if not p_id.endswith(suffix):
            filtered_list.append(p_id)
        else:
            print(
                "warning: participant ID  ( {} ) doesn't need suffix \"{}\". The program will automatically strip the "
                "suffix for each participant ID.".format(
                    p_id, suffix))
            filtered_list.append(p_id.replace(suffix, ''))

    # remove duplicates
    filtered_list = list(dict.fromkeys(filtered_list))
    return filtered_list


def cleanLine(line):
    line = line.strip('\n')
    return line


def parse_participants(participant_text_file_path):
    p_id_list = []
    with open(participant_text_file_path) as fp:
        Lines = fp.readlines()
        for line in Lines:
            cleaned_line = cleanLine(line)
            if len(cleaned_line) != 0:
                p_id_list.append(cleaned_line)

    p_id_list_filtered = filterParticipantList(p_id_list)
    # add suffix
    p_id_list_with_suffix = [x + suffix for x in p_id_list_filtered]
    print("\n> Entered Participant IDs ({} participants in total) :".format(len(p_id_list_with_suffix)))
    for i in range(len(p_id_list_with_suffix)):
        print(" {}.  {}".format(i + 1, p_id_list_with_suffix[i]))
    print("\n")
    return p_id_list_with_suffix


if __name__ == "__main__":
    participant_text_file_path = r"C:\Users\jixin\Documents\GitHub\microt_preprocessing\resource\sample_file" \
                                 r"\participants_sample "
    p_id_list = parse_participants(participant_text_file_path)
