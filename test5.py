import difflib
list = [
    ("miad123", "6757"),
    ("miad135", "12356"),
    ("docp123", "thrth"),
    ("juf135", "35trt"),
    ("inc321", "ewte64"),
    ("bit235", "dhyyt36"),
    ("cra012", "nhg675"),
    ("stib025", "oiq82134"),
    ("jeff091", "hjyth45543"),
    ("cru295", "g33t3gh4"),
    ("bit235", "dhyyt36"),
    ]

find = "bit235"

result = [item for item in list
          if item[0] == find]

print (result)


print (3 or 2)