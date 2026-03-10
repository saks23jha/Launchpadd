import sys
import io
import traceback


def execute_python(code: str, context: dict = None) -> dict:
    """
    Execute Python code using exec() and return the result.

    Parameters:
        code     : Python code string to execute
        context  : Optional dictionary of variables to inject into execution scope

    Returns:
        {
            "success": bool,
            "output": str,   ← stdout output
            "error": str,    ← error message if failed
            "locals": dict   ← local variables after execution
        }
    """

    # Capture stdout
    stdout_capture = io.StringIO()
    sys.stdout = stdout_capture

    # Build execution scope
    exec_globals = {"__builtins__": __builtins__}
    exec_locals = {}

    # Inject context variables if provided
    if context:
        exec_locals.update(context)

    try:
        exec(code, exec_globals, exec_locals)

        output = stdout_capture.getvalue()

        print(f"[CODE EXECUTOR] Execution successful", file=sys.__stdout__)
        if output:
            print(f"[CODE EXECUTOR] Output:\n{output}", file=sys.__stdout__)

        return {
            "success": True,
            "output": output.strip(),
            "error": None,
            "locals": exec_locals,
        }

    except Exception as e:
        error_msg = traceback.format_exc()

        print(f"[CODE EXECUTOR] Execution failed:\n{error_msg}", file=sys.__stdout__)

        return {
            "success": False,
            "output": None,
            "error": error_msg,
            "locals": {},
        }

    finally:
        # Always restore stdout
        sys.stdout = sys.__stdout__


def execute_analysis(code: str, csv_data: list[dict]) -> dict:
    """
    Execute analysis code with CSV data pre-injected into scope.

    Parameters:
        code     : Python analysis code
        csv_data : List of row dicts from file_tool.read_csv()

    Returns:
        Same as execute_python()
    """

    print(f"[CODE EXECUTOR] Running analysis on {len(csv_data)} rows")

    context = {
        "data": csv_data,
        "rows": csv_data,
    }

    return execute_python(code, context=context)