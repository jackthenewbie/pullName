prompt_original= """
/no_think

Text= FACKEK, PAUL E(ARL), b. Ogden, Utah, June 22, 18; m. 42- c. 3.
From "Text" extract info of people. Each person should include:

- lastname (e.g PACKARD, ROBERT G(AY) = PACKARD)
- firstname (e.g PACKARD, ROBERT G(AY) = ROBERT GAY)
- born (e.g Feb. 25, 40. = 40)
- m (e.g. m. 54 = 1954)
- c (e.g. c. 2 = 2)

Example 1: PACKARD, ROBERT G(AY), b. Regina, N.Mex, Aug. 13, 24; m. 54.
{"lastname":"PACKARD", "firstname":"ROBERT GAY", "born": 24 "m": "54", "c": null}

Example 2: PACKARD, VERNAL S(IDNEY), JR, b. Auburn, Maine, June 10, 30; m. 57; c. 2.
{"lastname":"PACKARD", "firstname":"VERNAL SIDNEY, JR", "born": 30, "m": "57", "c": 2}

Example 3: PACKCHANLAN, A(RDZROONY) (ARTHUR), b. Armenia, Nov. 17, 00;
{"lastname":PACKCHANLAN", "firstname":"ARDZROONY ARTHUR", "born": 00, "m": null, "c": null}

For the provided Text, the output JSON array should contain ONE object for the person found.
Return a single JSON, just 1 Object, no explain nation needed
"""

prompt1="""
/no_think

Text= input 
From "Text" extract info of people. Each person should include:

- lastname (e.g PACKARD, ROBERT G(AY) = PACKARD)
- firstname (e.g., PACKARD, ROBERT G(AY) = ROBERT GAY). For the firstname, if any part is enclosed in parentheses like N(AME) or (FULLNAME), include the content inside the parentheses as part of the first name, but remove the parentheses themselves. For example, E(ARL) should result in EARL being part of the first name. So, "PAUL E(ARL)" becomes "PAUL EARL".
- born (e.g Feb. 25, 40. = 40)
- m (e.g. m. 54 = 1954)
- c (e.g. c. 2 = 2)

Example 1: PACKARD, ROBERT G(AY), b. Regina, N.Mex, Aug. 13, 24; m. 54.
{"lastname":"PACKARD", "firstname":"ROBERT GAY", "born": 24 "m": "54", "c": null}

Example 2: PACKARD, VERNAL S(IDNEY), JR, b. Auburn, Maine, June 10, 30; m. 57; c. 2.
{"lastname":"PACKARD", "firstname":"VERNAL SIDNEY, JR", "born": 30, "m": "57", "c": 2}

Example 3: PACKCHANLAN, A(RDZROONY) (ARTHUR), b. Armenia, Nov. 17, 00;
{"lastname":"PACKCHANLAN", "firstname":"ARDZROONY ARTHUR", "born": 00, "m": null, "c": null}

For the provided Text, the output JSON array should contain ONE object for the person found.
Return a single JSON, just 1 Object, no explanation needed.
If content of Text isnt a person return {}
"""

prompt2="""
/no_think

You are an expert data extraction AI. Your task is to extract information about a single person from the provided "Text".
You must return the information as a single JSON object. Do not provide any explanations or text outside of this JSON object.

Extraction Rules:
1.  **lastname**: Extract the primary surname.
    *   Example: "PACKARD, ROBERT G(AY)" -> "PACKARD"
2.  **firstname**: Extract the given name(s), including middle names or suffixes like ", JR".
    *   If any part of the first name is enclosed in parentheses, such as N(AME) or (FULLNAME), include the content *inside* the parentheses as part of the first name, but *remove* the parentheses themselves.
    *   Example: "ROBERT G(AY)" -> "ROBERT GAY"
    *   Example: "A(RDZROONY) (ARTHUR)" -> "ARDZROONY ARTHUR"
    *   Example: "VERNAL S(IDNEY), JR" -> "VERNAL SIDNEY, JR"
3.  **born**: Extract the two-digit birth year. This is typically found after "b." and a date. The output should be a number.
    *   Example: "b. Regina, N.Mex, Aug. 13, 24;" -> 24
4.  **m**: Extract the marriage year. This is typically found after "m.". The output should be a string.
    *   Example: "m. 54" -> "54"
5.  **c**: Extract the number of children. This is typically found after "c.". The output should be a number.
    *   Example: "c. 2" -> 2

Output Specifications:
- The output MUST be a single JSON object.
- Each person extracted should be one object within a JSON array, but for this task, the array will contain only ONE object for the single person found.
- If a field (lastname, firstname, born, m, c) is not present in the "Text", its value in the JSON object must be `null`.
- If the "Text" does not contain information about a person matching the expected format, or if the text is clearly not a person's record (e.g., random words, placeholder text), return an empty JSON object: `{}`.
- Provide ONLY the JSON object as the response.

Examples:

Input Text 1: PACKARD, ROBERT G(AY), b. Regina, N.Mex, Aug. 13, 24; m. 54.
Output JSON 1: {"lastname":"PACKARD", "firstname":"ROBERT GAY", "born": 24, "m": "54", "c": null}

Input Text 2: PACKARD, VERNAL S(IDNEY), JR, b. Auburn, Maine, June 10, 30; m. 57; c. 2.
Output JSON 2: {"lastname":"PACKARD", "firstname":"VERNAL SIDNEY, JR", "born": 30, "m": "57", "c": 2}

Input Text 3: PACKCHANLAN, A(RDZROONY) (ARTHUR), b. Armenia, Nov. 17, 00;
Output JSON 3: {"lastname":"PACKCHANLAN", "firstname":"ARDZROONY ARTHUR", "born": 0, "m": null, "c": null}

Input Text to Process:
Text: input
"""
def prompt(text, think):
    result_prompt = prompt2
    if(think):
        result_prompt = prompt2.replace("/no_think", "")
    return result_prompt.replace("input", text)