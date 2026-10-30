"""Generator website Harsha Advisory.

Sumber halaman ada di _build/pages/**/*.html. Setiap file diawali blok
<!--meta {json} --> lalu isi <main>. Jalankan dari root repo:

    python _build/build.py

Hasilnya ditulis ke folder halaman (index.html, layanan/..., dst.),
plus sitemap.xml dan llms.txt. Folder _build tidak ikut dipublikasikan
oleh GitHub Pages karena diawali garis bawah.
"""
import datetime
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "_build" / "pages"
SITE = "https://konsultankeuangan.id"
CAL = "https://calendly.com/harshadanadigital/konsultasi-gratis"
EMAIL = "tanya@konsultankeuangan.id"
INSTAGRAM = "https://www.instagram.com/harsha.advisory/"
LINKEDIN = "https://www.linkedin.com/company/harshadana"
TODAY = datetime.date.today().isoformat()

ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 016.5 3H20v15H6.5A2.5 2.5 0 004 20.5v-15z"/><path d="M4 20.5A2.5 2.5 0 016.5 18H20v3H6.5"/><path d="M8.5 7.5h7M8.5 11h5"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.3-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 010 6.8M18 14.7c2 .7 3.2 2.5 3.5 5.3"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
    "pin": '<path d="M12 21s7-6.2 7-11.5A7 7 0 005 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14l-1.5 7 5-2.5 5 2.5-1.5-7"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 19l8-8"/>',
    "doc": '<path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8l-5-5z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "spark": '<path d="M12 3l1.8 5.4L19 10l-5.2 1.6L12 17l-1.8-5.4L5 10l5.2-1.6L12 3z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M7.5 10.5V17M7.5 7.5v.01M11.5 17v-6.5M11.5 13.5c0-1.7 1.1-3 2.6-3s2.4 1 2.4 2.8V17"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


ARROW = icon("arrow", "arrow")

NAV = [
    ("layanan", "Layanan", "/layanan/"),
    ("case-studies", "Studi Kasus", "/case-studies/"),
    ("pelatihan", "Pelatihan", "/layanan/pelatihan-keuangan/"),
    ("insights", "Insights", "/insights/"),
    ("tentang", "Tentang", "/tentang/"),
    ("kontak", "Kontak", "/kontak/"),
]

SERVICES = [
    ("Jasa Pembukuan", "/layanan/jasa-pembukuan/"),
    ("Evaluasi Keuangan Bisnis", "/layanan/evaluasi-keuangan-bisnis/"),
    ("CFO Fraction", "/layanan/cfo-fraction/"),
    ("Pelatihan Keuangan", "/layanan/pelatihan-keuangan/"),
    ("Sustainable Finance", "/sustainable-finance/"),
]

ORG_ID = SITE + "/#organization"
FOUNDER_ID = SITE + "/#founder"
WEBSITE_ID = SITE + "/#website"

ORG = {
    "@type": ["ProfessionalService", "FinancialService"],
    "@id": ORG_ID,
    "name": "Harsha Advisory",
    "legalName": "PT Harsha Dana Digital",
    "alternateName": ["Harsha Dana Digital", "Harshadana"],
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo.png", "width": 1350, "height": 1350},
    "image": SITE + "/assets/og-image.jpg",
    "description": ("Harsha Advisory (PT Harsha Dana Digital) adalah perusahaan konsultan keuangan B2B "
                    "berbasis di Denpasar, Bali, yang membantu bisnis memahami angkanya sendiri melalui "
                    "jasa pembukuan, evaluasi keuangan bisnis, CFO Fraction, dan pelatihan keuangan "
                    "untuk karyawan dan manajemen."),
    "slogan": "Bisnis yang sehat adalah bisnis yang memahami angkanya.",
    "email": EMAIL,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Jl. Tukad Unda No.6",
        "addressLocality": "Denpasar Selatan",
        "addressRegion": "Bali",
        "postalCode": "80226",
        "addressCountry": "ID",
    },
    "areaServed": [{"@type": "Country", "name": "Indonesia"}],
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "08:00", "closes": "17:00",
    }],
    "founder": {"@id": FOUNDER_ID},
    "sameAs": [INSTAGRAM, LINKEDIN],
    "knowsAbout": [
        "Pembukuan dan laporan keuangan", "Evaluasi keuangan bisnis", "CFO Fraction",
        "Pengendalian internal dan pencegahan fraud", "Proyeksi arus kas",
        "Retirement planning", "Financial planning", "Literasi keuangan karyawan",
        "Treasury advisory BPR", "Surat Berharga Negara (SBN)", "Sustainable finance",
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Layanan Harsha Advisory",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": SITE + u}}
            for n, u in SERVICES
        ],
    },
}

