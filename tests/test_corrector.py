from app.corrector import correct_text

def test_spelling_correction():
    result = correct_text("I definately recieve teh adress.")
    assert result["corrected_text"] == "I definitely receive the address."
    assert result["change_count"] == 4

def test_clean_text():
    result = correct_text("This is correct.")
    assert result["corrected_text"] == "This is correct."
    assert result["change_count"] == 0
