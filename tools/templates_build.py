"""Writes theme/templates/index.json, page.about.json, page.contact.json with demo content."""
import json, os

T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "theme", "templates")
img = lambda n: f"shopify://shop_images/altura-{n}.jpg"


def blocks(prefix, items):
    return {f"{prefix}{i}": b for i, b in enumerate(items)}, [f"{prefix}{i}" for i in range(len(items))]


def section(type_, settings, items=None, prefix="b"):
    s = {"type": type_, "settings": settings}
    if items:
        s["blocks"], s["block_order"] = blocks(prefix, items)
    return s


slide = lambda **k: {"type": "slide", "settings": k}
stat = lambda n, l: {"type": "stat", "settings": {"number": n, "label": l}}
q = lambda a, b: {"type": "question", "settings": {"question": a, "answer": b}}

index = {
    "hero": section("hero", {"height": "full", "autoplay": 7}, [
        slide(image=img("hero-farm"), eyebrow="Single origin · Perú", title="Grown higher.\nTastes <em>brighter.</em>",
              text="Direct-trade specialty coffee from small family farms 1,600–2,300 m up in the Peruvian Andes. Roasted to order in Lima.",
              btn1_label="Shop coffee", btn1_link="shopify://collections/coffee", btn2_label="Our story", btn2_link="shopify://pages/about", align="left"),
        slide(image=img("hero-hands"), eyebrow="New harvest", title="Picked by hand.\nOne cherry <em>at a time.</em>",
              text="The 2026 harvest is in. Meet the families behind every bag.",
              btn1_label="Shop single origin", btn1_link="shopify://collections/single-origin", btn2_label="Meet the growers", btn2_link="shopify://blogs/journal", align="left"),
        slide(image=img("hero-roaster"), eyebrow="Roasted twice a week", title="From the roaster\nto your <em>door.</em>",
              text="Every order is roasted on Tuesday or Friday and shipped within 24 hours.",
              btn1_label="Shop best sellers", btn1_link="shopify://collections/best-sellers", btn2_label="", align="center"),
    ]),
    "marquee": section("marquee", {"style": "", "speed": 45}, [{"type": "text", "settings": {"text": t}} for t in
                       ["Direct trade", "Roasted weekly", "Grown above 1,600 m", "Hand-picked", "Compostable bags", "Carbon-neutral shipping"]]),
    "featured": section("featured-collection", {"eyebrow": "This week's roast", "title": "Fresh from the roaster", "layout": "rail", "columns": 4, "limit": 8,
                                                "button_label": "Shop all coffee", "button_link": "shopify://collections/coffee", "style": ""},
                        [{"type": "collection", "settings": {"collection": c, "label": l}} for c, l in
                         [("coffee", "All coffee"), ("single-origin", "Single origin"), ("best-sellers", "Best sellers"), ("brewing-gear", "Gear")]]),
    "story": section("image-with-text", {"image": img("about-roaster"), "image_2": img("about-cherries"), "reverse": False, "eyebrow": "Our story",
                                         "title": "Coffee that pays it forward",
                                         "text": "<p>We buy directly from 42 family farms across the Peruvian Andes, pay an average of 2.4× the fair-trade minimum and visit every one of them each harvest. No middlemen, no mystery — just extraordinary coffee and the people who grow it.</p>",
                                         "button_label": "Read our story", "button_link": "shopify://pages/about", "style": ""},
                     [stat("42", "Partner farms"), stat("2.4×", "Fair-trade price"), stat("1,950 m", "Highest farm")]),
    "collections": section("collection-list", {"eyebrow": "Shop by", "title": "Find your ritual", "link_label": "All collections", "bento": True, "style": ""},
                           [{"type": "collection", "settings": {"collection": c, "title": t, "image": img(i)}} for c, t, i in
                            [("single-origin", "Single origin", "tile-single"), ("blends", "Espresso & blends", "tile-blends"),
                             ("brewing-gear", "Brewing gear", "tile-gear"), ("gifts", "Gifts & bundles", "tile-gifts")]]),
    "origins": section("origins", {"eyebrow": "Origins", "title": "Five regions. One mountain range.",
                                   "text": "Every Altura coffee is traceable to the farm, the altitude and the family who grew it. Hover a region to explore.",
                                   "badge": "Every farm visited in person each harvest"},
                       [{"type": "origin", "settings": dict(zip(["name", "altitude", "text", "process", "variety", "image", "product"], o))} for o in [
                           ("Cajamarca", "1,950 masl", "Cool nights, volcanic soil and the shade of native pacay trees. Home of our Geisha.", "Washed", "Geisha", img("origin-cajamarca"), "cajamarca-geisha"),
                           ("Villa Rica", "1,650 masl", "A cloud-forest valley in Pasco where coffee grows between banana and avocado trees.", "Honey", "Caturra, Typica", img("origin-villarica"), "villa-rica-honey"),
                           ("Cusco", "1,800 masl", "Steep terraces in the valleys below Machu Picchu, worked by Quechua families for generations.", "Natural", "Red Bourbon", img("origin-cusco"), "cusco-bourbon-natural"),
                           ("Amazonas", "1,850 masl", "Emerald cloud forest near the Gocta waterfall. Bright, crisp, endlessly drinkable coffees.", "Washed", "Typica", img("origin-amazonas"), "amazonas-washed"),
                           ("Puno", "2,100 masl", "Some of the highest coffee on earth. Cold nights slow ripening and build deep berry sweetness.", "Washed", "Bourbon", img("origin-puno"), "puno-tunki"),
                       ]]),
    "drop": section("countdown-drop", {"image": img("drop-geisha"), "eyebrow": "Limited release · 120 bags", "title": "The Geisha drop",
                                       "text": "Jasmine, white peach and bergamot. Our rarest lot of the year — when this harvest is gone, it's gone until next June.",
                                       "end": "2026-12-01 09:00", "product": "cajamarca-geisha", "button_label": "Reserve a bag"}),
    "look": section("shop-the-look", {"image": img("look-setup"), "eyebrow": "Shop the ritual", "title": "The slow morning set",
                                      "text": "Everything you need for a café-quality pour-over at home. Tap the dots to explore."},
                    [{"type": "hotspot", "settings": {"product": p, "x": x, "y": y}} for p, x, y in
                     [("gooseneck-kettle", 20, 68), ("glass-brewer", 48, 55), ("digital-brew-scale", 47, 82), ("ceramic-pour-over-dripper", 46, 38)]]),
    "brew": section("brew-calculator", {"eyebrow": "Brew better", "title": "Your perfect cup, calculated.",
                                        "text": "Pick a method, choose how many cups and how strong you like it. We'll do the math — and give you the steps."}),
    "reviews": section("testimonials", {"eyebrow": "Loved by coffee people", "press": "Crema Quarterly, The Daily Grind, Origin Notes, Slow Mornings, Field & Cup", "style": ""},
                       [{"type": "quote", "settings": dict(zip(["quote", "author", "role", "avatar"], t))} for t in [
                           ("The Geisha genuinely tastes like jasmine tea. I didn't know coffee could do that.", "Mariana T.", "Subscriber since 2023", img("person-1")),
                           ("Roasted on Tuesday, at my door on Thursday. You can taste the difference in every cup.", "Daniel R.", "Home barista", img("person-2")),
                           ("We switched our café to Altura's House Espresso and our regulars noticed within a week.", "Joaquín P.", "Café owner, Lima", img("person-3")),
                       ]]),
    "usps": section("usps", {"style": "section--surface"}, [{"type": "item", "settings": dict(zip(["icon", "title", "text"], u))} for u in [
        ("flame", "Roasted to order", "Every Tuesday and Friday, shipped within 24 h."), ("truck", "Free shipping over $60", "Tracked, carbon-neutral delivery."),
        ("leaf", "Direct trade", "2.4× the fair-trade price, paid to the grower."), ("heart", "Love it or it's on us", "Free replacement or a full refund.")]]),
    "journal": section("journal", {"blog": "journal", "eyebrow": "Journal", "title": "Stories from the source"}),
    "faq": section("faq", {"eyebrow": "Questions", "title": "Good to know", "text": "Can't find what you need? Our team replies within a few hours, seven days a week.",
                           "button_label": "Contact us", "button_link": "shopify://pages/contact", "open_first": True, "style": ""}, [
        q("How fresh is the coffee?", "<p>We roast every Tuesday and Friday and ship within 24 hours. Your coffee will never be more than four days off the roaster when it arrives.</p>"),
        q("Which grind should I choose?", "<p>Whole bean stays fresh longest. Choose <strong>Filter</strong> for pour-over, drip and French press, and <strong>Espresso</strong> for espresso machines and moka pots.</p>"),
        q("Do you offer subscriptions?", "<p>Yes — save 15% with a flexible subscription delivered every 2, 3 or 4 weeks. Skip, swap or cancel any time.</p>"),
        q("Is the packaging recyclable?", "<p>Our bags are home-compostable and our boxes are 100% recycled cardboard.</p>"),
        q("Do you ship internationally?", "<p>We ship to more than 40 countries. Rates and delivery times are calculated at checkout.</p>")]),
    "gram": section("gallery-grid", {"eyebrow": "@altura.coffee", "title": "Brewed by you"}, [{"type": "image", "settings": {"image": img(f"gram-{i}"), "link": ""}} for i in range(1, 7)]),
    "newsletter": section("newsletter", {"eyebrow": "The Altura letter", "title": "10% off your first bag.",
                                         "text": "Harvest news, brew guides and first access to limited lots. One email a week, never more.", "style": "section--accent"}),
}