FOUNDER = {
    "@type": "Person",
    "@id": FOUNDER_ID,
    "name": "Anak Agung Ngurah Mustakawarman",
    "honorificSuffix": "CFP®",
    "jobTitle": "Founder & CEO",
    "worksFor": {"@id": ORG_ID},
    "image": SITE + "/assets/Foto-NgurahWarman.png",
    "url": SITE + "/tentang/",
    "description": ("Praktisi keuangan dengan lebih dari 12 tahun pengalaman di industri perbankan dan "
                    "investasi, telah membantu lebih dari 200 klien financial planning di Indonesia, "
                    "Amerika Serikat, Jepang, dan Singapura."),
    "award": [
        "Top 40 Youth Economic Leadership Program, Bank Indonesia Institute",
        "Top 50 Startup Terbaik Indonesia, Kemenparekraf",
    ],
    "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "name": n, "credentialCategory": "certification"}
        for n in ["Certified Financial Planner (CFP®)", "Wakil Manajer Investasi (WMI)",
                  "Wakil Perantara Pedagang Efek (WPPE)", "Penasihat Investasi (PI)"]
    ],
    "knowsAbout": ["Financial planning", "Retirement planning", "Corporate financial advisory",
                   "Forensic accounting", "Treasury advisory", "Capital markets"],
}

WEBSITE = {
    "@type": "WebSite",
    "@id": WEBSITE_ID,
    "url": SITE + "/",
    "name": "Harsha Advisory",
    "inLanguage": "id-ID",
    "publisher": {"@id": ORG_ID},
}


# ---------------------------------------------------------------- loading

def load_pages():
    pages = []
    for f in sorted(PAGES.rglob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", raw, re.S)
        if not m:
            raise SystemExit(f"{f}: blok <!--meta--> tidak ditemukan")
        meta = json.loads(m.group(1))
        meta["body"] = raw[m.end():]
        meta["src"] = f
        pages.append(meta)
    return pages


def out_path(path):
    if path.endswith(".html"):
        return ROOT / path.lstrip("/")
    return ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"


def esc(s):
    return html.escape(s, quote=True)


def fmt_date(iso):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
             "Agustus", "September", "Oktober", "November", "Desember"]
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {bulan[d.month - 1]} {d.year}"


# ---------------------------------------------------------------- partials

def header(active):
    links = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""<a class="skip" href="#main">Langsung ke konten</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="/" class="brand" aria-label="Harsha Advisory, ke beranda">
      <img src="/assets/logo-mark.png" alt="" width="34" height="34">
      <span class="brand-name">Harsha <span>Advisory</span></span>
    </a>
    <nav class="nav" id="site-nav" aria-label="Menu utama">
      {' '.join(links)}
      <a href="{CAL}" class="btn btn-primary" target="_blank" rel="noopener">Diskusi Gratis</a>
    </nav>
    <button class="nav-toggle" aria-label="Buka menu" aria-expanded="false" aria-controls="site-nav">{icon("menu")}</button>
  </div>
</header>"""


def footer():
    svc = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in SERVICES)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <a href="/" class="brand"><img src="/assets/logo-mark.png" alt="" width="34" height="34"><span class="brand-name">Harsha <span>Advisory</span></span></a>
        <p class="footer-about">Konsultan keuangan B2B dari Bali. Kami membantu bisnis memahami angkanya sendiri: pembukuan yang rapi, evaluasi finansial berkala, strategi ke depan, dan pelatihan keuangan untuk tim.</p>
        <div class="social">
          <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram Harsha Advisory">{icon("instagram")}</a>
          <a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn Harsha Advisory">{icon("linkedin")}</a>
        </div>
      </div>
      <div>
        <h4>Layanan</h4>
        <ul>{svc}</ul>
      </div>
      <div>
        <h4>Perusahaan</h4>
        <ul>
          <li><a href="/tentang/">Tentang Kami</a></li>
          <li><a href="/case-studies/">Studi Kasus</a></li>
          <li><a href="/insights/">Insights</a></li>
          <li><a href="/#faq">FAQ</a></li>
          <li><a href="/kontak/">Kontak</a></li>
        </ul>
      </div>
      <div>
        <h4>Kontak</h4>
        <address>
          PT Harsha Dana Digital<br>
          Jl. Tukad Unda No.6, Denpasar Selatan<br>
          Bali 80226, Indonesia<br>
          <a href="mailto:{EMAIL}">{EMAIL}</a><br>
          Senin sampai Jumat, 08.00 sampai 17.00 WITA
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {datetime.date.today().year} Harsha Advisory · PT Harsha Dana Digital</span>
      <span>Bisnis yang sehat adalah bisnis yang memahami angkanya.</span>
    </div>
  </div>
</footer>
<div class="mobile-cta"><a href="{CAL}" class="btn btn-blue" target="_blank" rel="noopener">{icon("calendar")} Jadwalkan Diskusi Gratis</a></div>
<script src="/script.js" defer></script>"""


