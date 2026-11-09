"""Pages, blog + articles, menus for the Altura demo. Idempotent-ish (looks up by handle)."""
import json, os
from gql import gql

FILES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media", "uploaded.json")))
url = lambda n: FILES[f"altura-{n}.jpg"]["url"]

PAGES = [
    ("about", "Our Story", "about", "<p>Altura started in 2016 with one farm, one roaster and a simple idea: the people who grow extraordinary coffee should be paid like it.</p>"),
    ("contact", "Contact", "contact", "<p>Questions about an order, wholesale or visiting the roastery? We usually reply within a few hours.</p>"),
    ("shipping-returns", "Shipping & Returns", None,
     "<h2>Shipping</h2><p>We roast every Tuesday and Friday and ship within 24 hours of roasting. Orders over $60 ship free within the US. International shipping is available to 40+ countries.</p>"
     "<h2>Returns</h2><p>Not in love with a coffee? Tell us within 30 days and we'll send a different one or refund you in full — no need to send anything back.</p>"
     "<h2>Gear</h2><p>Unused gear can be returned within 30 days in its original packaging.</p>"),
    ("wholesale", "Wholesale & Cafés", None,
     "<p>We supply more than 60 cafés, restaurants and offices with fresh-roasted Peruvian coffee, equipment and barista training.</p>"
     "<ul><li>Weekly roasting, delivered within 48 hours</li><li>Free espresso dial-in and staff training</li><li>Custom blends from 20 kg/month</li></ul>"
     "<p>Write to <a href=\"mailto:wholesale@altura.coffee\">wholesale@altura.coffee</a> and we'll send you samples.</p>"),
    ("faq", "FAQ", None,
     "<h3>How fresh is the coffee?</h3><p>Roasted to order every Tuesday and Friday and shipped within 24 hours.</p>"
     "<h3>Which grind should I choose?</h3><p>Whole bean stays fresh longest. Choose Filter for pour-over, drip and French press, and Espresso for espresso machines and moka pots.</p>"
     "<h3>Do you ship internationally?</h3><p>Yes, to more than 40 countries. Rates are calculated at checkout.</p>"),
]

ARTICLES = [
    ("the-perfect-pour-over", "The perfect pour-over in 6 steps", "Brew guides", "journal-brew",
     "<p>A great pour-over isn't about expensive gear — it's about a few numbers and a little patience. Here's the recipe we use every morning at the roastery.</p>"
     "<h2>1. Weigh your coffee</h2><p>Use 15 g of coffee for every 250 ml of water. A ratio of 1:16 is a great starting point for light and medium roasts.</p>"
     "<h2>2. Grind just before brewing</h2><p>Aim for something like coarse sand. Too fine and the brew will taste bitter; too coarse and it will be sour and thin.</p>"
     "<h2>3. Bloom</h2><p>Pour twice the coffee's weight in water and wait 40 seconds. You'll see the bed rise as CO₂ escapes.</p>"
     "<blockquote>The bloom is where the magic starts — fresh coffee should puff up like bread dough.</blockquote>"
     "<h2>4. Pour in slow spirals</h2><p>Keep the water level steady and avoid pouring directly on the filter paper.</p>"
     "<h2>5. Let it drain</h2><p>Total time should be around 3 minutes.</p><h2>6. Taste and adjust</h2><p>Sour? Grind finer. Bitter? Grind coarser. That's it.</p>"),
    ("meet-the-huaman-family", "Meet the Huamán family, growers of our Geisha", "Origins", "journal-farm",
     "<p>At 1,950 metres above sea level, in the hills of San Ignacio, Cajamarca, the Huamán family farm a single hectare of Geisha trees planted in 2014.</p>"
     "<p>Every cherry is hand-picked at peak ripeness — up to six passes per tree each harvest. It's slow, careful work, and it shows in the cup: jasmine, white peach and a clean, tea-like finish.</p>"
     "<blockquote>We don't sell coffee. We sell the work of a whole year.</blockquote>"
     "<p>We've bought their entire Geisha lot since 2019, paying 3.1× the fair-trade minimum. This year there are only 120 bags.</p>"),
    ("espresso-at-home", "Café-quality espresso at home", "Brew guides", "journal-espresso",
     "<p>Dialing in espresso at home can feel like a science experiment. These three variables get you 90% of the way there.</p>"
     "<h2>Dose</h2><p>Start with 18 g of coffee in a double basket.</p><h2>Yield</h2><p>Aim for 36 g of liquid espresso — a 1:2 ratio.</p>"
     "<h2>Time</h2><p>25–30 seconds. If it runs faster, grind finer; slower, grind coarser.</p>"
     "<p>Our House Espresso is roasted specifically to be forgiving — chocolatey and sweet even when the shot isn't perfect.</p>"),
]


def page(handle, title, suffix, body):
    ex = gql("query($q:String!){ pages(first:1, query:$q){ nodes{ id handle } } }", {"q": f"handle:{handle}"})["pages"]["nodes"]
    inp = {"title": title, "body": body, "isPublished": True, "templateSuffix": suffix}
    if ex:
        r = gql("mutation($id:ID!,$p:PageUpdateInput!){ pageUpdate(id:$id, page:$p){ page{ id } userErrors{ field message } } }", {"id": ex[0]["id"], "p": inp})
        return ex[0]["id"]
    inp["handle"] = handle
    return gql("mutation($p:PageCreateInput!){ pageCreate(page:$p){ page{ id } userErrors{ field message } } }", {"p": inp})["pageCreate"]["page"]["id"]


