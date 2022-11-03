

from codex.data import HUMAN_EVAL
from codex.evaluation import evaluate_functional_correctness
from codex.execution import TimeoutException
from functools import reduce
import functools

IMPORT_HELPER = {
    "python": [
        "import math",
        "import re",
        "import sys",
        "import copy",
        "import datetime",
        "import itertools",
        "import collections",
        "import heapq",
        "import statistics",
        "import functools",
        "import hashlib",
        "import numpy",
        "import numpy as np",
        "import string",
        "from typing import *",
        "from collections import *",
        'from functools import reduce',
    ],
    "go"    : [
        "math",
        "strings",
        "fmt",
        "strconv",
        "time",
        "bytes",
        "regexp",
        "sort",
        "math/rand",
        "crypto/md5",
    ],
    "cpp"   : [
        "#include<stdlib.h>",
        "#include<algorithm>",
        "#include<math.h>",
        "#include<stdio.h>",
        "#include<vector>",
        "#include<string>",
        "#include<climits>",
        "#include<cstring>",
        "#include<iostream>",
    ],
}

def entry_point(
    sample_file: str,
    k: str = "1,10,100",
    n_workers: int = 4,
    timeout: float = 3.0,
    test_script: str = "",
):
    """
    Evaluates the functional correctness of generated samples, and writes
    results to f"{sample_file}_results.jsonl.gz"
    """
    # k = list(map(int, k.split(",")))
    # result = evaluate_functional_correctness(sample_file, k, n_workers, timeout, test_script)
    # return result
    test_setup = "\n".join(IMPORT_HELPER["python"]) + "\n"
    check_program = (
            test_setup +
            sample_file + "\n" +
            test_script
    )
    result = []
    try:
        exec(check_program)
        result.append("passed")
    except TimeoutException:
        result.append("timed out")
    except BaseException as e:
        result.append(f"failed: {e}")

    return dict(
        passed=result[0] == "passed",
        result=result[0]
    )
