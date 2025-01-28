from dataclasses import dataclass, field
from typing import List, Union, Any, Dict, Literal

@dataclass
class TestCase():
    args: Any = field(default_factory=tuple)
    solution: Any = field(default=None)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    result: Any = field(default=None, init=False)
    passed: bool = field(default=False, init=False)
    
    def __post_init__(self):
        if not isinstance(self.args, (tuple, list)):
            self.args = tuple(self.args)
        if not isinstance(self.kwargs, dict):
            raise ValueError("kwargs must be a dictionary")
    
    def set_result(self, res):
        self.result = res
        if self.result != self.solution:
            self.passed = False
        else:
            self.passed = True
        
class Tester():
    def __init__(self, solution, func_name):
        self.solution = solution
        self.solution_cls = solution.__class__
        self.func_name = func_name
        self.func = getattr(self.solution, func_name, None)
        self.test_cases = []
        assert self.func is not None, f"Test function named {func_name} is not found in solution class {self.solution_cls.__name__}"
        assert callable(self.func), f"Test function {self.solution_cls.__name__}.{func_name} is not callable"

    def test_one(self, test_case: TestCase):
        assert isinstance(test_case, TestCase), "Test case is not in the correct object"
        test_case.set_result(self.func(*test_case.args, **test_case.kwargs))
        self.test_cases.append(test_case)
        
    def test_many(self, test_cases: Union[TestCase, List[TestCase]]):
        if not isinstance(test_cases, list):
            test_cases = [test_cases]
        for test_case in test_cases:
            self.test_one(test_case)
    
    def report(self, print_option: Literal['failed', 'passed', 'all'] = 'failed'):
        """
        Generates a report of all test cases, including their status, inputs, expected solutions, and results.
        
        Args:
            print_option (str): Filter for test cases to display. Options are:
                                - 'failed': Display only failed test cases.
                                - 'passed': Display only passed test cases.
                                - 'all': Display all test cases.
        """
        if not self.test_cases:
            print("No test cases have been run.")
            return

        print(f"Testing Report for Function: {self.solution_cls.__name__}.{self.func_name}")
        print("=" * 80)
        
        passed_count = 0
        failed_count = 0

        for idx, test_case in enumerate(self.test_cases, start=1):
            status = "PASSED" if test_case.passed else "FAILED"
            
            if test_case.passed:
                passed_count += 1
            else:
                failed_count += 1
                
            # Filter based on print_option
            if (print_option == 'failed' and test_case.passed) or \
            (print_option == 'passed' and not test_case.passed):
                continue

            print(f"Test Case #{idx}: {status}")
            print(f"  Args: {test_case.args}")
            print(f"  Kwargs: {test_case.kwargs}")
            print(f"  Expected: {test_case.solution}")
            print(f"  Result: {test_case.result}")
            print("-" * 80)

            

        # Summary
        print(f"Summary:")
        print(f"  Total Test Cases: {len(self.test_cases)}")
        print(f"  Passed: {passed_count}")
        print(f"  Failed: {failed_count}")
        print("=" * 80)

    def __call__(self, test_cases: List[TestCase], **report_kwags):
        self.test_many(test_cases)
        self.report(**report_kwags)
    