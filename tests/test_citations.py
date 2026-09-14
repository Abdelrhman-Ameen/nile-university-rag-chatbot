from nu_chat.citations import citation_ids, normalize_citations


def test_python_lists_are_not_rewritten_as_source_references():
    answer = "NU is in Giza [2, 3]. A list: `values = [1, 20, 300]`.\n```python\nprint(values[99])\n```"
    normalized = normalize_citations(answer)
    assert normalized == answer.replace("[2, 3]", "[2] [3]")
    assert citation_ids(normalized) == {2, 3}


def test_even_an_unclosed_code_fence_cannot_supply_fake_citations():
    assert citation_ids("Supported [1].\n```python\nvalues[999]") == {1}