def blog():
    ex = gql("{ blogs(first:10){ nodes{ id handle } } }")["blogs"]["nodes"]
    for b in ex:
        if b["handle"] == "journal":
            return b["id"]
    return gql("mutation($b:BlogCreateInput!){ blogCreate(blog:$b){ blog{ id } userErrors{ field message } } }",
               {"b": {"title": "The Journal", "handle": "journal"}})["blogCreate"]["blog"]["id"]


def articles(blog_id):
    for i, (h, title, tag, img, body) in enumerate(ARTICLES):
        ex = gql("query($q:String!){ articles(first:1, query:$q){ nodes{ id } } }", {"q": f"handle:{h}"})["articles"]["nodes"]
        inp = {"title": title, "body": body, "tags": [tag], "isPublished": True, "image": {"url": url(img), "altText": title},
               "summary": body.split("</p>")[0] + "</p>", "publishDate": f"2026-1{0 if i else 1}-0{i + 3}T10:00:00Z"}
        if ex:
            gql("mutation($id:ID!,$a:ArticleUpdateInput!){ articleUpdate(id:$id, article:$a){ article{ id } userErrors{ field message } } }", {"id": ex[0]["id"], "a": inp})
        else:
            inp.update({"blogId": blog_id, "handle": h, "author": {"name": "Lucía Ramos"}})
            gql("mutation($a:ArticleCreateInput!){ articleCreate(article:$a){ article{ id } userErrors{ field message } } }", {"a": inp})
        print("article", h)


def ids():
    q = gql("""{ collections(first:20){ nodes{ id handle } } pages(first:20){ nodes{ id handle } } blogs(first:5){ nodes{ id handle } }
               products(first:50){ nodes{ id handle } } menus(first:10){ nodes{ id handle } } }""")
    return {k: {n["handle"]: n["id"] for n in v["nodes"]} for k, v in q.items()}


def item(title, typ, rid=None, url_=None, items=None):
    d = {"title": title, "type": typ, "items": items or []}
    if rid: d["resourceId"] = rid
    if url_: d["url"] = url_
    return d


def menus():
    I = ids(); C, P, B, PR = I["collections"], I["pages"], I["blogs"], I["products"]
    main = [
        item("Coffee", "COLLECTION", C["coffee"], items=[
            item("By type", "COLLECTION", C["coffee"], items=[item("Single origin", "COLLECTION", C["single-origin"]), item("Espresso & blends", "COLLECTION", C["blends"]),
                                                                  item("Limited releases", "COLLECTION", C["limited-releases"]), item("Best sellers", "COLLECTION", C["best-sellers"])]),
            item("By roast", "COLLECTION", C["coffee"], items=[item("Light roast", "HTTP", url_="/collections/coffee/light-roast"), item("Medium roast", "HTTP", url_="/collections/coffee/medium-roast"),
                                                                   item("Dark roast", "HTTP", url_="/collections/coffee/dark-roast"), item("Decaf", "PRODUCT", PR["chanchamayo-decaf"])]),
            item("By origin", "COLLECTION", C["single-origin"], items=[item("Cajamarca", "PRODUCT", PR["cajamarca-geisha"]), item("Villa Rica", "PRODUCT", PR["villa-rica-honey"]),
                                                                           item("Cusco", "PRODUCT", PR["cusco-bourbon-natural"]), item("Puno", "PRODUCT", PR["puno-tunki"])]),
        ]),
        item("Brewing Gear", "COLLECTION", C["brewing-gear"]),
        item("Gifts", "COLLECTION", C["gifts"]),
        item("Journal", "BLOG", B["journal"]),
        item("About", "PAGE", P["about"], items=[item("Our story", "PAGE", P["about"]), item("Wholesale", "PAGE", P["wholesale"]), item("Contact", "PAGE", P["contact"])]),
    ]
    shop = [item("All coffee", "COLLECTION", C["coffee"]), item("Single origin", "COLLECTION", C["single-origin"]), item("Brewing gear", "COLLECTION", C["brewing-gear"]),
            item("Gifts", "COLLECTION", C["gifts"]), item("Search", "SEARCH", url_="/search")]
    help_ = [item("Shipping & returns", "PAGE", P["shipping-returns"]), item("FAQ", "PAGE", P["faq"]), item("Wholesale", "PAGE", P["wholesale"]),
             item("Contact", "PAGE", P["contact"]), item("Journal", "BLOG", B["journal"])]
    UPD = "mutation($id:ID!,$t:String!,$h:String!,$i:[MenuItemUpdateInput!]!){ menuUpdate(id:$id,title:$t,handle:$h,items:$i){ menu{ id } userErrors{ field message } } }"
    CRE = "mutation($t:String!,$h:String!,$i:[MenuItemCreateInput!]!){ menuCreate(title:$t,handle:$h,items:$i){ menu{ id } userErrors{ field message } } }"
    for h, t, items in [("main-menu", "Main menu", main), ("footer", "Footer menu", help_), ("footer-shop", "Footer shop", shop)]:
        if h in I["menus"]:
            gql(UPD, {"id": I["menus"][h], "t": t, "h": h, "i": items})
        else:
            gql(CRE, {"t": t, "h": h, "i": items})
        print("menu", h)


if __name__ == "__main__":
    for p in PAGES:
        page(*p); print("page", p[0])
    b = blog(); articles(b); menus()
