from gql import gql
DEFS = [
 ("subtitle","Subtitle","single_line_text_field"),("tasting_notes","Tasting notes","single_line_text_field"),
 ("region","Region","single_line_text_field"),("altitude","Altitude","single_line_text_field"),
 ("process","Process","single_line_text_field"),("variety","Variety","single_line_text_field"),
 ("roast","Roast level (1-5)","number_integer"),("acidity","Acidity (1-5)","number_integer"),
 ("body","Body (1-5)","number_integer"),("sweetness","Sweetness (1-5)","number_integer"),
 ("score","Cupping score","single_line_text_field"),("brew_tip","Brew tip","multi_line_text_field"),
]
M = """mutation($d: MetafieldDefinitionInput!){ metafieldDefinitionCreate(definition:$d){ createdDefinition{ id } userErrors{ field message code } } }"""
for key,name,t in DEFS:
    d={"namespace":"custom","key":key,"name":name,"type":t,"ownerType":"PRODUCT","access":{"storefront":"PUBLIC_READ"}}
    if t=="number_integer": d["validations"]=[{"name":"min","value":"1"},{"name":"max","value":"5"}]
    try: print(key, gql(M,{"d":d})["metafieldDefinitionCreate"]["createdDefinition"])
    except Exception as e: print(key,"ERR",str(e)[:200])
