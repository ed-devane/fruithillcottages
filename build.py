#!/usr/bin/env python3
"""Generates the Fruit Hill Cottages static site.

Edit the text in PAGES below, then run:  python3 build.py
Every page is written to <slug>/index.html so URLs match the old
Squarespace site (e.g. /coach-house, /kirbys-1).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Image sizes (as served at 2500px max) so the browser reserves space while loading.
DIMS = {
    "home-hero": (2500, 1667), "home-cottages": (1440, 960), "home-region": (2500, 1667),
    "home-book": (2500, 3333), "about-hero": (1920, 1076), "rates-coach-house": (2500, 1667),
    "rates-kirbys": (1440, 960), "region-1": (1600, 600), "region-2": (1024, 683),
    "region-3": (1024, 681), "coach-hero": (2500, 1667),
    "coach-01": (1600, 1200), "coach-02": (1200, 1600), "coach-03": (1600, 1200),
    "coach-04": (1200, 1600), "coach-05": (2500, 3333), "coach-06": (2500, 3333),
    "coach-07": (2500, 3333), "coach-08": (2500, 3333), "coach-09": (2500, 1875),
    "coach-10": (2500, 3333), "kirbys-hero": (1440, 960),
    "kirbys-01": (1200, 1600), "kirbys-02": (1200, 1600), "kirbys-03": (1600, 1200),
    "kirbys-04": (1600, 1200), "kirbys-05": (1600, 1200), "kirbys-06": (2500, 1875),
    "kirbys-07": (1200, 1600), "kirbys-08": (2500, 3333),
}

# Email is stored in two parts and joined by assets/menu.js in the browser, so
# the full address never appears in the HTML (or in this public file) for spam
# harvesters to find.
EMAIL_USER, EMAIL_DOMAIN = "fruithill", "gmail.com"
PHONE_DISPLAY = "(+353) 51-388694"
PHONE_TEL = "+35351388694"
MOBILE_DISPLAY = "(+353) 87 9597474"
MOBILE_TEL = "+353879597474"
ADDRESS = "Fruit Hill, Campile, New Ross, Co. Wexford, Y34V128"
INSTAGRAM = "https://www.instagram.com/fruithillcottages/"
FACEBOOK = "https://www.facebook.com/Fruit-Hill-Irish-Holiday-Cottages-122177474511639"
AIRBNB_COACH = "https://www.airbnb.com/h/fruithill1"
AIRBNB_KIRBYS = "https://www.airbnb.com/h/fruithill2"

IG_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.6" r="1.2" fill="currentColor"/></svg>'
FB_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5h1.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/></svg>'


def img(name, alt, cls="", lazy=True, sizes="100vw"):
    w, h = DIMS[name]
    return (f'<img src="/images/{name}.jpg" alt="{alt}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""}{f" class=\"{cls}\"" if cls else ""}>')


def gallery(prefix, n, label):
    items = "\n".join(
        f'      <a href="/images/{prefix}-{i:02d}.jpg" class="gallery-item">{img(f"{prefix}-{i:02d}", f"{label} photo {i}", sizes="(max-width: 700px) 100vw, 50vw")}</a>'
        for i in range(1, n + 1))
    return f'    <div class="gallery">\n{items}\n    </div>'


def framed_hero(name, alt, inner=""):
    return f'''  <section class="frame">
    <div class="hero">
      {img(name, alt, lazy=False)}
      {f'<div class="hero-text">{inner}</div>' if inner else ''}
    </div>
  </section>'''


def mail(text=None):
    """Email link. Without JavaScript it reads "fruithill [at] gmail [dot] com"
    and links to the contact page; menu.js swaps in the real address."""
    show = text is None
    if show:
        text = f'{EMAIL_USER} [at] {EMAIL_DOMAIN.replace(".", " [dot] ")}'
    return (f'<a class="email" href="/contact" data-u="{EMAIL_USER}" data-d="{EMAIL_DOMAIN}"'
            f'{" data-show" if show else ""}>{text}</a>')


HEADER = f'''<header class="site-header">
  <a class="site-title" href="/">Fruit Hill Cottages</a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav id="site-nav" class="site-nav">
    <div class="nav-folder">
      <a href="/about-us" class="nav-folder-title">About</a>
      <div class="nav-folder-items">
        <a href="/about-us">About Us</a>
        <a href="/cottages-rates">Cottages &amp; Rates</a>
        <a href="/region">Region</a>
      </div>
    </div>
    <a href="/coach-house">Coach House</a>
    <a href="/kirbys-1">Kirby’s</a>
    <a href="/contact">Contact</a>
    <span class="social">
      <a href="{INSTAGRAM}" aria-label="Instagram">{IG_SVG}</a>
      <a href="{FACEBOOK}" aria-label="Facebook">{FB_SVG}</a>
    </span>
    <a href="/book-a-stay" class="btn">Book a Stay</a>
  </nav>
</header>'''

FOOTER = f'''<footer class="site-footer">
  <div class="social">
    <a href="{INSTAGRAM}" aria-label="Instagram">{IG_SVG}</a>
    <a href="{FACEBOOK}" aria-label="Facebook">{FB_SVG}</a>
  </div>
  <h2>Fruit Hill Cottages</h2>
  <p>{ADDRESS}</p>
  <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br>{mail()}</p>
</footer>'''


PAGES = {}

PAGES["index"] = ("Fruit Hill Cottages", "Traditional self-catering farm cottages in the grounds of 18th-century Fruit Hill House, Campile, Co. Wexford.", f'''
{framed_hero("home-hero", "Garden and stone cottage at Fruit Hill",
  '<h1>Traditional farm cottages set in the grounds of Fruit Hill House</h1><a class="btn btn-light" href="/book-a-stay">Book a Stay</a>')}
  <section class="intro">
    <h2>Set in the landscaped grounds of 18th Century Fruit Hill House, these traditional self-catering farm cottages make an ideal base for touring South-East Ireland.</h2>
  </section>
  <section class="cards">
    <div class="card">
      <a href="/cottages-rates">{img("home-cottages", "A whitewashed cottage among autumn trees", sizes="(max-width: 700px) 100vw, 45vw")}</a>
      <h3>Cottages</h3>
      <p>Enjoy Irish country living at its finest in either of our beautiful rural retreats.</p>
      <p><a class="more" href="/cottages-rates">Learn More</a></p>
    </div>
    <div class="card">
      <a href="/region">{img("home-region", "Cows grazing in a green field", sizes="(max-width: 700px) 100vw, 45vw")}</a>
      <h3>Region</h3>
      <p>Discover Ireland’s sunny South-East, where vibrant history and modern life meet.</p>
      <p><a class="more" href="/region">Learn More</a></p>
    </div>
  </section>
  <section class="frame">
    <a class="hero hero-link" href="/book-a-stay">
      {img("home-book", "Tulips along a garden path beside the glasshouse")}
      <div class="hero-text"><h1 class="underline">Book a Stay</h1></div>
    </a>
  </section>''')

PAGES["about-us"] = ("About Us — Fruit Hill Cottages", "The story of Fruit Hill House and its cottages, restored by the Devane family since 1995.", f'''
{framed_hero("about-hero", "Fruit Hill House and grounds")}
  <section class="text">
    <h2>About Us</h2>
    <p>The restoration of Fruit Hill House, grounds and cottages has been a labour of love for the Devane family since 1995, when all the buildings on the farm were either derelict or in very bad repair. Our restoration work was partly completed by June 2002, when the first visitors came to stay in the Coach House. Kirby’s, the 19th century converted stable block, was our next building project in 2008. Since then, we have welcomed countless visitors who have enjoyed the secluded charm of this heritage property set apart from the busy world in a mature garden.</p>
    <p>For people in search of somewhere special with a true sense of place, Fruit Hill is ideal as a base for exploring Wexford, Waterford, Kilkenny, and the beauty and majesty of the Hook Peninsula with its sandy coves, wild and rocky seascapes, ancient monasteries, and Europe’s oldest lighthouse. The relaxed atmosphere and friendly welcome, together with every home comfort, make these cottages ideal for families who want to experience the Irish countryside.</p>
    <p>There is a wide range of <a href="/region">attractions and activities</a> on offer locally, so there’s no need to spend all day in a car. Less than an hour’s drive in any direction will take you to a new adventure, and then back to an open fire, books, tv, and a comfy bed.</p>
    <p>Susan and Richard are always on hand if something is needed, or just for a chat about plans for a day out. Please {mail("email")} or <a href="/contact">call</a> if you have any questions. We look forward to welcoming you to Fruit Hill.</p>
  </section>''')

PAGES["cottages-rates"] = ("Cottages & Rates — Fruit Hill Cottages", "The Coach House (sleeps 6) and Kirby’s (sleeps 4), self-catering cottages at Fruit Hill, Co. Wexford.", f'''
  <section class="text center">
    <h2>Cottages &amp; Rates</h2>
    <p>Enjoy Irish country living at its finest in our beautiful rural retreats.</p>
  </section>
  <section class="cards">
    <div class="card">
      <a href="/coach-house">{img("rates-coach-house", "The Coach House", sizes="(max-width: 700px) 100vw, 45vw")}</a>
      <h3><a href="/coach-house"><em>The Coach House</em></a></h3>
      <h4>Sleeps 6</h4>
      <p>With ample room for a family or group of friends, this traditional farm house looks out on to extensive and picturesque gardens.</p>
    </div>
    <div class="card">
      <a href="/kirbys-1">{img("rates-kirbys", "Kirby’s stone cottage", sizes="(max-width: 700px) 100vw, 45vw")}</a>
      <h3><a href="/kirbys-1"><em>Kirby’s</em></a></h3>
      <h4>Sleeps 4</h4>
      <p>This newly-refurbished old stone cottage bordered with magnificent mature trees boasts stunning views across the pasture.</p>
    </div>
  </section>''')

PAGES["region"] = ("Region — Fruit Hill Cottages", "Things to see and do around Fruit Hill in Ireland’s South-East: Hook Lighthouse, beaches, Wexford, New Ross.", f'''
  <section class="text">
    <h4 class="kicker"><em>Region</em></h4>
    <h3>Fruit Hill is located in Ireland’s South-East, where ancient history and modern life meet. Enjoy memorable food experiences, wander down the cobbled streets of medieval towns, and explore the gorgeous gardens of this scenic region.</h3>
    {img("region-1", "South-East Ireland coastline", sizes="(max-width: 860px) 100vw, 800px")}
    <p>Reading through the visitors’ book you will see that Hook Lighthouse is universally recommended. A half hour’s drive from Fruit Hill, the winding route to Europe’s oldest lighthouse is picturesque and interesting. Every age group will enjoy the tour of this historic building with its dramatic backdrop of rocky seascape. Slade village, Duncannon Fort and Loftus Hall are worth a visit too, and there is an excellent visitors’ centre and cafe at the Hook. There are 14 beautiful sandy beaches around the Peninsula, and at certain times of year you can see dolphins and whales swimming out at sea. Horse riding on the strand is an option in Fethard on Sea (one of several in this horse-loving county).</p>
    {img("region-2", "Hook Lighthouse", sizes="(max-width: 860px) 100vw, 800px")}
    {img("region-3", "A boardwalk in the Wexford countryside", sizes="(max-width: 860px) 100vw, 800px")}
    <p>Follow the Wexford coastal drive and stop off at pretty Kilmore Quay with its thatched cottages and excellent sea food restaurants. Wexford town has a famous Opera House, and is a nice place for a stroll and some shopping. Fine foods and art exhibitions at Green Acres or the Wexford Arts Centre. Johnstown Castle is open to visitors, and the Irish National Heritage Park just outside Wexford is another popular place to visit, especially with children. Probably the biggest hit is the tour of Dunbrody Heritage Ship. This is in nearby New Ross, and everyone will enjoy exploring the reconstructed famine ship with guides in costume to give a flavour of what life was like on board during the six-week crossing to America in the 19th Century.</p>
  </section>''')

PAGES["coach-house"] = ("Coach House — Fruit Hill Cottages", "The Coach House at Fruit Hill: a 300-year-old farmhouse sleeping 6, with open fire, three bedrooms and garden views.", f'''
{framed_hero("coach-hero", "The Coach House and garden")}
  <section class="text">
    <h3>The Coach House</h3>
    <p>The 300-year-old Coach House was converted in 1995 to a comfortable family home. It is the larger of the two cottages, with ample room for a family or group of friends. The kitchen table is vast enough for a jigsaw down one end not to disrupt dinner, and for younger children the area under the stairs is a secret little play house. The Coach House is fully-equipped, so the kitchen has a dishwasher, laundry room, and everything required by the chef.</p>
    <p>The living room with its open fireplace and well-stocked book shelves, big armchairs, and views of the garden is Irish country living at its finest. You may not want to go out at all except to stroll in the grounds.</p>
    <p>There are two bathrooms: shower downstairs and bath upstairs, and any of the three bedrooms (one on the ground floor) is large enough to accommodate the cot or an extra camp bed if requested. All beds have good comfortable mattresses and pillows.</p>
    <p>The Devane family has been welcoming visitors from all over the world to Fruit Hill since 2002, and Susan or Richard are always available if help or advice is needed. They can arrange for a reliable babysitter if required.</p>
    <p>An initial supply of fuel for the fires is provided in the welcome pack for each cottage. Also included tea/coffee/milk/sugar and homemade cake or scones.</p>
    <p>You can book the Coach House at <a href="{AIRBNB_COACH}">airbnb.com/h/fruithill1</a>.</p>
  </section>
  <section class="wide">
{gallery("coach", 10, "Coach House")}
  </section>''')

PAGES["kirbys-1"] = ("Kirby’s — Fruit Hill Cottages", "Kirby’s at Fruit Hill: a refurbished old stone cottage sleeping 4, with open fire and views across the pasture.", f'''
{framed_hero("kirbys-hero", "Kirby’s stone cottage")}
  <section class="text">
    <h2>Kirby’s</h2>
    <p>Newly refurbished, this old stone cottage has the atmosphere and feel of an early Irish home, with an open fire in the kitchen/living room. Kirby’s has the advantage of higher ceilings and bigger than traditional windows to let in light and allow you to enjoy the view across pastures bordered with magnificent mature trees.</p>
    <p>The name “Kirby’s” came about because the initials WK are to be seen carved in a stone at the back of the house. (William Kirby came to Fruit Hill House as head gardener in the early 1900’s, and eventually, by a twist of fate, came to own the property; he reared 10 children here).</p>
    <p>The comfortable sleeping accommodation comprises one double room beside the shower room, and a bright and airy twin room at the far side of the kitchen. A cot and highchair can always be provided, and there are plenty of toys and DVDs to keep children occupied. Electric storage heaters and an open fire ensure that nowhere could be cosier at the end of a day’s touring the surrounding counties.</p>
    <p>The Devane family has been welcoming visitors from all over the world to Fruit Hill since 2002, and Susan or Richard are always available if help or advice is needed. They can arrange for a reliable babysitter if required.</p>
    <p>Washing machine and tumble dryer are housed in a separate laundry building. An initial supply of fuel for the fires is provided in the welcome pack for each cottage.</p>
    <p>You can book Kirby’s online at: <a href="{AIRBNB_KIRBYS}">airbnb.com/h/fruithill2</a>.</p>
  </section>
  <section class="wide">
{gallery("kirbys", 8, "Kirby’s")}
  </section>''')

PAGES["contact"] = ("Contact — Fruit Hill Cottages", "Contact Fruit Hill Cottages: email, phone and directions to Fruit Hill, Campile, Co. Wexford.", f'''
  <section class="text">
    <h2>Contact</h2>
    <p><strong>Email</strong></p>
    <p>{mail()}</p>
    <p><strong>Phone</strong></p>
    <p><a href="tel:{PHONE_TEL}">(+353) 51 388-694</a></p>
    <p><a href="tel:{MOBILE_TEL}">{MOBILE_DISPLAY}</a></p>
    <p><strong>Directions</strong></p>
    <p>Our address is Fruit Hill, Campile, Ballinamona, New Ross, Co. Wexford, Y34 V128. You’ll see a post with red reflective bands opposite the entrance for Fruit Hill. Through the gateway at the end of the lane, turn to the right and drive to the house on the turning circle.</p>
  </section>''')

PAGES["book-a-stay"] = ("Book a Stay — Fruit Hill Cottages", "Book the Coach House or Kirby’s at Fruit Hill through Airbnb.", f'''
  <section class="text">
    <h2>Book a Stay</h2>
    <p>Our family has been in the hospitality business for almost 20 years. We enjoy sharing Fruit Hill and our knowledge of the area with visitors from around the world, and look forward to welcoming you for your stay.</p>
    <p>To check availability and make a booking, please do so through our cottages’ Airbnb pages.</p>
    <p>You can find a link to the Coach House at <a href="{AIRBNB_COACH}">www.airbnb.com/h/fruithill1</a>, and Kirby’s at <a href="{AIRBNB_KIRBYS}">www.airbnb.com/h/fruithill2</a>.</p>
    <p class="book-buttons"><a class="btn" href="{AIRBNB_COACH}">Book the Coach House</a> <a class="btn" href="{AIRBNB_KIRBYS}">Book Kirby’s</a></p>
    <p>For any queries, don’t hesitate to email Susan at {mail()}, or phone <a href="tel:{PHONE_TEL}">(+353) 51 388694</a>.</p>
  </section>''')

NOT_FOUND = '''
  <section class="text center">
    <h2>Page not found</h2>
    <p>Sorry, that page doesn’t exist. <a href="/">Go to the home page</a>.</p>
  </section>'''


TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{canonical}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://www.fruithillcottages.com/images/home-hero.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,300;0,400;0,500;1,300;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
</head>
<body>
{header}
<main id="page">
{body}
</main>
{footer}
<script src="/assets/menu.js" defer></script>
</body>
</html>
'''


def relativise(html, prefix):
    """Turn root paths into relative ones so the site works both on the custom
    domain and at a GitHub project address like user.github.io/repo/."""
    html = re.sub(r'(href|src)="/"', lambda m: f'{m.group(1)}="{prefix or "./"}"', html)
    # page links: /coach-house -> ../coach-house/
    html = re.sub(r'href="/([a-z0-9-]+)"', lambda m: f'href="{prefix}{m.group(1)}/"', html)
    # files: /assets/x, /images/x
    html = re.sub(r'(href|src)="/((?:assets|images)/[^"]+)"', lambda m: f'{m.group(1)}="{prefix}{m.group(2)}"', html)
    return html


def main():
    for slug, (title, desc, body) in PAGES.items():
        out = ROOT / ("index.html" if slug == "index" else f"{slug}/index.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        # Trailing slash: GitHub Pages redirects /coach-house to /coach-house/
        path = "/" if slug == "index" else f"/{slug}/"
        canonical = f'<link rel="canonical" href="https://www.fruithillcottages.com{path}">'
        html = TEMPLATE.format(title=title.replace("&", "&amp;"), desc=desc, canonical=canonical,
                               header=HEADER, body=body, footer=FOOTER)
        out.write_text(relativise(html, "" if slug == "index" else "../"), encoding="utf-8")
    # GitHub Pages serves 404.html at whatever URL was missing, so relative links
    # can't work here; use root paths (correct on the custom domain).
    html = TEMPLATE.format(title="Page not found — Fruit Hill Cottages", desc="", canonical="",
                           header=HEADER, body=NOT_FOUND, footer=FOOTER)
    (ROOT / "404.html").write_text(relativise(html, "/"), encoding="utf-8")
    # Old Squarespace folder URL /about -> /about-us
    (ROOT / "about").mkdir(exist_ok=True)
    (ROOT / "about/index.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>About — Fruit Hill Cottages</title>'
        '<meta http-equiv="refresh" content="0; url=../about-us/"><link rel="canonical" href="https://www.fruithillcottages.com/about-us/">'
        '<a href="../about-us/">About Us</a>\n', encoding="utf-8")
    print("Built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
