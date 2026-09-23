import pytest

@pytest.mark.parametrize("var_c_str,var_p_str", [
    ('NM_000159.4:c.1074_1075insAGTTGAAGGACC', 'NP_000150.1:p.(Asp358_Gln359insSerTer)'),
    ('NM_000159.4:c.1074_1075insAGTTGAAGGAC', 'NP_000150.1:p.(Asp358_Gln359insSerTer)'),
    ('NM_004380.3:c.138_139insTCATCATGAGCTCCC', 'NP_004371.2:p.(Pro46_Asn47insSerSerTer)'),
    ('NM_000038.6:c.4189_4197delinsATATAAAAAA', 'NP_000029.2:p.(Glu1397IlefsTer2)'),
    ('NM_004380.2:c.139delinsTCATCATGAGCTG', 'NP_004371.2:p.(Asn47delinsSerSerTer)'),
    ('NM_004448.4:c.2339dup', 'NP_004439.2:p.(Tyr781IlefsTer93)'),
    ('NM_024529.5:c.1595_*2delinsCCCC', 'NP_078805.3:p.(Ter532SerextTer29)'),
    ('NM_004985.5:c.567_*1delinsTC', 'NP_004976.2:p.(Ter189TyrextTer8)'),
    ('NM_004985.5:c.567_*1insTAGAAA', 'NP_004976.2:p.?'),
    ('NM_000203.4:c.1960T>C', 'NP_000194.2:p.(Ter654ArgextTer?)'),
    ('NM_000203.4:c.1730del', 'NP_000194.2:p.(Cys577SerfsTer?)'),
    # --- insertion point inside a codon (frame_offset != 0); without the fix these
    # --- render as a delins removing the C-terminus instead of an insertion
    ('NM_000159.4:c.1073_1074insTAGTTGAAGGA', 'NP_000150.1:p.(Asp358_Gln359insSerTer)'),
    # insertion rewrites codon 358 (Asp to Val); with the split codon rebuilt after
    # the stop this is an insertion before Asp358, not a delins of it
    ('NM_000159.4:c.1072_1073insTTAGTTGAAGG', 'NP_000150.1:p.(Lys357_Asp358insValSerTer)'),
    # --- the base after the inserted stop is never translated and must not change
    # --- the description; all three yield Lys357, Val, Ser, Ter
    ('NM_000159.4:c.1072_1073insTTAGTTGAGGG', 'NP_000150.1:p.(Lys357_Asp358insValSerTer)'),
    ('NM_000159.4:c.1072_1073insTTAGTTGACGG', 'NP_000150.1:p.(Lys357_Asp358insValSerTer)'),
    # stop ends one base before the end of the insertion (f = 2, 5 bases); the
    # whole-codon round up would overrun the insertion
    ('NM_000159.4:c.1073_1074insATAGG', 'NP_000150.1:p.(Lys357_Asp358insGluTer)'),
    # --- duplication path (_incorporate_dup); without the cds_stop adjustment
    # --- these render as a delins running to the C-terminus with the Ter dropped
    ('NM_000159.4:c.1061_1080dup', 'NP_000150.1:p.(Asp360_Lys361insAlaAlaTer)'),
    # mid-codon dup (f = 1); Lys361 codon becomes Thr
    ('NM_000159.4:c.1062_1081dup', 'NP_000150.1:p.(Asp360_Lys361insThrAlaTer)'),
    # edge case: stop completes exactly at the end of the insertion; the retained
    # length cannot be rounded up, the whole insertion is kept, and translation
    # halts at the inserted stop (a nonsense variant)
    ('NM_000159.4:c.1073_1074insTTAG', 'NP_000150.1:p.(Gln359Ter)'),
])
def test_c_to_p(var_c_str, var_p_str, parser, am37):
    var_c = parser.parse(var_c_str)
    var_p = am37.c_to_p(var_c)
    assert str(var_p) == var_p_str


@pytest.mark.parametrize("var_c_str,var_p_str", [
    ('NM_000159.4:c.1074_1075insAGTTGAAGGAC', 'NP_000150.1:p.(D358_Q359insS*)')
])
def test_c_to_p_1_letter(var_c_str, var_p_str, parser, am37):
    var_c = parser.parse(var_c_str)
    var_p = am37.c_to_p(var_c)
    assert var_p.format(conf={"p_3_letter": False}) == var_p_str

