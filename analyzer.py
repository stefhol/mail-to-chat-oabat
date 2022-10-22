from email.message import Message
import re


def show_header(parsed_eml: Message):
    max_key_width = max([len(x) for x, _ in parsed_eml.items()])
    for key, value in parsed_eml.items():
        values_in_lines = value.split('\n')
        first_value = values_in_lines.pop(0)
        for x in values_in_lines:
            x = x.replace('\t', '').strip().replace('\r', '').strip(' ')
            print((max_key_width + 5) * ' ' + x)
    print()


def show_structure(parsed_eml: Message):
    __show_structure(parsed_eml=parsed_eml)
    print()


def __show_structure(parsed_eml: Message, level=0):
    filename = parsed_eml.get_filename()
    type_with_intend = level*'|  ' + '|- {}'.format(parsed_eml.get_content_type())
    print(type_with_intend.ljust(40), filename)
    if parsed_eml.is_multipart():
        for child in parsed_eml.get_payload():
            __show_structure(parsed_eml=child, level=level+1)


def check_tracking(parsed_eml: Message):
    sources = set()
    html_str = __get_decoded_payload(parsed_eml=parsed_eml, content_type='text/html')
    if html_str is None:
        print('Email contains no HTML')
    else:
        for pattern in [r'src="(.+?)"', r"src='(.+?)'", r'background="(.+?)"', r"background='(.+?)'"]:
            for match in re.finditer(pattern, html_str):
                if not match.group(1).startswith('cid:'):
                    sources.add(match.group(1))
        if len(sources) == 0:
            print()
        for x in sources:
            print('-'+x)
    print()


def show_urls(parsed_eml: Message):
    all_links = set()
    html_str = __get_decoded_payload(parsed_eml=parsed_eml, content_type='text/html')
    if html_str is None:
        print()
    else:
        for pattern in [r'href="(.+?)"', r"href='(.+?)'"]:
            for match in re.finditer(pattern, html_str):
                all_links.add(match.group(1))
        if len(all_links) == 0:
            print()
        for x in all_links:
            print(' - '+x)
    print()


def show_text(parsed_eml: Message):
    text = __get_decoded_payload(parsed_eml=parsed_eml, content_type='text/plain')

    if text is None:
        print()
    else:
        print(text)
    print()


def show_html(parsed_eml: Message):
    html = __get_decoded_payload(parsed_eml=parsed_eml, content_type='text/html')
    if html is None:
        print()
    else:
        print(html)
    print()


def __get_decoded_payload(parsed_eml: Message, content_type: str) -> str or None:
    if parsed_eml.get_content_type() == content_type:
        html_in_bytes = parsed_eml.get_payload(decode=True)
        return __try_to_decode(content=html_in_bytes, parsed_eml=parsed_eml)
    if type(parsed_eml.get_payload()) is not list:
        return
    for sub_element in parsed_eml.get_payload():
        result = __get_decoded_payload(parsed_eml=sub_element, content_type=content_type)
        if result is not None:
            return result


def __try_to_decode(content: bytes, parsed_eml: Message) -> str or None:
    list_of_possible_encodings = __create_list_of_possible_encodings(parsed_eml=parsed_eml)

    for encoding_format in list_of_possible_encodings:
        try:
            return content.decode(encoding_format)
        except ValueError:
            continue
    return None


def __create_list_of_possible_encodings(parsed_eml: Message) -> set:
    """ creates a list of the most possible encodings of the payload """
    list_of_possible_encodings = set()

    # at first add the encodings mentioned in the object header
    for k, v in parsed_eml.items():
        k = str(k).lower()
        v = str(v).lower()
        if k == 'content-type':
            entries = v.split(';')
            for entry in entries:
                entry = entry.strip()
                if entry.startswith('charset='):
                    encoding = entry.replace('charset=', '').replace('"', '')
                    list_of_possible_encodings.add(encoding)

    for x in ['utf-8', 'windows-1251', 'iso-8859-1', 'us-ascii', 'iso-8859-15']:
        if x not in list_of_possible_encodings:
            list_of_possible_encodings.add(x)

    return list_of_possible_encodings



