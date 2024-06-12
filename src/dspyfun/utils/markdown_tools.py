from textwrap import dedent


def extract_triple_backticks(markdown_string):
    """
    Extracts text within triple backticks from a markdown string using a state machine.

    Args:
        markdown_string (str): The markdown content as a string.

    Returns:
        list: A list of strings, each containing the content within triple backticks.
    """
    # Define states
    OUTSIDE_CODE_BLOCK = 0
    ENTERING_CODE_BLOCK = 1
    INSIDE_CODE_BLOCK = 2

    state = OUTSIDE_CODE_BLOCK
    code_blocks = []
    current_block = []

    lines = markdown_string.split('\n')

    for line in lines:
        if state == OUTSIDE_CODE_BLOCK:
            if line.strip().startswith('```'):
                state = ENTERING_CODE_BLOCK
        elif state == ENTERING_CODE_BLOCK:
            # This state helps in handling the language specifier line
            if line.strip() == '':
                state = INSIDE_CODE_BLOCK
            else:
                state = INSIDE_CODE_BLOCK
                current_block.append(line)
        elif state == INSIDE_CODE_BLOCK:
            if line.strip().startswith('```'):
                state = OUTSIDE_CODE_BLOCK
                code_blocks.append('\n'.join(current_block))
                current_block = []
            else:
                current_block.append(line)

    return "\n\n".join(code_blocks)
