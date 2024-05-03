import rjscanmodule.rjmetadata as rjmeta

title = "SW-932"
title = "IPZZ-014" # javmeear7a
#title = "DOCP-094"
#title = "042CLT-079"
title = "abc123miad-283af2ghj955docp094rr1qqq123x4rjrj65078dcx105miad283"#
#title = "FC2-PPV-4289049"

print (rjmeta.new_search_title(
    f_input_string = title,
    f_my_logger = None,
    f_attribute_override = "javmeear7a"
))

x ,_ , _ = (rjmeta.new_search_title("DOCP-094", f_my_logger = None))
print (x)