import pytest

testdata = [
    ('NM_000159.4:c.1074_1075insAGTTGAAGGACC', 'NP_000150.1:p.(Gln359_Lys438delinsSer)'),
    ('NM_000159.4:c.1074_1075insAGTTGAAGGAC', 'NP_000150.1:p.(Gln359_Lys438delinsSer)'),
]

@pytest.mark.parametrize("var_c_str,var_p_str", testdata)
def test_c_to_p(var_c_str, var_p_str, parser, am37):
    var_c = parser.parse(var_c_str)
    var_p = am37.c_to_p(var_c)
    assert str(var_p) == var_p_str
