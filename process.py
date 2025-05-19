import json
from fetch import *
def json_from_response_of_text(text):
    ai_response = get_ai_response(text)
    extracted_json_string = None
    current_pos = len(ai_response)
    print(ai_response)
    while current_pos > 0:
        start_index = ai_response.rfind('{', 0, current_pos)
        if start_index == -1:
            break  # No '{' found
        try:
            # Attempt to decode from this point
            # raw_decode returns (python_object, index_of_end_in_substring)
            _, length = json.JSONDecoder().raw_decode(ai_response[start_index:])
            extracted_json_string = ai_response[start_index : start_index + length]
            extracted_json_string = json.loads(extracted_json_string)
            break  # Successfully extracted a JSON object string
        except json.JSONDecodeError:
            # This '{' was not the start of a valid JSON object, or json is malformed from here
            # Continue searching from before this problematic '{'
            current_pos = start_index
    return extracted_json_string
def ai_response_to_list(text):
    result = []
    answer = json_from_response_of_text(text)
    if( answer is []
        or answer["firstname"] is None 
        or answer["lastname"] is None):
        return result
    for key in answer:
        if answer[key] is None:
            answer[key] = "\u200B"
        result.append(answer[key])
    return result