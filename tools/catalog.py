"""Creates/updates the Altura demo catalog: collections, products (productSet, idempotent by handle), publishing.
Run again any time; it upserts by handle. Bag images are used when media/uploaded.json has them.
"""
import json, os
from gql import gql

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = json.load(open(os.path.join(HERE, "..", "media", "uploaded.json")))
LOCATION = "gid://shopify/Location/92902228043"
ONLINE_STORE = "gid://shopify/Publication/226136096843"


def f(name):
    k = f"altura-{name}.jpg" if not name.endswith(".png") else name
    return FILES.get(k, {}).get("id")


SIZES = ["250 g", "1 kg"]
GRINDS = ["Whole bean", "Filter", "Espresso"]

COFFEES = [
    dict(handle="cajamarca-geisha", title="Cajamarca Geisha", bag="geisha", life="life-geisha", origin="origin-cajamarca",
         price=(24, 84), stock=8, tags=["single-origin", "limited", "new", "light-roast"],
         subtitle="Jasmine, white peach & bergamot", notes="Jasmine, White peach, Bergamot, Honey",
         region="Cajamarca", altitude="1,950 masl", process="Washed", variety="Geisha", score="89.5",
         roast=1, acidity=5, body=2, sweetness=4,
         desc="<p>Our rarest lot of the year. Grown by the Huamán family on a single hectare in San Ignacio, this Geisha is floral, tea-like and impossibly clean — the kind of cup that makes people fall in love with coffee.</p>",
         more="<p>Hand-picked at peak ripeness, fermented 36 hours and washed in spring water. Dried on raised beds for 21 days. Only 120 bags available this harvest.</p>"),
    dict(handle="villa-rica-honey", title="Villa Rica Honey", bag="villarica", life="life-villarica", origin="origin-villarica",
         price=(18, 62), stock=140, tags=["single-origin", "bestseller", "medium-roast"],
         subtitle="Caramel, red apple & brown sugar", notes="Caramel, Red apple, Brown sugar",
         region="Villa Rica, Pasco", altitude="1,650 masl", process="Honey", variety="Caturra, Typica", score="86.5",
         roast=3, acidity=3, body=4, sweetness=5,
         desc="<p>Our best-selling everyday coffee. Honey processing leaves some of the sweet fruit on the bean while it dries, giving a syrupy body and a long caramel finish. Delicious black or with milk.</p>",
         more="<p>Grown by the Villa Rica cooperative in the cloud forest of Pasco. Yellow-honey processed and sun-dried on patios for 14 days.</p>"),
    dict(handle="cusco-bourbon-natural", title="Cusco Bourbon Natural", bag="cusco", life="life-cusco", origin="origin-cusco",
         price=(17, 58), stock=95, tags=["single-origin", "medium-roast"],
         subtitle="Dark chocolate, cherry & cacao nib", notes="Dark chocolate, Cherry, Cacao nib",
         region="La Convención, Cusco", altitude="1,800 masl", process="Natural", variety="Red Bourbon", score="87",
         roast=3, acidity=3, body=5, sweetness=4,
         desc="<p>A fruit-forward natural from the valleys below Machu Picchu. Whole cherries dry slowly in the sun, building jammy notes of black cherry over a deep chocolate base.</p>",
         more="<p>From the Quellouno producers association. Dried as whole cherry on African beds for 28 days.</p>"),
    dict(handle="amazonas-washed", title="Amazonas Washed", bag="amazonas", life="life-amazonas", origin="origin-amazonas",
         price=(16, 55), stock=120, tags=["single-origin", "light-roast"],
         subtitle="Green apple, panela & lemon zest", notes="Green apple, Panela, Lemon zest",
         region="Rodríguez de Mendoza, Amazonas", altitude="1,850 masl", process="Washed", variety="Typica, Catimor", score="86",
         roast=2, acidity=4, body=3, sweetness=3,
         desc="<p>Bright, crisp and endlessly drinkable. Grown near the Gocta waterfall in Peru's northern cloud forest — a fantastic pour-over coffee for every day.</p>",
         more="<p>Fully washed and dried on raised beds. Sourced from 18 smallholders who share a wet mill.</p>"),
    dict(handle="puno-tunki", title="Puno Tunki", bag="puno", life="life-puno", origin="origin-puno",
         price=(19, 66), stock=60, tags=["single-origin", "medium-roast", "award-winner"],
         subtitle="Blackberry, plum & milk chocolate", notes="Blackberry, Plum, Milk chocolate",
         region="Sandia Valley, Puno", altitude="2,100 masl", process="Washed", variety="Bourbon, Typica", score="88",
         roast=2, acidity=4, body=4, sweetness=4,
         desc="<p>Grown higher than almost any coffee on earth. The cold nights of the Sandia valley slow the cherry's ripening and pack it with dark-berry sweetness.</p>",
         more="<p>From the CECOVASA cooperative, home of multiple Cup of Excellence winners.</p>"),
    dict(handle="house-espresso-blend", title="House Espresso", bag="espresso", life="life-espresso", origin="hero-roaster",
         price=(15, 50), stock=200, tags=["blend", "bestseller", "dark-roast"],
         subtitle="Cocoa, toasted hazelnut & molasses", notes="Cocoa, Toasted hazelnut, Molasses",
         region="Villa Rica + Cusco", altitude="1,650–1,800 masl", process="Honey & Natural", variety="Blend", score="85",
         roast=4, acidity=2, body=5, sweetness=4,
         desc="<p>Built for espresso and milk drinks. Thick crema, low acidity and a sweet chocolate finish that cuts through any latte.</p>",
         more="<p>60% Villa Rica Honey, 40% Cusco Natural, roasted a touch longer for body.</p>"),
    dict(handle="chanchamayo-decaf", title="Chanchamayo Decaf", bag="decaf", life="life-decaf", origin="origin-villarica",
         price=(16, 54), compare=(19, 64), stock=75, tags=["single-origin", "decaf", "medium-roast"],
         subtitle="Milk chocolate, orange & almond", notes="Milk chocolate, Orange, Almond",
         region="Chanchamayo, Junín", altitude="1,500 masl", process="Swiss Water® decaf", variety="Catuai", score="84.5",
         roast=3, acidity=2, body=3, sweetness=4,
         desc="<p>All of the flavor, none of the jitters. Decaffeinated with only water — no chemicals — so you can enjoy a proper cup at 9 pm.</p>",
         more="<p>99.9% caffeine free. Processed by Swiss Water in Canada, roasted by us in Lima.</p>"),
]

