from enclosed.parser import Parser, TokenType

success_test_map = {
    "{}": [],
    r"\{": [(TokenType.NOT_ENCLOSED, 1, "{")],
    r"\{\}": [(TokenType.NOT_ENCLOSED, 2, "{}")],
    "abc": [(TokenType.NOT_ENCLOSED, 0, "abc")],
    "abc{xp}": [(TokenType.NOT_ENCLOSED, 0, "abc"), (TokenType.ENCLOSED, 4, "xp")],
    "abc{{xp}}": [(TokenType.NOT_ENCLOSED, 0, "abc"), (TokenType.ENCLOSED, 4, "{xp}")],
    "abc{xp}to": [
        (TokenType.NOT_ENCLOSED, 0, "abc"),
        (TokenType.ENCLOSED, 4, "xp"),
        (TokenType.NOT_ENCLOSED, 7, "to"),
    ],
    "{ab}{cde}": [(TokenType.ENCLOSED, 1, "ab"), (TokenType.ENCLOSED, 5, "cde")],
}


def pytest_generate_tests(metafunc):
    id_list = []
    argvalues = []
    argnames = ["text", "expected_result"]
    for text, expected_result in success_test_map.items():
        id_list.append(text)
        argvalues.append(([text, expected_result]))
    metafunc.parametrize(argnames, argvalues, ids=id_list)


def test_parse(text, expected_result):
    parser = Parser()
    result = parser.tokenize(text)
    assert expected_result == result
