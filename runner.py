import pytest
import sys


class Runner:
    web_test_case_dir = "web_test/test_case"
    api_test_case_dir = "api_test/test_case"

    @classmethod
    def run_test(cls, test_case_path):
        pytest.main(["-sv", test_case_path])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "api":
            Runner.run_test(Runner.api_test_case_dir)
        elif sys.argv[1] == "web":
            Runner.run_test(Runner.web_test_case_dir)
    else:
        print("Usage: runner.py [api|web]")