def crumbs_html(crumbs):
    items = ['<li><a href="/">Beranda</a></li>']
    for label, href in crumbs:
        items.append(f'<li><a href="{href}">{esc(label)}</a></li>' if href else f'<li aria-current="page">{esc(label)}</li>')
    return '<ol class="crumbs">' + "".join(items) + "</ol>"


def faq_html(faq):
    out = ['<div class="faq">']
    for q, a in faq:
        paras = "".join(f"<p>{p}</p>" for p in a.split("\n\n"))
        out.append(f'<details class="reveal"><summary>{q}</summary><div class="answer">{paras}</div></details>')
    out.append("</div>")
    return "\n".join(out)


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def art(cls):
    return (f'<div class="art {cls}" aria-hidden="true"><svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice">'
            '<g fill="none" stroke="rgba(255,255,255,.16)" stroke-width="1.2">'
            '<circle cx="330" cy="40" r="60"/><circle cx="330" cy="40" r="110"/><circle cx="330" cy="40" r="160"/>'
            '<path d="M0 190 C60 170 90 120 150 130 S250 90 300 100 S370 60 400 50"/></g></svg></div>')


def post_card(p):
    return f"""<article class="post reveal">
  <a href="{p['path']}" tabindex="-1" aria-hidden="true">{art(p['art'])}</a>
  <div class="body">
    <div class="post-meta"><span class="tag">{esc(p['category'])}</span><span>{p['minutes']} menit baca</span></div>
    <h3><a href="{p['path']}">{esc(p['title'])}</a></h3>
    <p>{esc(p['excerpt'])}</p>
    <a class="link-arrow" href="{p['path']}">Baca artikel</a>
  </div>
</article>"""


def post_feature(p):
    return f"""<article class="post-feature reveal">
  {art(p['art'])}
  <div class="body">
    <div class="post-meta"><span class="tag dark">{esc(p['category'])}</span><span>{p['minutes']} menit baca · {fmt_date(p['published'])}</span></div>
    <h2><a href="{p['path']}">{esc(p['title'])}</a></h2>
    <p>{esc(p['excerpt'])}</p>
    <a class="link-arrow" href="{p['path']}">Baca selengkapnya</a>
  </div>
</article>"""


# ---------------------------------------------------------------- schema

