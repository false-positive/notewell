import xml.etree.ElementTree as ET
import pke

subject = "Oxygen"
subject_xml = 'Wikipedia Articles/' + subject + '.xml'
tree = ET.parse(subject_xml)
root = tree.getroot()
raw_text = ""
output = open(subject + '.txt', "w", encoding="utf-8")

def _clear_ref_tags(text):
    text = text.replace("&nbsp;", ' ')
    text = text.replace("'''", ' ')
    text = text.replace("''", ' ')
    if text.find("==See also==") != -1:
        text = text.replace(text[text.find("==See also=="):len(text)], '')
    elif text.find("== See also ==") != -1:
        text = text.replace(text[text.find("== See also =="):len(text)], '')
    while text.find("{") != -1 and text.find("}") != -1:
        start_idx = text.find("{")
        while text[start_idx+1:].find("{") < text[start_idx+1:].find("}") and text[start_idx + 1:].find("{") != -1:
            tmp_substring = text[start_idx+1:].replace('{', '', 1)
            tmp_substring = tmp_substring.replace('}', '', 1)
            text = text[:start_idx+1] + tmp_substring
        end_idx = start_idx + text[start_idx:].find("}")
        substring = text[start_idx:end_idx + 1]
        text = text.replace(substring, '')
    while text.find("<br") != -1:
        start_idx = text.find("<br")
        end_idx = start_idx + text[start_idx:].find("/>") + 2
        substring = text[start_idx:end_idx]
        text = text.replace(substring, '', 1)
    while text.find("<ref") != -1:
        start_idx = text.find("<ref")
        end_idx = start_idx + text[start_idx:].find("/>")+2
        if text.find("</ref>") != -1 and (text.find("</ref>") < end_idx  or end_idx == 1 or text.find("/>") < start_idx):
            end_idx = start_idx + text[start_idx:].find("</ref>") + 6
        substring = text[start_idx:end_idx]
        text = text.replace(substring, '', 1)
    while text.find("<sup") != -1:
        start_idx = text.find("<sup")
        end_idx = text.find("/>") + 2
        if text.find("</sup>") < end_idx or end_idx == 1 or text.find("/>") < start_idx:
            end_idx = text.find("</sup>") + 6
        substring = text[start_idx:end_idx]
        text = text.replace(substring, '', 1)
    return text


def _clear_redirects(text):
    while text.find("[[") != -1:
        start_idx = text.find("[[")
        end_idx = start_idx + text[start_idx:].find("]]") + 2
        while text[start_idx + 2: end_idx].find("[[") != -1:
            text = text[:start_idx + 2] + text[start_idx + 2:].replace("[[", '', 1)
            text = text[:start_idx + 2] + text[start_idx + 2:].replace("]]", '', 1)
            end_idx = text.find("]]") + 2
        dump_text = text[start_idx:end_idx]
        if text[start_idx:end_idx].find("|") != -1 and text[start_idx:end_idx].find("File") == -1:
            temp_start_indx = text[start_idx:end_idx].find("|")
            if text[start_idx + temp_start_indx:end_idx - 2].find("{") == -1:
                start_idx += temp_start_indx-1
            else:
                end_idx -= temp_start_indx+1
        replace_text = text[start_idx + 2:end_idx - 2]
        if text[start_idx:end_idx].find("[[File") != -1:
            replace_text = ''
        text = text.replace(dump_text, replace_text, 1)
    text = text.replace('\n', '')
    return text


def _separate_text(text):
    s_text = {}
    s_text['Summary'] = {}
    s_text['Summary']['text'] = text[:text.find("==")]
    text = text.replace(text[:text.find("==") + 2], '', 1)
    while text.find("==") != -1:
        tmp_key = text[:text.find('==')]
        text = text.replace(text[:text.find('==') + 2], '', 1)
        if text.find("==") >= text.find("==="):
            s_text[tmp_key] = {}
            s_text[tmp_key]['text'] = text[:text.find("===")]
            while text.find("==") >= text.find("===") and text.find("===") != -1:
                text = text.replace(text[:text.find('===') + 3], '', 1)
                if text.find(" ===") == -1 or text.find('===') < text.find(' ==='):
                    sec_tmp_key = text[:text.find('===')].replace('  ', '')
                else:
                    sec_tmp_key = text[:text.find(' ===')].replace('  ', '')
                text = text.replace(text[:text.find('===') + 3], '', 1)
                if text.find("==") < text.find("==="):
                    s_text[tmp_key][sec_tmp_key] = text[:text.find("==")]
                else:
                    s_text[tmp_key][sec_tmp_key] = text[:text.find("===")]
            text = text.replace(text[:text.find("==") + 2], '', 1)
        else:
            s_text[tmp_key] = {}
            s_text[tmp_key]['text'] = text[:text.find("==")]
            text = text.replace(text[:text.find("==") + 2], '', 1)
    return s_text


def _parse(text):
    text = _clear_ref_tags(text)
    text = _clear_redirects(text)
    s_text = _separate_text(text)
    return s_text


def _extract(segmented_text):
    max_n = 40
    for title in segmented_text:
        for key in segmented_text[title]:
            n_chars = len(segmented_text[title][key].replace(' ', ''))
            #print(f"title: {title}, key: {key}, number of chars: {n_chars}")
            if n_chars > 50:
                if int(n_chars/125) > max_n:
                    n_keywords = max_n
                else:
                    n_keywords = int(n_chars/125)
                extractor = pke.unsupervised.TopicRank()
                extractor.load_document(segmented_text[title][key])
                extractor.candidate_selection()
                extractor.candidate_weighting()
                key_phrases = extractor.get_n_best(n=n_keywords)
                for tple in key_phrases:
                    output.write(tple[0] + ' ')


def parse():
    i = 0
    for parent in root:
        p_clean_tag = parent.tag
        p_clean_tag = p_clean_tag.replace(p_clean_tag[p_clean_tag.find('{'):p_clean_tag.find('}') + 1], '')
        if p_clean_tag == "page":
            for child in parent[3]:
                clean_tag = child.tag
                clean_tag = clean_tag.replace(clean_tag[clean_tag.find('{'):clean_tag.find('}') + 1], '')
                if clean_tag == "text":
                    i += 1
                    raw_text = child.text
                    s_text = _parse(raw_text)
                    _extract(s_text)
                    print(f"ready!, iteration: {i}")

parse()

print("ready!!!")
'''segmented_text = parse(raw_text)


extractor.candidate_selection()
extractor.candidate_weighting()
key_phrases = extractor.get_n_best(n=20)
for tple in key_phrases:
    print(tple[0])
'''