import sys
import os

# Add project root to PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from tools.code_executor import CodeExecutor


def main():
    executor = CodeExecutor()

    code = """
x = 10
y = 20
print("Sum:", x + y)

numbers = [1, 2, 3, 4, 5]
print("Average:", sum(numbers) / len(numbers))
"""

    result = executor.run(code)
    print("---- CodeExecutor Output ----")
    print(result)


if __name__ == "__main__":
    main()