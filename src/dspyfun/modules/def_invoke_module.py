import dspy

from dspyfun.utils.dspy_tools import init_ol
from dspyfun.utils.markdown_tools import extract_triple_backticks


class GenerateFunctionInvocation(dspy.Signature):
    """
    Generate a Python function invocation based on the provided function declaration.
    """
    function_declaration = dspy.InputField(desc="The declaration of the function including its name and parameters.")
    additional_instructions = dspy.InputField(
        desc="Additional instructions to include in the function invocation. For example, a comment or print statement.")
    invocation_command = dspy.OutputField(desc="The generated invocation command for the function.")


# Example usage within the DefInvokeModule
class DefInvokeModule(dspy.Module):
    """DefInvokeModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, function_declaration, additional_instructions):
        pred = dspy.Predict(GenerateFunctionInvocation)
        self.output = pred(function_declaration=function_declaration,
                           additional_instructions=additional_instructions).invocation_command
        return self.output


def def_invoke_call(function_declaration, additional_instructions=""):
    def_invoke = DefInvokeModule()
    code = extract_triple_backticks(def_invoke.forward(function_declaration=function_declaration,
                                                       additional_instructions=additional_instructions))

    if not code:
        raise ValueError("No code found in the provided function declaration.")
    else:
        return code


example = '''import requests
def make_api_request(url):
    """Make a request to an API and return the response."""
    try:
        response = requests.get(url)
        # Ensure we have a successful status code (200-299 range)
        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise ValueError("API request failed with status code: {}".format(response.status_code))
    except requests.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")
        return None'''


def main():
    init_ol()
    invoke = def_invoke_call(example)
    print(invoke)


if __name__ == "__main__":
    main()