GEAR = [
    dict(handle="ceramic-pour-over-dripper", title="Ceramic Pour-Over Dripper", type="Brewing Gear", tags=["gear", "bestseller"],
         images=["dripper-1", "dripper-2", "tile-gear"], option=("Size", [("01 · 1–2 cups", 28), ("02 · 1–4 cups", 32)]), stock=40,
         desc="<p>Hand-thrown in Chulucanas, Piura, and glazed in our signature terracotta. The spiral ribs and single large hole give you full control of flow — and a sweeter, clearer cup.</p>",
         more="<p>Stoneware, dishwasher safe. Fits #01 or #02 cone filters. Each piece is unique.</p>"),
    dict(handle="gooseneck-kettle", title="Gooseneck Pour Kettle", type="Brewing Gear", tags=["gear"],
         images=["kettle-1", "kettle-2"], option=("Capacity", [("0.6 L", 79), ("0.9 L", 89)]), stock=25,
         desc="<p>A slim spout for a slow, precise pour. Matte black stainless steel with a heat-safe handle — works on gas, electric and induction.</p>",
         more="<p>18/8 stainless steel. Built-in thermometer in the lid.</p>"),
    dict(handle="heritage-hand-grinder", title="Heritage Hand Grinder", type="Brewing Gear", tags=["gear", "limited"],
         images=["grinder-1", "grinder-2"], price=119, stock=12,
         desc="<p>Restored-style wooden grinder with a hardened steel burr. Slow, quiet and satisfying — and it grinds evenly enough for pour-over.</p>",
         more="<p>Walnut body, cast-iron crank, adjustable burr. Holds 30 g.</p>"),
    dict(handle="glass-brewer", title="Glass Brewer & Server", type="Brewing Gear", tags=["gear"],
         images=["server-1", "server-2"], price=49, stock=30,
         desc="<p>An hourglass brewer in heat-resistant borosilicate glass, with a wooden collar. Brews up to six cups and doubles as a beautiful server.</p>",
         more="<p>800 ml. Uses square or round bonded filters.</p>"),
    dict(handle="digital-brew-scale", title="Digital Brew Scale", type="Brewing Gear", tags=["gear"],
         images=["scale-1", "scale-2"], price=59, compare=72, stock=18,
         desc="<p>Weigh your coffee and water to 0.1 g and time your brew on the same screen. The single biggest upgrade for better coffee at home.</p>",
         more="<p>3 kg capacity, auto-tare, USB-C rechargeable.</p>"),
    dict(handle="stoneware-mug", title="Stoneware Mug", type="Drinkware", tags=["gear", "gift"],
         images=["mug-1", "mug-2"], option=("Size", [("8 oz", 24), ("12 oz", 28)]), stock=60,
         desc="<p>A heavy, hand-glazed mug that keeps coffee hot and feels good in both hands. Made by potters in Lima's Barranco district.</p>",
         more="<p>Microwave and dishwasher safe.</p>"),
    dict(handle="discovery-box", title="Origins Discovery Box", type="Gift", tags=["gift", "bestseller", "bundle"],
         images=["altura-discovery-box.jpg", "tile-gifts"], price=39, stock=50,
         desc="<p>Three 100 g bags from three regions — Cajamarca, Villa Rica and Cusco — with tasting cards and a handwritten note. The perfect gift for the coffee lover who has everything.</p>",
         more="<p>Ships in a recyclable gift box. Add a gift note in your bag.</p>"),
]


