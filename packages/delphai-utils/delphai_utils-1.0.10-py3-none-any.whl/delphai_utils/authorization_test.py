from delphai_utils.authorization import is_authorized

test_cases = [
    [[[], ["1"], "all"], False],
    [[[], ["1"], "some"], False],
    [[["1", "2", "3"], ["2", "3"], "all"], True],
    [[["1", "2", "3"], ["2", "4"], "all"], False],
    [[["1", "2", "3"], ["2", "4"], "some"], True],
    [[["1", "2", "3"], ["2", "3", "3", "2"], "all"], True],
]


def test_is_authorized():
    for test_case in test_cases:
        args, expected = test_case
        assert is_authorized(*args) == expected
