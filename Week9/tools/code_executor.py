import io
import contextlib


class CodeExecutor:
    """
    Code Execution Tool

    Responsibilities:
    - Execute arbitrary Python code provided as a string
    - Capture stdout safely
    - Return execution output
    """

    def run(self, code: str) -> str:
        if not isinstance(code, str):
            raise TypeError("CodeExecutor expects Python code as a string")

        output_buffer = io.StringIO()

        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(code, {})
                

        except Exception as e:
            return f"Execution Error: {str(e)}"

        return output_buffer.getvalue().strip()