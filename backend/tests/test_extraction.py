from app.scoring.extraction import extract_name, extract_age, extract_class

def test_extraction_functions():
    txt = "Hello everyone, my name is Priya. I am 14 years old and I am in class 9."
    assert extract_name(txt) == "Priya"
    assert extract_age(txt) == 14
    assert extract_class(txt) == "9"