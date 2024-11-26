from bs4 import BeautifulSoup

MAX_LEN = 4096


def split_html_message(source_html: str, max_len=MAX_LEN):
    soup = BeautifulSoup(source_html, 'html.parser')
    fragments = []
    current_fragment = ""
    current_length = 0

    def add_to_fragment(element):
        nonlocal current_fragment, current_length
        element_str = str(element)
        element_len = len(element_str)

        if current_length + element_len > max_len:
            fragments.append(current_fragment)
            current_fragment = ""
            current_length = 0

        current_fragment += element_str
        current_length += element_len

    for child in soup.body or soup:
        add_to_fragment(child)

    if current_fragment:
        fragments.append(current_fragment)

    return fragments


source_file_path = './source.html'
with open(source_file_path, 'r', encoding='utf-8') as file:
    source_html = file.read()

html_fragments = split_html_message(source_html)

for i, fragment in enumerate(html_fragments, start=1):
    print(f"Fragment #{i} ({len(fragment)} chars):\n{fragment}\n{'-' * 40}")