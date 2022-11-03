from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union, Iterable, Dict
import itertools

import numpy as np
import tqdm

from codex.data import HUMAN_EVAL, read_problems, stream_jsonl, write_jsonl
from codex.execution import check_correctness


def estimate_pass_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array([estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)])


def evaluate_functional_correctness(
    sample_file: str,
    k: List[int] = [1, 10, 100],
    n_workers: int = 4,
    timeout: float = 3.0,
    test_script: str = "",
):
    """
    Evaluates the functional correctness of generated samples, and writes
    results to f"{sample_file}_results.jsonl.gz"
    """

    # problems = read_problems(problem_file)

    # Check the generated samples against test suites.
    with ThreadPoolExecutor(max_workers=n_workers) as executor:

        futures = []
        result = None

        print("Reading samples...")

        for sample_file in tqdm.tqdm([sample_file]):
            # task_id = sample["task_id"]
            completion = sample_file
            args = (test_script, completion, timeout)
            future = executor.submit(check_correctness, *args)
            futures.append(future)

#         assert len(completion_id) == len(problems), "Some problems are not attempted."

        print("Running test suites...")
        for future in tqdm.tqdm(as_completed(futures), total=len(futures)):
            result = future.result()

    return result