def media_ids(names):
    out = []
    for n in names:
        fid = FILES.get(n, {}).get("id") if n.endswith((".jpg", ".png")) and n.startswith("altura") else f(n)
        if fid:
            out.append({"id": fid})
    return out


SET = """mutation($input: ProductSetInput!, $id: ProductSetIdentifiers){ productSet(input:$input, identifier:$id, synchronous:true){ product{ id handle } userErrors{ field message code } } }"""


def inv(q):
    return [{"locationId": LOCATION, "name": "available", "quantity": q}]


def coffee_input(c):
    variants = []
    for s, size in enumerate(SIZES):
        for g in GRINDS:
            v = {"optionValues": [{"optionName": "Size", "name": size}, {"optionName": "Grind", "name": g}],
                 "price": str(c["price"][s]), "sku": f"ALT-{c['handle'][:6].upper()}-{size.replace(' ', '')}-{g[:3].upper()}",
                 "inventoryItem": {"tracked": True}, "inventoryQuantities": inv(c["stock"] if s == 0 else max(4, c["stock"] // 3))}
            if c.get("compare"):
                v["compareAtPrice"] = str(c["compare"][s])
            variants.append(v)
    mf = [("subtitle", "single_line_text_field", c["subtitle"]), ("tasting_notes", "single_line_text_field", c["notes"]),
          ("region", "single_line_text_field", c["region"]), ("altitude", "single_line_text_field", c["altitude"]),
          ("process", "single_line_text_field", c["process"]), ("variety", "single_line_text_field", c["variety"]),
          ("score", "single_line_text_field", c["score"]),
          ("roast", "number_integer", c["roast"]), ("acidity", "number_integer", c["acidity"]),
          ("body", "number_integer", c["body"]), ("sweetness", "number_integer", c["sweetness"])]
    bag = FILES.get(f"altura-bag-{c['bag']}.jpg", {}).get("id")
    files = ([{"id": bag}] if bag else []) + media_ids([c["life"], c["origin"]])
    return {
        "title": c["title"], "handle": c["handle"], "vendor": "Altura Coffee Co.", "productType": "Coffee", "status": "ACTIVE",
        "tags": c["tags"], "descriptionHtml": c["desc"] + "<!-- more -->" + c["more"],
        "seo": {"title": f"{c['title']} — {c['subtitle']}", "description": f"Peruvian specialty coffee from {c['region']}. {c['subtitle']}."},
        "productOptions": [{"name": "Size", "values": [{"name": s} for s in SIZES]}, {"name": "Grind", "values": [{"name": g} for g in GRINDS]}],
        "variants": variants, "files": files,
        "metafields": [{"namespace": "custom", "key": k, "type": t, "value": str(v)} for k, t, v in mf],
    }


def gear_input(g):
    if "option" in g:
        name, vals = g["option"]
        opts = [{"name": name, "values": [{"name": v} for v, _ in vals]}]
        variants = [{"optionValues": [{"optionName": name, "name": v}], "price": str(p), "inventoryItem": {"tracked": True},
                     "inventoryQuantities": inv(g["stock"]), "sku": f"ALT-{g['handle'][:8].upper()}-{i}"} for i, (v, p) in enumerate(vals)]
    else:
        opts = [{"name": "Title", "values": [{"name": "Default Title"}]}]
        v = {"optionValues": [{"optionName": "Title", "name": "Default Title"}], "price": str(g["price"]), "inventoryItem": {"tracked": True},
             "inventoryQuantities": inv(g["stock"]), "sku": f"ALT-{g['handle'][:8].upper()}"}
        if g.get("compare"):
            v["compareAtPrice"] = str(g["compare"])
        variants = [v]
    return {"title": g["title"], "handle": g["handle"], "vendor": "Altura Coffee Co.", "productType": g["type"], "status": "ACTIVE",
            "tags": g["tags"], "descriptionHtml": g["desc"] + "<!-- more -->" + g["more"],
            "productOptions": opts, "variants": variants, "files": media_ids(g["images"])}


COLLECTIONS = [
    ("coffee", "Coffee", "Single origins and blends from the Peruvian Andes, roasted to order every week.", "tile-single", [("TYPE", "EQUALS", "Coffee")]),
    ("single-origin", "Single Origin", "Traceable to one farm or cooperative. Taste the place.", "origin-cajamarca", [("TAG", "EQUALS", "single-origin")]),
    ("blends", "Espresso & Blends", "Balanced, chocolatey coffees built for espresso and milk.", "tile-blends", [("TAG", "EQUALS", "blend")]),
    ("brewing-gear", "Brewing Gear", "Tools we use every morning at the roastery.", "tile-gear", [("TAG", "EQUALS", "gear")]),
    ("gifts", "Gifts", "Thoughtful gifts for every kind of coffee lover.", "tile-gifts", [("TAG", "EQUALS", "gift")]),
    ("best-sellers", "Best Sellers", "The coffees and tools our customers come back for.", "hero-farm", [("TAG", "EQUALS", "bestseller")]),
    ("limited-releases", "Limited Releases", "Micro-lots and rare varieties. When they're gone, they're gone.", "drop-geisha", [("TAG", "EQUALS", "limited")]),
]

COLL_Q = """query($h:String!){ collectionByHandle(handle:$h){ id } }"""
COLL_C = """mutation($input: CollectionInput!){ collectionCreate(input:$input){ collection{ id handle } userErrors{ field message } } }"""
COLL_U = """mutation($input: CollectionInput!){ collectionUpdate(input:$input){ collection{ id handle } userErrors{ field message } } }"""
PUB = """mutation($id:ID!, $input:[PublicationInput!]!){ publishablePublish(id:$id, input:$input){ userErrors{ field message } } }"""


def run():
    ids = []
    for h, title, desc, img, rules in COLLECTIONS:
        url = FILES.get(f"altura-{img}.jpg", {}).get("url")
        inp = {"title": title, "handle": h, "descriptionHtml": f"<p>{desc}</p>", "sortOrder": "BEST_SELLING",
               "ruleSet": {"appliedDisjunctively": False, "rules": [{"column": c, "relation": r, "condition": v} for c, r, v in rules]}}
        if url:
            inp["image"] = {"src": url, "altText": title}
        ex = gql(COLL_Q, {"h": h})["collectionByHandle"]
        if ex:
            inp["id"] = ex["id"]; inp.pop("ruleSet")
            cid = gql(COLL_U, {"input": inp})["collectionUpdate"]["collection"]["id"]
        else:
            cid = gql(COLL_C, {"input": inp})["collectionCreate"]["collection"]["id"]
        ids.append(cid); print("collection", h)
    for c in COFFEES:
        p = gql(SET, {"input": coffee_input(c), "id": {"handle": c["handle"]}})["productSet"]["product"]
        ids.append(p["id"]); print("product", p["handle"])
    for g in GEAR:
        p = gql(SET, {"input": gear_input(g), "id": {"handle": g["handle"]}})["productSet"]["product"]
        ids.append(p["id"]); print("product", p["handle"])
    for i in ids:
        try:
            gql(PUB, {"id": i, "input": [{"publicationId": ONLINE_STORE}]})
        except Exception as e:
            print("publish", i, str(e)[:120])
    print("done", len(ids))


if __name__ == "__main__":
    run()
