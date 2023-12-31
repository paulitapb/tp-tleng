from parse_regex import parse_regex, SyntaxError
import pytest
import re

cases = [
    {"text": ''},
    {"text": 'a'},
    {"text": 'b'},
    {"text": '1'},
    {"text": '\\|'},
    {"text": '\\+'},
    {"text": '\\?'},
    {"text": '\\\\'},
    {"text": '\\('},
    {"text": '\\)'},
    {"text": '\\['},
    {"text": '\\]'},
    {"text": '()|()'},
    {"text": 'a|b'},
    {"text": 'a|1'},
    {"text": 'a|\\+'},
    {"text": 'a|b|c'},
    {"text": 'a|b|c|d|e'},
    {"text": '()()'},
    {"text": 'ab'},
    {"text": 'a1'},
    {"text": 'a\\+'},
    {"text": 'abc'},
    {"text": 'abcde'},
    {"text": 'ab|cd'},
    {"text": '(ab|cd)'},
    {"text": '(ab)|(cd)'},
    {"text": 'a(b|c)d'},
    {"text": '(ab|c)d'},
    {"text": 'a(b|cd)'},
    {"text": '()*'},
    {"text": 'a*'},
    {"text": '1*'},
    {"text": '\\+*'},
    {"text": 'ab*'},
    {"text": '(ab)*'},
    {"text": 'a|b*'},
    {"text": '(a|b)*'},
    {"text": '()+'},
    {"text": 'a+'},
    {"text": '1+'},
    {"text": '\\++'},
    {"text": 'ab+'},
    {"text": '(ab)+'},
    {"text": 'a|b+'},
    {"text": '(a|b)+'},
    {"text": '(()+)*'},
    {"text": '(a+)*'},
    {"text": '(a*)+'},
    {"text": 'a*a+'},
    {"text": 'a+a*'},
    {"text": 'a*|b+'},
    {"text": '()?'},
    {"text": 'a?'},
    {"text": '1?'},
    {"text": '\\+?'},
    {"text": 'a?b'},
    {"text": 'ab?'},
    {"text": '(ab)?'},
    {"text": 'a|b?'},
    {"text": '(a|b)?'},
    {"text": '(a*)?'},
    {"text": '(a?)*'},
    {"text": '(a+)?'},
    {"text": '(a?)+'},
    {"text": '(){0}'},
    {"text": '(){1}'},
    {"text": 'a{0}'},
    {"text": 'a{1}'},
    {"text": 'a{3}'},
    {"text": 'a{5}'},
    {"text": '\\+{0}'},
    {"text": '\\+{1}'},
    {"text": '\\+{3}'},
    {"text": 'a{3}b'},
    {"text": 'ab{3}'},
    {"text": '(ab){3}'},
    {"text": '(ab){5}'},
    {"text": 'a{3}|b'},
    {"text": 'a|b{3}'},
    {"text": '(a|b){3}'},
    {"text": '(a*){3}'},
    {"text": '(a{3})*'},
    {"text": '(a+){3}'},
    {"text": '(a{3})+'},
    {"text": '(a?){3}'},
    {"text": '((ab)*){3}'},
    {"text": '((ab)+){3}'},
    {"text": '((ab)?){3}'},
    {"text": '(){0,3}'},
    {"text": '(){2,4}'},
    {"text": 'a{0,3}'},
    {"text": 'a{2,4}'},
    {"text": '\\+{0,3}'},
    {"text": '\\+{2,4}'},
    {"text": 'a{0,3}b{2,4}'},
    {"text": '(ab){0,3}'},
    {"text": '(ab){2,4}'},
    {"text": 'a{0,3}|b{2,4}'},
    {"text": '(a|b){0,3}'},
    {"text": '(a|b){2,4}'},
    {"text": '(a*){0,3}'},
    {"text": '(a*){2,4}'},
    {"text": '(a+){0,3}'},
    {"text": '(a+){2,4}'},
    {"text": '(a?){0,3}'},
    {"text": '(a?){2,4}'},
    {"text": '((ab)*){0,3}'},
    {"text": '((ab)*){2,4}'},
    {"text": '((ab)+){0,3}'},
    {"text": '((ab)+){2,4}'},
    {"text": '((ab)?){0,3}'},
    {"text": '((ab)?){2,4}'},
    {"text": '(a{2}){2,4}'},
    {"text": '(a{0,3}){2}'},
    {"text": 'a\\{1\\}'},
    {"text": '[a]'},
    {"text": '[1]'},
    {"text": '[\\+]'},
    {"text": '[\\*]'},
    {"text": '[\\[]'},
    {"text": '[abc]'},
    {"text": '[ace]'},
    {"text": '[a1]'},
    {"text": '[1a]'},
    {"text": '[a\\+]'}, {
        "text": '[a1\\+]'},
    {"text": '[a-e]'},
    {"text": '[a-z]'},
    {"text": '[A-Z]'},
    {"text": '[a-zA-Z]'},
    {"text": '[3-7]'},
    {"text": '[0-9]'},
    {"text": '[a-zA-Z0-9]'},
    {"text": '[a-zA-Z0-9\\+]'},
    {"text": '[a-zA-Z0-9_]'},
    {"text": '[]', "should_match": lambda string: False},
    {"text": '[a-cx-z]'},
    {"text": '[ax-z]'},
    {"text": '[a-cx]'},
    {"text": '[-]'},
    {"text": '[a-]'},
    {"text": '[-a]'},
    {"text": '[ab-]'},
    {"text": '[-ab]'},
    {"text": '[-ab-]'},
    {"text": '[-a-c]'},
    {"text": '[a-c-]'},
    {"text": '[-a-c-]'},
    {"text": '[-ax-z]'},
    {"text": '[ax-z-]'},
    {"text": '[-ax-z-]'},
    {"text": '[-a-cx]'},
    {"text": '[a-cx-]'},
    {"text": '[-a-cx-]'},
    {"text": '[-a-cx-z]'},
    {"text": '[a-cx-z-]'},
    {"text": '[-a-cx-z-]'},
    {"text": '[{]'},
    {"text": '[a-z-]'},
    {"text": '[a-z{]'},
    {"text": '\\d'},
    {"text": '\\w'},
    {"text": '[ab]a'},
    {"text": '[ab]1'},
    {"text": 'a[ab]'},
    {"text": '1[ab]'},
    {"text": '[ab][cd]'},
    {"text": '[ab]|[cd]'},
    {"text": '[ab]*'},
    {"text": '[ab]+'},
    {"text": '[ab]?'},
    {"text": '[ab]{0}'},
    {"text": '[ab]{3}'},
    {"text": '[ab]{0,3}'},
    {"text": '[ab]{2,4}'},
    {"text": '[a-e]*'},
    {"text": '[a-e]+'},
    {"text": '[a-e]?'},
    {"text": 'a\\d'},
    {"text": '\\da'},
    {"text": '\\d+'},
    {"text": '\\d*'},
    {"text": '\\d?'},
    {"text": 'a\\w'},
    {"text": '\\wa'},
    {"text": '\\w+'},
    {"text": '\\w*'},
    {"text": '\\w?'},
    {"text": '\\d\\w'},
    {"text": '()'},
    {"text": '(())'},
    {"text": '(a)'},
    {"text": '((a)b)'},
    {"text": '(a(b))'},
    {"text": '(a(b(c)))'},
    {"text": '(((a)b)c)'},
    {"text": '{ '},
    {"text": '}'},
    {"text": '{{ '},
    {"text": '}}'},
    {"text": '{}'},
    {"text": '{{}}'},
    {"text": '{a}'},
    {"text": '-'},
    {"text": '--'},
    {"text": '0-9'},
    {"text": 'a-z'},
    {"text": '{-}'},
    {"text": '[a{1}]', "should_fail": True},
    {"text": '|', "should_fail": True},
    {"text": 'a|', "should_fail": True},
    {"text": '|a', "should_fail": True},
    {"text": '+', "should_fail": True},
    {"text": '+a', "should_fail": True},
    {"text": '?', "should_fail": True},
    {"text": '?a', "should_fail": True},
    {"text": 'a**', "should_fail": True},
    {"text": 'a++', "should_fail": True},
    {"text": 'a??', "should_fail": True},
    {"text": 'a*+', "should_fail": True},
    {"text": 'a*?', "should_fail": True},
    {"text": 'a*{0}', "should_fail": True},
    {"text": 'a*{0,1}', "should_fail": True},
    {"text": 'a{0}{0,1}', "should_fail": True},
    {"text": '(', "should_fail": True},
    {"text": ')', "should_fail": True},
    {"text": ')(', "should_fail": True},
    {"text": '())', "should_fail": True},
    {"text": '[', "should_fail": True},
    {"text": ']', "should_fail": True},
    {"text": '][', "should_fail": True},
    {"text": '[]]', "should_fail": True},
    {"text": '(]', "should_fail": True},
    {"text": '{2}', "should_fail": True},
    {"text": '{2}a', "should_fail": True},
    {"text": '{1,2}', "should_fail": True},
    {"text": '{1,2}a', "should_fail": True},
    {"text": '{2}{3}', "should_fail": True},
    {"text": '[a|b]', "should_fail": True},
    {"text": '[a*]', "should_fail": True},
    {"text": '[a+]', "should_fail": True},
    {"text": '[a?]', "should_fail": True},
    {"text": '[\\d]', "should_fail": True},
    {"text": '[\\w]', "should_fail": True},
    {"text": '[z-a]', "should_fail": True},
    {"text": ' '},
    {"text": '  '},
    {"text": 'a '},
    {"text": ' a'},
    {"text": 'a b'},
    {"text": ' |a'},
    {"text": 'a| '},
    {"text": ' +'},
    {"text": ' *'},
    {"text": ' ?'}
]

@pytest.mark.parametrize("case", cases, ids=lambda case: case["text"])
class TestParser:

    def test_parse_and_match(self, case, strings):
        '''Se aceptan las cadenas correctas'''
        if not "should_fail" in case or not case["should_fail"]:
            regex = parse_regex(case["text"])
            for string in strings:
                if "should_match" in case:
                    should_match = case["should_match"](string)
                else:
                    should_match = re.fullmatch(
                        case["text"], string) is not None
                assert regex.match(
                    string) == should_match, f"El resultado de parsear '{regex}' { 'no acepta' if should_match else 'acepta'} la cadena '{string}'"
        else:
            with pytest.raises(SyntaxError):
                parse_regex(case["text"])
