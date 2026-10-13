from pdf_extract_chunking import character_chunking

def test_character_chunking_no_overlap():
    chunks = character_chunking(25 * "a", 10, 0)
    # always write code value == known value
    assert len(chunks) == 3
    assert [len(chunk) for chunk in chunks] == [10,10,5]