from functools import reduce
from typing import List, Tuple
import streamlit as st
import requests
from codegeex.generate_codegeex import cleanup_code

def generate_one_completion_request(code_promt, model_name):
    url = 'https://api.openai.com/v1/completions'
    myobj = {      'model': model_name,
      'prompt': code_promt,
      'temperature': 0.8,
      'top_p': 0.95,
      'max_tokens': 1024,
#       stop = ['\nclass', '\ndef', '\n#', '\nif', '\nprint'],
      'n': 1}

    x = requests.post(url,
      headers={'Content-Type':'application/json',
               'Authorization': 'Bearer ' + st.secrets['CODEX']},
                json=myobj)

    stop_sequences = ['\nclass', '\ndef', '\n#', '\nif', '\nprint']
    text = x.json()
#     print(text)
#     if 'choices' in text:
#         text = text['choices'][0]['text']
#         index = None
#         for sequence in stop_sequences:
#             cur_index = text.find(sequence)
#             if cur_index != -1 and (index == None or index > cur_index):
#                 index = cur_index
#         if index == None:
#             index = -1
#
#         return text[0:index]
#     else:
#         return ""
    if 'choices' in text:
        text = text['choices'][0]['text']
        return cleanup_code(text)
    else:
        return ""

def sum_product(numbers: List[int]) -> Tuple[int, int]:

    sum = reduce(lambda a, b : a + b, numbers)
    product = reduce(lambda a, b: a * b, numbers)
    return sum, product



if __name__ == '__main__':
    print(sum_product([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
