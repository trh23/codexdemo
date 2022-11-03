import streamlit as st
from codex.generate_codex import generate_one_completion_request
from codegeex.generate_codegeex import generate_codegeex_more_lines
from codex.evaluate_functional_correctness import entry_point

if 'test_examples' not in st.session_state:
    st.session_state['test_examples'] = {
        0: {'id': 0,'display': 'Select an example', 'prompt': '', 'test':''},
        1: {'id': 1, 'display': '# Code golf # implement a python function for fizz buzz def fizz_buzz(n):',
            'prompt': '# Code golf\n# implement a python function for fizz buzz\ndef fizz_buzz(n):', 'test': ''},
        2: {'id': 2, 'display': '# Code golf # For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.\n# Empty sum should be equal to 0 and empty product should be equal to 1. def sum_product(numbers: List[int]) -> Tuple[int, int]:',
            'prompt': "# language: Python\n# code golf\n# write a function that returns a tuple consisting of a sum and a product of all the integers in a list.\nfrom typing import List, Tuple\ndef sum_product(numbers: List[int]) -> Tuple[int, int]:",
            'test': "METADATA = {\n    'author': 'jt',\n    'dataset': 'test'\n}\n\n\ndef check(sum_product):\n    assert sum_product([1, 1, 1]) == (3, 1)\n    assert sum_product([100, 0]) == (100, 0)\n    assert sum_product([3, 5, 7]) == (3 + 5 + 7, 3 * 5 * 7)\n    assert sum_product([10]) == (10, 10)\n\ncheck(sum_product)"}


    }
if 'codex_prompt' not in st.session_state:
    st.session_state['codex_prompt'] = ''
if 'codex_test' not in st.session_state:
    st.session_state['codex_test'] = ''
if 'codex_display' not in st.session_state:
    st.session_state['codex_display'] = ''
if 'codegeex_prompt' not in st.session_state:
    st.session_state['codegeex_prompt'] = ''
if 'codegeex_test' not in st.session_state:
    st.session_state['codegeex_test'] = ''
if 'codegeex_display' not in st.session_state:
    st.session_state['codegeex_display'] = ''
if 'codex_result' not in st.session_state:
    st.session_state['codex_result'] = None
if 'codegeex_result' not in st.session_state:
    st.session_state['codegeex_result'] = None
if 'codex_length' not in st.session_state:
    st.session_state['codex_length'] = None
if 'codegeex_length' not in st.session_state:
    st.session_state['codegeex_length'] = None

st.set_page_config(
    page_title="Gode Golf: Codex VS CodeGeeX",
    layout="wide"
)

def generate_test_codex(codex_prompt, codex_test, codegeex_prompt, codegeex_test, col1, col2):
    # codex generation
    if codex_prompt.strip() != "":
        codex_generation = generate_one_completion_request(codex_prompt)
        codex_display = codex_prompt + "\n" + codex_generation
        st.session_state['codex_display'] = codex_display
        st.session_state['codex_length'] = len(codex_generation)
        if codex_test.strip() != "":
            result = entry_point(sample_file=codex_display, test_script=codex_test)
            st.session_state['codex_result'] = result

    # codegeex generation
    if codegeex_prompt.strip() != "":
        codegeex_generation = generate_codegeex_more_lines(codegeex_prompt, 3)
        codegeex_display = codegeex_prompt + "\n" + codegeex_generation
        st.session_state['codegeex_display'] = codegeex_display
        st.session_state['codegeex_length'] = len(codegeex_generation)
        if codegeex_test.strip() != "":
            result = entry_point(sample_file=codegeex_display, test_script=codegeex_test)
            st.session_state['codegeex_result'] = result

def change_code_input():
    example_select = st.session_state['example_select']
    if not example_select[0].isnumeric:
        pass
    id = int(example_select.split('.')[0])
    prompt = st.session_state['test_examples'][id]['prompt']
    test = st.session_state['test_examples'][id]['test']
    st.session_state['codex_prompt'] = prompt
    st.session_state['codex_test'] = test
    st.session_state['codegeex_prompt'] = prompt
    st.session_state['codegeex_test'] = test
    # st.session_state['codex_display'] = ''
    # st.session_state['codegeex_display'] = ''




st.title('Gode Golf: Codex VS CodeGeeX')

col1, col2 = st.columns(2, gap="large")


with col1:
    col1.caption("Codex")
    codex_prompt = st.text_area('Input', value=st.session_state['codex_prompt'], key='col1.codex_prompt')
    codex_test = st.text_area('Test Script', value=st.session_state['codex_test'], key='col1.codex_test')


with col2:
    col2.caption("CodeGeeX")
    codegeex_prompt = st.text_area('Input', value=st.session_state['codegeex_prompt'], key='col2.codegeex_prompt')
    codegeex_test = st.text_area('Test Script', value=st.session_state['codegeex_test'], key='col2.codegeex_test')

st.button("generate & test", on_click=generate_test_codex, args=(codex_prompt, codex_test, codegeex_prompt, codegeex_test, col1, col2))

col3, col4 = st.columns(2, gap="large")
with col3:
    col3.caption("Output")
    col3.code(st.session_state['codex_display'], language='python')

with col4:
    col4.caption("output")
    col4.code(st.session_state['codegeex_display'], language='python')

col5, col6 = st.columns(2, gap="large")
with col5:
    codex_result = st.session_state['codex_result']
    if codex_result is not None:
        if len(codex_result) == 0:
            col5.warning('No Test Script', icon="⚠️")
        else:
            if codex_result['passed']:
                col5.success("Passed!", icon="✅")
            else:
                col5.error("Failed: " + codex_result['result'], icon="🚨")

with col6:
    codegeex_result = st.session_state['codegeex_result']
    if codegeex_result is not None:
        if len(codegeex_result) == 0:
            col6.warning('No Test Script', icon="⚠️")
        else:
            if codegeex_result['passed']:
                col6.success("Passed!", icon="✅")
            else:
                col6.error("Failed: " + codegeex_result['result'], icon="🚨")


codex_length = st.session_state['codex_length']
codegeex_length = st.session_state['codegeex_length']
if codex_length is not None and codegeex_length is not None:
    # st.caption("Code Golf Result")
    col7, col8 = st.columns(2, gap="large")
    difference = codex_length - codegeex_length
    codex_win = True
    if difference > 0:
        codex_win = False
    with col7:
        col7.metric(label="chars", value=codex_length, delta=difference, delta_color='inverse')
        if codex_win:
            col7.success("Win!", icon="✅")

    with col8:
        col8.metric(label="chars", value=codegeex_length)
        if not codex_win:
            col8.success("Win!", icon="✅")



test_prompts = []
for item in st.session_state['test_examples'].values():
    if item['id'] == 0:
        test_prompts.append(item['display'])
    else:
        test_prompts.append(str(item['id']) + '. ' + item['display'])
st.selectbox("Example Inputs", test_prompts, key='example_select', on_change=change_code_input)

example_code = "def find_the_difference(self, s: str, t: str) -> str:\n    \"\"\"Given two strings s and t.\n    String t is generated by random shuffling string s and then add one more letter at a random position.\n    Return the letter that was added to t\"\"\"\n"
sample = "    c = 0\n    for cs in s:\n        c ^= ord(cs)\n    for ct in t:\n        c ^= ord(ct)\n    return chr(c)"
st.code(example_code + sample, language="python")
st.code("from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    \"\"\"\n", language='python')