about = {
    "hero": section("page-hero", {"image": img("origin-cusco"), "height": 80, "eyebrow": "Our story", "title": "We go to the source.",
                                  "text": "Altura started in 2016 with one farm, one roaster and a simple idea: the people who grow extraordinary coffee should be paid like it."}),
    "split": section("image-with-text", {"image": img("hero-hands"), "image_2": img("about-cherries"), "reverse": True, "eyebrow": "Direct trade", "title": "No middlemen. No mystery.",
                                         "text": "<p>We travel to every farm we buy from, every harvest. We cup the coffee together, agree on a price before it's picked and pay growers directly — on average 2.4× the fair-trade minimum.</p><p>That price funds new drying beds, better processing and school fees. It also means we get first pick of the very best lots.</p>",
                                         "button_label": "Shop single origin", "button_link": "shopify://collections/single-origin", "style": ""},
                     [stat("42", "Partner farms"), stat("$1.2M", "Paid to growers in 2025"), stat("100%", "Traceable")]),
    "timeline": section("timeline", {"eyebrow": "Milestones", "title": "From one farm to forty-two"}, [{"type": "event", "settings": dict(zip(["year", "title", "text"], e))} for e in [
        ("2016", "One farm, one roaster", "We roast our first 60 kg from a single farm in Villa Rica in a borrowed 5 kg roaster."),
        ("2018", "The roastery opens", "Our café and roastery opens in Miraflores, Lima. Wholesale to the first 10 cafés."),
        ("2020", "Direct trade, everywhere", "Every coffee we sell is bought directly from the grower at a pre-agreed price."),
        ("2023", "Compostable everything", "All bags become home-compostable; shipping becomes carbon-neutral."),
        ("2026", "42 farms, 5 regions", "Coffee from Cajamarca to Puno, shipped to 40+ countries.")]]),
    "dark": section("image-with-text", {"image": img("about-roaster"), "reverse": False, "eyebrow": "The roastery", "title": "Roasted in small batches in Lima",
                                        "text": "<p>We roast on a 15 kg drum roaster twice a week, profiling every coffee to bring out its origin — never to hide it.</p>",
                                        "button_label": "Visit the café", "button_link": "shopify://pages/contact", "style": "section--dark"}),
    "newsletter": section("newsletter", {"eyebrow": "The Altura letter", "title": "Follow the harvest.", "text": "Farm visits, new lots and brew guides in your inbox.", "style": "section--accent"}),
}

contact = {
    "main": section("main-page", {"eyebrow": "Get in touch"}),
    "form": section("contact-form", {"image": img("cafe"), "title": "Send us a note",
                                     "info": "<p><strong>Roastery & café</strong><br>Av. Larco 345, Miraflores, Lima</p><p><strong>Hours</strong><br>Mon–Sat · 8am – 7pm</p><p><strong>Email</strong><br>hola@altura.coffee</p>"}),
    "faq": section("faq", {"eyebrow": "Quick answers", "title": "Before you write", "text": "These cover most questions we get.", "button_label": "", "open_first": False, "style": "section--surface"}, [
        q("Where is my order?", "<p>You'll get a tracking link by email as soon as your coffee ships — usually within 24 hours of roasting.</p>"),
        q("Can I change my grind after ordering?", "<p>Yes, until roasting day. Just reply to your order confirmation.</p>"),
        q("Do you supply cafés?", "<p>We do — see our Wholesale page or write to wholesale@altura.coffee.</p>")]),
}

for name, secs in [("index", index), ("page.about", about), ("page.contact", contact)]:
    json.dump({"sections": secs, "order": list(secs)}, open(os.path.join(T, f"{name}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ok")
