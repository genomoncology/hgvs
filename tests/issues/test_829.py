import pytest

testdata = [
    ('NM_000159.4:c.1074_1075insAGTTGAAGGACC', 'NP_000150.1:p.(Asp358_Gln359insSerTer)'),
    ('NM_000159.4:c.1074_1075insAGTTGAAGGAC', 'NP_000150.1:p.(Asp358_Gln359insSerTer)'),
    ('NM_004380.3:c.138_139insTCATCATGAGCTCCC', 'NP_004371.2:p.(Pro46_Asn47insSerSerTer)'),
    ('NM_000038.6:c.4189_4197delinsATATAAAAAA', 'NP_000029.2:p.(Glu1397IlefsTer2)'),
    ('NM_004380.2:c.139delinsTCATCATGAGCTG', 'NP_004371.2:p.(Asn47delinsSerSerTer)'),
    ('NM_004448.4:c.2339dup', 'NP_004439.2:p.(Tyr781IlefsTer93)')
]

@pytest.mark.parametrize("var_c_str,var_p_str", testdata)
def test_c_to_p(var_c_str, var_p_str, parser, am37):
    var_c = parser.parse(var_c_str)
    var_p = am37.c_to_p(var_c)
    assert str(var_p) == var_p_str
