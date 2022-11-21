import streamlit as st
from codex.generate_codex import generate_one_completion_request
from codegeex.generate_codegeex import generate_codegeex_more_lines
from codex.evaluate_functional_correctness import entry_point

if 'test_examples' not in st.session_state:
    st.session_state['test_examples'] = {
        0: {'id': 0,'display': 'Select an example', 'prompt': '', 'test':''},
        1: {'id': 1, 'display': '# language: Python\n# implement a python function for fizz buzz def fizz_buzz(n):',
            'prompt': '# implement a python function for fizz buzz\ndef fizz_buzz(n):', 'test': ''},
        2: {'id': 2, 'display': '# language: Python\n# For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.\n# Empty sum should be equal to 0 and empty product should be equal to 1. def sum_product(numbers: List[int]) -> Tuple[int, int]:',
            'prompt': "# language: Python\n# write a function that returns a tuple consisting of a sum and a product of all the integers in a list.\nfrom typing import List, Tuple\ndef sum_product(numbers: List[int]) -> Tuple[int, int]:",
            'test': "def check(sum_product):\n    assert sum_product([1, 1, 1]) == (3, 1)\n    assert sum_product([100, 0]) == (100, 0)\n    assert sum_product([3, 5, 7]) == (3 + 5 + 7, 3 * 5 * 7)\n    assert sum_product([10]) == (10, 10)\n\ncheck(sum_product)"},
        3: {'id': 3, 'display': "from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    \"\"\"\n",
            'prompt': "# language: Python\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    \"\"\"\n",
            'test': "def check(candidate):\n    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True\n    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False\n    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True\n    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False\n    assert candidate([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True\n    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True\n    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False\ncheck(has_close_elements)\n"},
        4: {'id':4, 'display': "from typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups('( ) (( )) (( )( ))')\n    ['()', '(())', '(()())']\n    \"\"\"\n",
            'prompt': "# language: Python\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups('( ) (( )) (( )( ))')\n    ['()', '(())', '(()())']\n    \"\"\"\n",
            'test': "def check(separate_paren_groups):\n    assert separate_paren_groups('(()()) ((())) () ((())()())') == [\n        '(()())', '((()))', '()', '((())()())'\n    ]\n    assert separate_paren_groups('() (()) ((())) (((())))') == [\n        '()', '(())', '((()))', '(((())))'\n    ]\n    assert separate_paren_groups('(()(())((())))') == [\n        '(()(())((())))'\n    ]\n    assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']\n\ncheck(separate_paren_groups)"},
        5: {'id':5, 'display': "\n\ndef truncate_number(number: float) -> float:\n    \"\"\" Given a positive floating point number, it can be decomposed into\n    and integer part (largest integer smaller than given number) and decimals\n    (leftover part always smaller than 1).\n\n    Return the decimal part of the number.\n    >>> truncate_number(3.5)\n    0.5\n    \"\"\"\n",
            'prompt': "# language: Python\ndef truncate_number(number: float) -> float:\n    \"\"\" Given a positive floating point number, it can be decomposed into\n    and integer part (largest integer smaller than given number) and decimals\n    (leftover part always smaller than 1).\n\n    Return the decimal part of the number.\n    >>> truncate_number(3.5)\n    0.5\n    \"\"\"\n",
            'test': "def check(truncate_number):\n    assert truncate_number(3.5) == 0.5\n    assert abs(truncate_number(1.33) - 0.33) < 1e-6\n    assert abs(truncate_number(123.456) - 0.456) < 1e-6\n\ncheck(truncate_number)"},
        6: {'id':6, 'display': "\n\ndef string_sequence(n: int) -> str:\n    \"\"\" Return a string containing space-delimited numbers starting from 0 upto n inclusive.\n    >>> string_sequence(0)\n    '0'\n    >>> string_sequence(5)\n    '0 1 2 3 4 5'\n    \"\"\"\n",
            'prompt': "# language: Python\ndef string_sequence(n: int) -> str:\n    \"\"\" Return a string containing space-delimited numbers starting from 0 upto n inclusive.\n    >>> string_sequence(0)\n    '0'\n    >>> string_sequence(5)\n    '0 1 2 3 4 5'\n    \"\"\"\n",
            'test': "def check(string_sequence):\n    assert string_sequence(0) == '0'\n    assert string_sequence(3) == '0 1 2 3'\n    assert string_sequence(10) == '0 1 2 3 4 5 6 7 8 9 10'\n\ncheck(string_sequence)"}
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
if 'code_golf' not in st.session_state:
    st.session_state['code_golf'] = True

st.set_page_config(
    page_title="Gode Golf: Codex VS CodeGeeX",
    layout="wide"
)

def generate_test_codex(codex_prompt, codex_test, codegeex_prompt, codegeex_test, col1, col2):
    # codex generation
    if codex_prompt.strip() != "":
        input = ""
        if st.session_state['code_golf']:
            codex_prompt = "# Code golf\n" + codex_prompt
            input = codex_prompt
        else:
            input = "#verbose code\n" + codex_prompt
        model_name = 'code-davinci-002'
        codex_generation = generate_one_completion_request(input, model_name)
        codex_display = codex_prompt + "\n" + codex_generation
        st.session_state['codex_display'] = codex_display
        st.session_state['codex_length'] = len(codex_generation)
        if codex_test.strip() != "":
            result = entry_point(sample_file=codex_display, test_script=codex_test)
            st.session_state['codex_result'] = result
        else:
            st.session_state['codex_result'] = ""

    # codegeex generation
    if codegeex_prompt.strip() != "":
        input = ""
        if st.session_state['code_golf']:
            codegeex_prompt = "# Code golf\n" + codegeex_prompt
            input = codegeex_prompt
        else:
            input = "#verbose code\n" + codegeex_prompt
        # codegeex_generation = generate_codegeex_more_lines(codegeex_prompt, 3)
        model_name = 'code-cushman-001'
        codegeex_generation = generate_one_completion_request(input, model_name)
        codegeex_display = codegeex_prompt + "\n" + codegeex_generation
        st.session_state['codegeex_display'] = codegeex_display
        st.session_state['codegeex_length'] = len(codegeex_generation)
        if codegeex_test.strip() != "":
            result = entry_point(sample_file=codegeex_display, test_script=codegeex_test)
            st.session_state['codegeex_result'] = result
        else:
            st.session_state['codegeex_result'] = ""

def change_code_input():
    example_select = st.session_state['example_select']
    if example_select[0].isnumeric():
        id = int(example_select.split('.')[0])
        prompt = st.session_state['test_examples'][id]['prompt']
        test = st.session_state['test_examples'][id]['test']
        st.session_state['codex_prompt'] = prompt
        st.session_state['codex_test'] = test
        st.session_state['codegeex_prompt'] = prompt
        st.session_state['codegeex_test'] = test


def change_code_golf():
    st.session_state['code_golf'] = not st.session_state['code_golf']

# st.title('Gode Golf: Codex VS CodeGeeX')
st.title('Gode Golf: codex-cushman VS codex-davinci')

st.checkbox('Code Golf', True, on_change=change_code_golf)

col1, col2 = st.columns(2, gap="large")


with col1:
    col1.caption("davinci model")
    codex_prompt = st.text_area('Input', value=st.session_state['codex_prompt'], key='col1.codex_prompt')
    codex_test = st.text_area('Test Script', value=st.session_state['codex_test'], key='col1.codex_test')


with col2:
    col2.caption("cushman model")
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
if st.session_state['code_golf'] and codex_length is not None and codegeex_length is not None:
    # st.caption("Code Golf Result")
    col7, col8 = st.columns(2, gap="large")
    difference = codex_length - codegeex_length
    codex_win = True
    if difference > 0:
        codex_win = False
    with col7:
        col7.metric(label="chars", value=codex_length, delta=difference, delta_color='inverse')
        if codex_win:
            col7.success("Win Code Golf!", icon="✅")

    with col8:
        col8.metric(label="chars", value=codegeex_length)
        if not codex_win:
            col8.success("Win Code Golf!", icon="✅")



test_prompts = []
for item in st.session_state['test_examples'].values():
    if item['id'] == 0:
        test_prompts.append(item['display'])
    else:
        test_prompts.append(str(item['id']) + '. ' + item['display'])
st.selectbox("Example Inputs", test_prompts, key='example_select', on_change=change_code_input)
