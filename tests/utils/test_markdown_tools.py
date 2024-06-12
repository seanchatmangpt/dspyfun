import pytest
from dspyfun.utils.markdown_tools import extract_triple_backticks_content


def test_extract_triple_backticks_content():
    markdown_string = """
    Here is some text.
    ```
    code block 1
    ```
    More text.
    ```
    code block 2
    ```
    """
    expected_output = ["\n    code block 1\n    ", "\n    code block 2\n    "]
    assert extract_triple_backticks_content(markdown_string) == expected_output


def test_extract_triple_backticks_content_empty():
    markdown_string = "Here is some text without any code blocks."
    expected_output = []
    assert extract_triple_backticks_content(markdown_string) == expected_output


def test_extract_triple_backticks_content_nested():
    markdown_string = """
    ```python
    code block 1
    ```
    ```python
    code block 2 with ```nested``` backticks
    ```
    """
    expected_output = ["\n    code block 1\n    ", "\n    code block 2 with ```nested``` backticks\n    "]
    extracted = extract_triple_backticks_content(markdown_string)
    assert extracted == expected_output


def test_extract_triple_backticks_content_with_language():
    markdown_string = """
    ```python
    def foo2():
        pass
    ```
    """
    expected_output = ["def foo():\n    pass\n"]
    assert extract_triple_backticks_content(markdown_string) == expected_output


def test_extract_triple_backticks_content_missing_language():
    markdown_string = """
    ```
    def foo():
        pass
    ```
    """
    expected_output = ["def foo():\n    pass\n"]
    assert extract_triple_backticks_content(markdown_string) == expected_output
