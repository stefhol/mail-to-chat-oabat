from email import message_from_string

from analyzer import show_text, __get_decoded_payload, show_structure, show_header

path_to_input = "./pages/response_6.eml"
with open(path_to_input, mode='r') as input_file:
    eml_content = input_file.read()
parsed_eml = message_from_string(eml_content)
result = __get_decoded_payload(parsed_eml=parsed_eml, content_type='text/plain')
# print(result)
# result = result.split("Sie haben eine neue Nachricht!")[0]
# result = "\n".join([x.strip() for x in result.splitlines()])


import re
hash = ['von:','to:','from:','zu:']
p = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
array_coolio = []
array_coolio.append([])
counter = 0
for idx in result.splitlines():
    if idx == "":
        counter += 1
        array_coolio.append([])
    else:
        array_coolio[counter].append(idx)


# print(result)

def fun_function_that_returns_to_first_blob(array_coolio):
    for idx in range(0, len(array_coolio)):
        for idx_2 in range(0, len(array_coolio[idx])):
            target_string:str = array_coolio[idx][idx_2]
            match = p.search(target_string)
            if match is not None:
                found = False
                for x in hash:
                    if target_string.lower().find(x) > -1:
                        found = True
                if(found):
                    array_coolio = [array_coolio[f] for f in range(0, idx)]
                    return array_coolio


print(
    "\n".join(
        ["\n".join(x) for x in fun_function_that_returns_to_first_blob(array_coolio)]
    )
)