def page_schema(p, url):
    graph = [ORG, WEBSITE]
    crumbs = p.get("crumbs", [])
    page_type = p.get("pageType", "WebPage")
    webpage = {
        "@type": page_type,
        "@id": url + "#webpage",
        "url": url,
        "name": p["title"],
        "description": p["description"],
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": ORG_ID},
        "inLanguage": "id-ID",
        "dateModified": p.get("modified", p.get("lastmod", TODAY)),
    }
    if p["path"] != "/":
        items = [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": SITE + "/"}]
        for i, (label, href) in enumerate(crumbs, start=2):
            items.append({"@type": "ListItem", "position": i, "name": label, "item": SITE + (href or p["path"])})
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": items})
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
    graph.append(webpage)
    if p.get("founder"):
        graph.append(FOUNDER)
    if p.get("service"):
        s = p["service"]
        graph.append({
            "@type": "Service", "@id": url + "#service", "name": s["name"], "serviceType": s.get("type", s["name"]),
            "description": s["description"], "provider": {"@id": ORG_ID}, "url": url,
            "areaServed": {"@type": "Country", "name": "Indonesia"}, "audience": {"@type": "BusinessAudience", "name": s.get("audience", "Perusahaan dan pemilik bisnis")},
        })
    if p.get("faq"):
        graph.append({
            "@type": "FAQPage", "@id": url + "#faq",
            "mainEntity": [{"@type": "Question", "name": strip_tags(q),
                            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in p["faq"]],
        })
    if p.get("layout") == "article":
        words = len(strip_tags(p["body"]).split())
        graph.append({
            "@type": "Article", "@id": url + "#article", "headline": p["title"], "description": p["description"],
            "articleSection": p["category"], "inLanguage": "id-ID", "wordCount": words,
            "datePublished": p["published"], "dateModified": p["modified"],
            "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
            "image": SITE + "/assets/og-image.jpg", "mainEntityOfPage": {"@id": url + "#webpage"},
        })
    for extra in p.get("schema", []):
        graph.append(extra)
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- render

def head(p, url):
    title = p["title"] if p.get("rawTitle") else f'{p["title"]} | Harsha Advisory'
    robots = "noindex, follow" if p.get("noindex") else "index, follow, max-image-preview:large"
    og_type = "article" if p.get("layout") == "article" else "website"
    extra = ""
    if p.get("layout") == "article":
        extra = (f'\n  <meta property="article:published_time" content="{p["published"]}">'
                 f'\n  <meta property="article:modified_time" content="{p["modified"]}">'
                 f'\n  <meta property="article:section" content="{esc(p["category"])}">')
    gsv = '\n  <meta name="google-site-verification" content="jmkiCpikYeTn6lvK6ahbdeN8ChffgprwPAnVHjPJRmo">' if p["path"] == "/" else ""
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(p['description'])}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">
  <meta name="author" content="Harsha Advisory">
  <meta name="theme-color" content="#f7f5f0">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Harsha Advisory">
  <meta property="og:locale" content="id_ID">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(p['description'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">{extra}{gsv}
  <link rel="icon" type="image/png" sizes="64x64" href="/assets/favicon-64.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="alternate" type="text/plain" title="llms.txt" href="/llms.txt">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <script type="application/ld+json">
{page_schema(p, url)}
  </script>
</head>"""


def article_main(p, articles):
    others = [a for a in articles if a["path"] != p["path"]][:3]
    return f"""<section class="article-head">
  <div class="wrap wrap-narrow">
    {crumbs_html(p['crumbs'])}
    <span class="tag">{esc(p['category'])}</span>
    <h1>{esc(p['title'])}</h1>
    <div class="byline">
      <span class="who"><img src="/assets/logo-mark.png" alt="" width="36" height="36">Tim Harsha Advisory</span>
      <span>Diterbitkan <time datetime="{p['published']}">{fmt_date(p['published'])}</time></span>
      <span>Diperbarui <time datetime="{p['modified']}">{fmt_date(p['modified'])}</time></span>
      <span>{p['minutes']} menit baca</span>
    </div>
  </div>
</section>
<article class="article">
  <div class="wrap">
{p['body']}
    <aside class="article-cta">
      <h2>Menghadapi tantangan serupa di perusahaan Anda?</h2>
      <p>Setiap perusahaan punya dinamika keuangan yang unik. Kami bantu menemukan akar masalahnya, merancang solusi yang terukur, dan mendampingi implementasinya.</p>
      <div class="hero-cta"><a href="{CAL}" class="btn btn-light" target="_blank" rel="noopener">{icon("calendar")} Jadwalkan Diskusi 30 Menit</a><a href="mailto:{EMAIL}" class="btn btn-outline-light">Kirim Email</a></div>
    </aside>
  </div>
</article>
<section class="section bg-paper">
  <div class="wrap">
    <div class="split-head"><div><span class="eyebrow">Baca juga</span><h2>Insight lainnya</h2></div><div><a class="link-arrow" href="/insights/">Semua artikel</a></div></div>
    <div class="posts">{''.join(post_card(o) for o in others)}</div>
  </div>
</section>"""


def render(p, articles):
    url = SITE + (p["path"] if p["path"] != "/404.html" else "/404.html")
    if p.get("layout") == "article":
        main = article_main(p, articles)
    else:
        main = p["body"]
        featured = next(a for a in articles if a.get("featured"))
        tokens = {
            "{{cal}}": CAL,
            "{{email}}": EMAIL,
            "{{instagram}}": INSTAGRAM,
            "{{linkedin}}": LINKEDIN,
            "{{crumbs}}": crumbs_html(p.get("crumbs", [])),
            "{{faq}}": faq_html(p.get("faq", [])),
            "{{post_feature}}": post_feature(featured),
            "{{posts_rest}}": "".join(post_card(a) for a in articles if a is not featured),
            "{{posts_latest}}": "".join(post_card(a) for a in articles[:3]),
            "{{arrow}}": ARROW,
        }
        for k, v in tokens.items():
            main = main.replace(k, v)
        main = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), main)
    left = re.findall(r"\{\{[^}]+\}\}", main)
    if left:
        raise SystemExit(f"{p['src']}: token tidak dikenal {left}")
    return f"""{head(p, url)}
<body>
{header(p.get('nav'))}
<main id="main">
{main}
</main>
{footer()}
</body>
</html>
"""


def write_sitemap(pages):
    rows = []
    for p in sorted(pages, key=lambda x: x["path"]):
        if p.get("noindex"):
            continue
        lastmod = p.get("modified", p.get("lastmod", TODAY))
        rows.append(f"  <url><loc>{SITE}{p['path']}</loc><lastmod>{lastmod}</lastmod></url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8", newline="\n")


def write_llms(pages, articles):
    def line(p):
        return f"- [{p['title']}]({SITE}{p['path']}): {p['description']}"
    main_pages = [p for p in pages if not p.get("noindex") and p.get("layout") != "article"]
    order = {path: i for i, path in enumerate(["/", "/layanan/", "/layanan/jasa-pembukuan/",
             "/layanan/evaluasi-keuangan-bisnis/", "/layanan/cfo-fraction/", "/layanan/pelatihan-keuangan/",
             "/sustainable-finance/", "/case-studies/", "/tentang/", "/kontak/", "/insights/"])}
    main_pages.sort(key=lambda p: order.get(p["path"], 99))
    text = f"""# Harsha Advisory

> Harsha Advisory (PT Harsha Dana Digital) adalah perusahaan konsultan keuangan B2B yang berbasis di Denpasar, Bali, Indonesia. Kami membantu perusahaan memahami angkanya sendiri melalui jasa pembukuan, evaluasi keuangan bisnis dengan pendekatan kuantitatif, CFO Fraction (CFO paruh waktu), dan pelatihan keuangan untuk karyawan dan manajemen.

Fakta utama:
- Nama: Harsha Advisory. Badan usaha: PT Harsha Dana Digital.
- Founder & CEO: Anak Agung Ngurah Mustakawarman, CFP®. Lebih dari 12 tahun pengalaman perbankan dan 10 tahun pengalaman investasi; lebih dari 200 klien financial planning di 4 negara (Indonesia, Amerika Serikat, Jepang, Singapura). Sertifikasi: CFP®, WMI, WPPE, PI.
- Penghargaan founder: Top 40 Youth Economic Leadership Program (Bank Indonesia Institute); Top 50 Startup Terbaik Indonesia (Kemenparekraf).
- Alamat: Jl. Tukad Unda No.6, Denpasar Selatan, Bali 80226. Melayani klien di seluruh Indonesia.
- Kontak: {EMAIL}. Diskusi awal 30 menit gratis: {CAL}
- Klien dan mitra pelatihan antara lain: British Petroleum, Petronas, Kangean Energy, Eni Indonesia, Donggi Senoro LNG, Bank Indonesia, Komdigi, GoPay, BPR Lestari, Joger Bali.
- Biaya: disesuaikan dengan ruang lingkup, ditawarkan setelah diskusi awal. Tidak ada paket harga tetap.
- Harsha Advisory tidak menyediakan audit statutory, layanan hukum, perpajakan kompleks lintas yurisdiksi, atau manajemen investasi diskresioner; untuk area tersebut kami bekerja dengan mitra spesialis.

## Halaman utama
{chr(10).join(line(p) for p in main_pages)}

## Artikel
{chr(10).join(line(a) for a in articles)}
"""
    (ROOT / "llms.txt").write_text(text, encoding="utf-8", newline="\n")


def main():
    pages = load_pages()
    articles = [p for p in pages if p.get("layout") == "article"]
    articles.sort(key=lambda a: a.get("order", 99))
    for p in pages:
        if p.get("layout") == "article":
            p.setdefault("crumbs", [["Insights", "/insights/"], [p["title"], None]])
    for p in pages:
        target = out_path(p["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(p, articles), encoding="utf-8", newline="\n")
        print("ok", p["path"])
    write_sitemap(pages)
    write_llms(pages, articles)
    print(f"{len(pages)} halaman, sitemap.xml, llms.txt")


if __name__ == "__main__":
    main()
