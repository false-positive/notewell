
new_dataset = open("new_dataset.txt", "a+", encoding="utf-8")


def write_lines(k_title):
    keywords = open(k_title + ".txt", "r", encoding="utf-8")
    keywords = keywords.readlines()[0].split("; ")
    i = 0
    line_output = '{"text": "'
    for keyword in keywords:
        line_output += keyword + ' '
        i += 1
        if i % 10 == 0:
            line_output += '", "label": "' + k_title + '", "metadata": []}'
            new_dataset.write(line_output + '\n')
            line_output = '{"text": "'


write_lines("Chemistry")
write_lines("Biology")
write_lines("Physics")
write_lines("Computer Science")
