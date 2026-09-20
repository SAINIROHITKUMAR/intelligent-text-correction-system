from app import corrector

def test_spelling_correction():
    result = corrector.correct_text("I definately recieve teh adress.", use_language_tool=False)
    assert result["corrected_text"] == "I definitely receive the address."
    assert result["change_count"] == 4

def test_clean_text():
    result = corrector.correct_text("This is correct.", use_language_tool=False)
    assert result["corrected_text"] == "This is correct."
    assert result["change_count"] == 0

def test_school_sentence_correction():
    result = corrector.correct_text("i go schol", use_language_tool=False)
    assert result["corrected_text"] == "I go to school"
    assert result["change_count"] == 2

def test_name_sentence_correction():
    result = corrector.correct_text("my nam rohit", use_language_tool=False)
    assert result["corrected_text"] == "My name is Rohit"
    assert result["change_count"] == 1

def test_language_tool_suggestion(monkeypatch):
    monkeypatch.setattr(
        corrector,
        "_apply_language_tool",
        lambda text: ("I go to school.", [{"original": "go school", "corrected": "go to school.", "type": "grammar/spelling"}])
    )
    result = corrector.correct_text("I go school.")
    assert result["corrected_text"] == "I go to school."
    assert result["change_count"] == 1
