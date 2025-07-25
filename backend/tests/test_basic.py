from app.bizlogic.summary import count_words, get_words


def test_count_words():
    word_list = ["hello", "hello", "kalimera"]
    assert count_words(word_list) == [
        {"name": "hello", "count": 2},
        {"name": "kalimera", "count": 1},
    ]


def test_get_words():
    text = "George wants to work for you"
    result = get_words(text)
    expected = {"George", "wants", "work", "you"}
    assert result == expected
