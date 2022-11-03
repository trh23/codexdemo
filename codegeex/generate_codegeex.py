# encoding:utf-8

import requests
import json

'''
Code Generation
'''
API_KEY = "9043777edd444212a0f4da7fb6027dd9"  # Get from Tianqi console. 从控制台获取
API_SECRET = "3d789654edbf44cfab095de61cc597d9"  # Get from Tianqi console. 从控制台获取
PROMPT = "from typing import List\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    \"\"\"\n"
NUMBER = 5
LANG = "Python"
request_url1 = "https://tianqi.aminer.cn/api/v2/"
api = 'multilingual_code_generate'

# Request is in json format. 指定请求参数格式为json


def generate_one_completion_codegeex(prompt):
    headers = {'Content-Type': 'application/json'}
    request_url = request_url1 + api
    data = {
        "apikey": API_KEY,
        "apisecret": API_SECRET,
        "prompt": prompt,
        "n": NUMBER,
        "lang": LANG
    }
    response = requests.post(request_url, headers=headers, data=json.dumps(data))
    if response:
        print(response.json())
        generated_code = ''
        for code in response.json()["result"]["output"]["code"]:
            generated_code += code + '\n'
        print(generated_code)
        return generated_code

def generate_codegeex_more_lines(original_prompt, n):
    generated_code = ''
    for i in range(n):
        generated_one_completion = generate_one_completion_codegeex(original_prompt + generated_code)
        generated_code += generated_one_completion
    generated_code = cleanup_code(generated_code)
    return generated_code

def cleanup_code(
        code: str,
        language_type: str = "Python",
        dataset: str = "humaneval",
):
    """
    Cleans up the generated code.
    """
    if language_type is None or dataset is None:
        return code

    if "humaneval" in dataset.lower():
        if language_type.lower() == "python":
            end_words = ["\ndef", "\nclass", "\nif", "\n#", "\nprint", "\nassert"]
            for w in end_words:
                if w in code:
                    code = code[:code.find(w)]
        elif language_type.lower() == "java":
            main_pos = code.find("public static void main")
            if main_pos != -1:
                code = code[:main_pos] + '}'
            if '}' in code:
                code = code[:code.rfind('}')] + '}'
            if code.count('{') + 1 == code.count('}'):
                code += "\n}"
        elif language_type.lower() == "go":
            end_words = ["\n//", "\nfunc main("]
            for w in end_words:
                if w in code:
                    code = code[:code.rfind(w)]
            if '}' in code:
                code = code[:code.rfind('}')] + '}'
        elif language_type.lower() == "cpp":
            if '}' in code:
                code = code[:code.rfind('}')] + '}'
        elif language_type.lower() == "js":
            if '}' in code:
                code = code[:code.rfind('}')] + '}'

    return code
