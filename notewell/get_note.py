import requests


def search(search_text):
    """
    :param search_text:
    :return: note's content
    """
    re = requests.get(f"https://notewell.app/notes/user_search/?search_query={search_text}")
    if re.status_code != 200:
        return "error in finding note, try another set of search parameters"
    note_id_start = re.text.find('class="mdc-card__primary-action note-card__action" href="/notes/') + 64
    note_id_end = re.text[note_id_start:].find('/') + note_id_start
    note_id = re.text[note_id_start:note_id_end]
    return get(note_id)

def get(note_id):
    note_text = {}
    re = requests.get(f"https://notewell.app/notes/{note_id}")
    note_content_start = re.text.find('<div class="note-content">') + 36
    note_content_end = re.text[note_content_start:].find('</div>') + note_content_start
    note_content = re.text[note_content_start:note_content_end]
    while note_content.find("<h") != -1:
        header_start = note_content.find("<h") + 2
        header_end = note_content[header_start:].find(">") + header_start
        note_text[note_content[header_start:header_end-4]] = ""
        text_start = note_content[header_end+1].find("<p") + header_end + 4
        text_end = note_content[text_start:].find(">") + text_start
        note_text[note_content[header_start:header_end-4]] = note_content[text_start:text_end-4]
        note_content.replace(note_content[header_start-2:text_end+1], '', 1)
    return note_text

