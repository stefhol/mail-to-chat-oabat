import os
from email import message_from_string
import bs4
from analyzer import show_text, __get_decoded_payload, show_structure, show_header
path_to_input2 = "./pages/response_outlook.eml"


def do_html(path):
    html_file = open(path, mode='r',encoding='UTF-8')
    soup_html(html_file)
def soup_html(html_file):
    plain_text = '\n'.join([line.replace("\\n", "").replace("\\r", "").strip() for line in
                            bs4.BeautifulSoup(html_file, "html.parser").find("body").get_text(strip=True,
                                                                                              separator='\n').splitlines()])
    handle_plain_text(plain_text)

def do_eml(path):
    with open(path, mode='r', encoding='UTF-8') as input_file:
        eml_content = input_file.read()
    parsed_eml = message_from_string(eml_content)
    result = __get_decoded_payload(parsed_eml=parsed_eml, content_type='text/plain')
    if result is None:
        html_code = __get_decoded_payload(parsed_eml=parsed_eml, content_type='text/html')
        soup_html(html_code)
        return

    handle_plain_text(result)



def handle_plain_text(result):

    array_coolio = [[]]
    counter = 0
    for line in result.splitlines():
        if line == "":
            counter += 1
            array_coolio.append([])
        else:
            array_coolio[counter].append(line)

    # print(result)
    print(array_coolio)

    def fun_function_that_returns_to_first_blob(blob):
        import re
        predefined_values = ['von:', 'to:', 'from:', 'zu:', 'wrote:','@oabmail.de']
        email_regex = re.compile(r'<([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+>')
        on_date_time_regex_en = re.compile(r"On \w+, \w+ \d+, \d+ at \d+:\d+ (AM|PM)")
        on_date_time_regex_de = re.compile(r"Am (\d{2}\.\d{2}\.\d{4}) um (\d{2}:\d{2}) schrieb:")

        for idx_blob in range(0,len(blob)):
            for idx_line in range(0,len(blob[idx_blob])):
                line:str = blob[idx_blob][idx_line]
                for value in predefined_values:
                    if line.lower().__contains__(value):
                        blob[idx_blob] = blob[idx_blob][0:idx_line]
                        blob = blob[0:idx_blob + 1]
                        return blob
                res_email_regex = email_regex.search(line)
                res_date_de_regex = on_date_time_regex_de.search(line)
                res_date_en_regex = on_date_time_regex_en.search(line)
                if (res_date_en_regex is not None or
                        res_date_de_regex is not None or
                        res_email_regex is not None):
                    print(res_email_regex,res_date_en_regex,res_date_de_regex)
                    blob[idx_blob] = blob[idx_blob][0:idx_line]
                    blob = blob[0:idx_blob+1]

                    return blob
        return blob
    print(
        "\n".join(
            ["\n".join(x) for x in fun_function_that_returns_to_first_blob(array_coolio)]
        ),
    )
for filename in os.listdir('pages'):
    f = os.path.join('pages', filename)
    # checking if it is a file
    if os.path.isfile(f):
        if os.path.splitext(f)[1] == '.eml':
            print(os.path.basename(f))
            try:
                do_html(f)
            except:
                do_eml(f)
            print("-"*100)

