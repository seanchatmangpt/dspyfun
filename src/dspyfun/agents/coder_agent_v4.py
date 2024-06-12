import os
import subprocess
import tempfile
from textwrap import indent

from dspygen.agents.coder_agent import CoderAgentState
from dspygen.mixin.fsm.fsm_mixin import trigger, FSMMixin
from dspygen.modules.python_source_code_module import python_source_code_call

from dspyfun.modules.def_invoke_module import def_invoke_call
from dspyfun.utils.markdown_tools import extract_triple_backticks
from jinja2 import Template


def generate_code_with_main(python_code, invocation_code):
    template_str = """
{{ python_code }}


if __name__ == "__main__":
{{ invocation_code }}
    
    """
    template = Template(template_str)
    return template.render(python_code=python_code, invocation_code=invocation_code)


class CoderAgent(FSMMixin):
    def __init__(self, requirements: str, output_file: str = "output.py"):
        super().setup_fsm(CoderAgentState, initial=CoderAgentState.ANALYZING_REQUIREMENTS)
        self.requirements = requirements
        self.code = ""
        self.errors = []
        self.test_results = ""
        self.filename = None
        self.output_file = output_file

    @trigger(source=CoderAgentState.ANALYZING_REQUIREMENTS, dest=CoderAgentState.WRITING_CODE)
    def start_coding(self):
        """Simulate writing Python code."""
        pycode = extract_triple_backticks(python_source_code_call(self.requirements) + "\n\n")
        print(f"Code written:\n\n{self.code}")
        invoke = def_invoke_call(pycode, "use https://httpbin.org/get and print the result")
        print(f"Function invocation:\n\n{invoke}")
        self.code = generate_code_with_main(pycode, indent(invoke, "    "))
        self.filename = self.write_code_to_file(self.code)
        self.test_code()

    def write_code_to_file(self, code):
        """Write code to a temporary file and return the filename."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as f:
            f.write(code)
            return f.name

    @trigger(source=CoderAgentState.WRITING_CODE, dest=CoderAgentState.TESTING_CODE)
    def test_code(self):
        """Test the written code by executing the Python file."""
        output, error = self.execute_code(self.filename)
        if error:
            self.errors.append(error)
            print("Test Failed: ", error)
            self.handle_errors()
            # self.refactor_code()
            with open(self.output_file, 'w') as f:
                f.write(self.code)
        else:
            self.test_results = "Test Passed: Output = " + output
            print(self.test_results)
            self.complete_task()


    def execute_code(self, filepath):
        """Execute a Python script file and capture its output and errors."""
        try:
            result = subprocess.run(['python', filepath], capture_output=True, text=True, timeout=30)
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return "", "Execution timed out"

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.HANDLING_ERRORS, conditions=['errors_detected'])
    def handle_errors(self):
        """Handle errors if any are detected during testing."""
        print("Handling coding errors.")
        self.errors.clear()

    @trigger(source=[CoderAgentState.TESTING_CODE, CoderAgentState.HANDLING_ERRORS], dest=CoderAgentState.REFACTORING_CODE, conditions=['errors_resolved'])
    def refactor_code(self):
        """Refactor code after errors are resolved."""
        # TODO: Implement code refactoring
        self.code = "# Added by refactoring\n" + self.code
        print("Code after refactoring:\n", self.code)
        os.remove(self.filename)  # Clean up the original file
        self.filename = self.write_code_to_file(self.code)  # Write the refactored code back to disk
        self.handle_errors()

    @trigger(source=CoderAgentState.REFACTORING_CODE, dest=CoderAgentState.COMPLETING_TASK)
    def complete_refactored_task(self):
        """Complete the coding task after refactoring."""
        print("Task completed after refactoring.")
        os.remove(self.filename)  # Clean up after completion
        self.complete_task()

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.COMPLETING_TASK, unless=['errors_detected'])
    def complete_task(self):
        """Complete the coding task after successful testing."""
        print("Task completed without errors.")
        with open(self.output_file, 'w') as f:
            f.write(self.code)

    def errors_detected(self):
        """Check if there are any errors in the code."""
        return len(self.errors) > 0

    def errors_resolved(self):
        """Check if the errors have been successfully resolved."""
        return len(self.errors) == 0


def main():
    from dspygen.utils.dspy_tools import init_ol

    init_ol(max_tokens=3000)
    agent = CoderAgent("Make a request to an API and return the response.", output_file="api_request.py")
    print("Initial state:", agent.state)
    agent.start_coding()


if __name__ == "__main__":
    main()
