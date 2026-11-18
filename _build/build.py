"""Generator website Harsha Advisory.

Sumber halaman ada di _build/pages/**/*.html. Setiap file diawali blok
<!--meta {json} --> lalu isi <main>. Jalankan dari root repo:

    python _build/build.py

Hasilnya ditulis ke folder halaman (index.html, layanan/..., dst.),
plus sitemap.xml dan llms.txt. Folder _build tidak ikut dipublikasikan
oleh GitHub Pages karena diawali garis bawah.
"""
import datetime
import hashlib
import html
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "_build" / "pages"
SITE = "https://harshaadvisory.com"
EMAIL = "info@harshaadvisory.com"
WA_NUMBER = "6289673144112"
WA_DISPLAY = "+62 896-7314-4112"
WA = f"https://wa.me/{WA_NUMBER}?text=Halo%20Harsha%20Advisory%2C%20saya%20ingin%20konsultasi%20tentang%20keuangan%20bisnis%20saya."
INSTAGRAM = "https://www.instagram.com/harsha.advisory/"
LINKEDIN = "https://www.linkedin.com/company/harshadana"
THREADS = "https://www.threads.com/@harsha.advisory"
LYNK = "https://lynk.id/harshadana"
TODAY = datetime.date.today().isoformat()
PRICE_FROM = 5000000
PRICE_TEXT = "Rp5 juta"

# ---------------------------------------------------------------- bahasa
# Versi Inggris: sumber di _build/pages_en/ (struktur sama, "path" tetap path
# Indonesia) dan _build/products_en.json. Semua halaman Inggris tayang di /en/.
PAGES_EN = ROOT / "_build" / "pages_en"
CUR = {"lang": "id"}  # bahasa halaman yang sedang dirender

WA_TEXT = {
    "id": "Halo%20Harsha%20Advisory%2C%20saya%20ingin%20konsultasi%20tentang%20keuangan%20bisnis%20saya.",
    "en": "Hello%20Harsha%20Advisory%2C%20I%20would%20like%20to%20discuss%20my%20company%27s%20finances.",
}

STR = {
    "id": {
        "price": f"{PRICE_TEXT} per bulan", "price_range": f"Mulai dari {PRICE_TEXT}",
        "skip": "Langsung ke konten", "home_aria": "Harsha Advisory, ke beranda", "menu": "Menu utama",
        "open_menu": "Buka menu", "cta": "Jadwalkan Diskusi Awal", "home": "Beranda",
        "f_about": "Harsha Advisory adalah firma konsultasi keuangan bisnis yang membantu pemilik usaha dan manajemen mengambil keputusan melalui analisis keuangan dan pendampingan strategis.",
        "f_services": "Layanan", "f_company": "Perusahaan", "f_contact": "Kontak",
        "f_links": [("Tentang Kami", "/tentang/"), ("Studi Kasus", "/case-studies/"), ("Insights", "/insights/"),
                    ("Kamus Keuangan", "/kamus-keuangan/"), ("Produk Digital", "/katalog/"), ("FAQ", "/#faq"), ("Kontak", "/kontak/")],
        "hours": "Senin sampai Jumat, 08.00 sampai 17.00 WITA",
        "slogan": "Bisnis yang sehat adalah bisnis yang memahami angkanya",
        "wa_chat": "Chat WhatsApp", "wa_aria": "Chat WhatsApp Harsha Advisory", "wa_contact": "Hubungi via WhatsApp",
        "min_read": "menit baca", "read_article": "Baca artikel", "read_more": "Baca selengkapnya",
        "team": "Tim Harsha Advisory", "published": "Diterbitkan", "updated": "Diperbarui",
        "art_cta_h": "Keputusan Bisnis yang Tepat Dimulai dari Analisis yang Tepat",
        "art_cta_p": "Menghadapi persoalan serupa di perusahaan Anda? Jadwalkan konsultasi awal 30 menit secara gratis via WhatsApp.",
        "read_also": "Baca juga", "more_insights": "Insight lainnya", "all_articles": "Semua artikel",
        "buy_schedule": "Pilih jadwal &amp; pesan", "buy_now": "Beli sekarang",
        "note_schedule": "Anda akan memilih jadwal dan membayar di Lynk.id.",
        "note_buy": "Pembayaran diproses dengan aman oleh Lynk.id.", "ask_first": "Tanya dulu",
        "price_word": "Harga", "other_choices": "Pilihan lainnya", "all_products": "Semua produk digital",
        "see_detail": "Lihat detail", "digital_products": "Produk Digital",
        "img_of": "gambar {i} dari {n}", "see_img": "Lihat gambar {i} dari {n}", "gallery": "Galeri gambar {name}",
        "prev_img": "Gambar sebelumnya", "next_img": "Gambar berikutnya",
        "lang_name": "Bahasa Indonesia", "switch_label": "Ganti bahasa",
        "months": ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
                   "September", "Oktober", "November", "Desember"],
    },
    "en": {
        "price": "IDR 5 million per month", "price_range": "From IDR 5 million",
        "skip": "Skip to content", "home_aria": "Harsha Advisory, home", "menu": "Main menu",
        "open_menu": "Open menu", "cta": "Schedule a Discussion", "home": "Home",
        "f_about": "Harsha Advisory is a business financial advisory firm helping owners and management make informed decisions through financial analysis and strategic guidance.",
        "f_services": "Services", "f_company": "Company", "f_contact": "Contact",
        "f_links": [("About Us", "/tentang/"), ("Case Studies", "/case-studies/"), ("Insights", "/insights/"),
                    ("Finance Glossary", "/kamus-keuangan/"), ("Digital Products", "/katalog/"), ("FAQ", "/#faq"), ("Contact", "/kontak/")],
        "hours": "Monday to Friday, 08:00 to 17:00 WITA (UTC+8)",
        "slogan": "A healthy business is one that understands its numbers",
        "wa_chat": "Chat on WhatsApp", "wa_aria": "Chat with Harsha Advisory on WhatsApp", "wa_contact": "Contact via WhatsApp",
        "min_read": "min read", "read_article": "Read article", "read_more": "Read more",
        "team": "Harsha Advisory Team", "published": "Published", "updated": "Updated",
        "art_cta_h": "Better Business Decisions Start with Better Financial Analysis",
        "art_cta_p": "Facing a similar issue in your company? Schedule a free 30-minute initial consultation on WhatsApp.",
        "read_also": "Read also", "more_insights": "More insights", "all_articles": "All articles",
        "buy_schedule": "Choose a schedule &amp; book", "buy_now": "Buy now",
        "note_schedule": "You will choose a schedule and pay on Lynk.id.",
        "note_buy": "Payment is processed securely by Lynk.id.", "ask_first": "Ask first",
        "price_word": "Price", "other_choices": "Other options", "all_products": "All digital products",
        "see_detail": "View details", "digital_products": "Digital Products",
        "img_of": "image {i} of {n}", "see_img": "View image {i} of {n}", "gallery": "{name} image gallery",
        "prev_img": "Previous image", "next_img": "Next image",
        "lang_name": "English", "switch_label": "Change language",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August",
                   "September", "October", "November", "December"],
    },
}


def t(key):
    return STR[CUR["lang"]][key]


def wa_link():
    return f"https://wa.me/{WA_NUMBER}?text={WA_TEXT[CUR['lang']]}"


def is_internal_page(path):
    """Path halaman situs (bukan aset atau file) yang punya versi per bahasa."""
    base = path.split("#")[0].split("?")[0]
    return (path.startswith("/") and not path.startswith("//") and not path.startswith("/en/")
            and not path.startswith("/assets/") and not re.search(r"\.\w+$", base))


def lp(path, lang=None):
    """Path untuk bahasa tertentu: '/x/' -> '/en/x/' pada versi Inggris."""
    lang = lang or CUR["lang"]
    if lang == "en" and is_internal_page(path):
        return "/en" + path
    return path


def localize_links(markup):
    if CUR["lang"] != "en":
        return markup
    return re.sub(r'href="(/[^"]*)"', lambda m: f'href="{lp(m.group(1))}"', markup)

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
    "threads": '<path transform="translate(1.9 1.9) scale(.84)" fill="currentColor" stroke="none" d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 013.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.79-1.548 7.158-1.85 1.81-4.094 2.628-7.277 2.65zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 00-2.215-.221z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "whatsapp": '<path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1112 20.5a8.4 8.4 0 01-4.1-1.1L3.5 20.5z"/><path d="M9 8.5c0 3.3 3.2 6.5 6.5 6.5l1-1.6-2-1-1 .9c-1-.4-2.3-1.7-2.7-2.7l.9-1-1-2L9 8.5z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


ARROW = icon("arrow", "arrow")

CFO_URL = "/layanan/fractional-cfo/"

# Menu utama mengikuti keputusan audit (PDF halaman 5). Produk Digital dan Kontak
# sengaja tidak masuk navbar: Produk Digital hanya di footer, kontak lewat tombol.
NAV = [
    ("home", "Beranda", "/"),
    ("fractional-cfo", "Fractional CFO", CFO_URL),
    ("pelatihan", "Corporate Financial Training", "/layanan/pelatihan-keuangan/"),
    ("case-studies", "Studi Kasus", "/case-studies/"),
    ("insights", "Insights", "/insights/"),
    ("tentang", "Tentang", "/tentang/"),
]

NAV_EN = {"home": "Home", "fractional-cfo": "Fractional CFO", "pelatihan": "Corporate Financial Training",
          "case-studies": "Case Studies", "insights": "Insights", "tentang": "About"}

CATALOG = [
    ("template", "Template"),
    ("konsultasi", "Konsultasi"),
    ("bundle", "Bundle"),
]
CATALOG_EN = {"template": "Templates", "konsultasi": "Consultation", "bundle": "Bundles"}
SERVICES = [
    ("Fractional CFO", CFO_URL),
    ("Business Financial Evaluation", "/layanan/evaluasi-keuangan-bisnis/"),
    ("Pelatihan Keuangan", "/layanan/pelatihan-keuangan/"),
    ("Sustainable Finance", "/sustainable-finance/"),
]
SERVICES_EN = {"Pelatihan Keuangan": "Financial Training"}


def catalog_label(key):
    return CATALOG_EN[key] if CUR["lang"] == "en" else dict(CATALOG)[key]


def services():
    if CUR["lang"] == "en":
        return [(SERVICES_EN.get(n, n), lp(u)) for n, u in SERVICES]
    return SERVICES

# URL lama yang dialihkan. GitHub Pages tidak punya redirect server, jadi
# dibuat halaman pengalihan (meta refresh + canonical ke tujuan baru).
REDIRECTS = {
    "/layanan/cfo-fraction/": CFO_URL,
    "/layanan/": "/",
    "/layanan/jasa-pembukuan/": "/",
    "/insights/cfo-fraction-vs-cfo-full-time/": "/insights/fractional-cfo-vs-cfo-full-time/",
    "/insights/jasa-pembukuan-vs-software-akuntansi/": "/insights/",
}

# Kartu solusi di beranda (token {{service_cards}}): Fractional CFO sebagai kartu utama.
SERVICE_CARDS = """<article class="service service-featured reveal">
        <div>
          <div class="service-top"><span class="service-icon">{{icon:compass}}</span><span class="tag">Layanan unggulan</span></div>
          <h3>Fractional CFO</h3>
          <p>Kami membantu manajemen membaca kinerja, menjaga fokus pada arus kas, dan menilai pilihan keuangan dengan perspektif yang lebih menyeluruh.</p>
          <a class="btn btn-primary" href="/layanan/fractional-cfo/">Kenali Fractional CFO {{arrow}}</a>
        </div>
        <ul><li>Profitabilitas dan kinerja usaha</li><li>Arus kas dan kebutuhan modal kerja</li><li>Skenario dan konsekuensi keputusan keuangan</li><li>Pembahasan rutin bersama manajemen</li></ul>
      </article>
      <article class="service reveal">
        <div class="service-top"><span class="service-icon">{{icon:chart}}</span><span class="service-letter">BFE</span></div>
        <h3>Business Financial Evaluation (BFE)</h3>
        <p>Kenali posisi keuangan perusahaan dan area yang paling perlu menjadi perhatian sebelum menentukan langkah berikutnya.</p>
        <a class="link-arrow" href="/layanan/evaluasi-keuangan-bisnis/">Pelajari BFE</a>
      </article>
      <article class="service reveal d1">
        <div class="service-top"><span class="service-icon">{{icon:users}}</span><span class="tag">Corporate Financial Training</span></div>
        <h3>Pelatihan Keuangan</h3>
        <p>Pembelajaran keuangan untuk manajemen dan peserta perusahaan, disusun sesuai konteks dan tujuan program.</p>
        <a class="link-arrow" href="/layanan/pelatihan-keuangan/">Diskusikan Program Pelatihan</a>
      </article>"""

SERVICE_CARDS_EN = """<article class="service service-featured reveal">
        <div>
          <div class="service-top"><span class="service-icon">{{icon:compass}}</span><span class="tag">Flagship service</span></div>
          <h3>Fractional CFO</h3>
          <p>We help management read performance, stay focused on cash flow, and weigh financial options with a broader perspective.</p>
          <a class="btn btn-primary" href="/layanan/fractional-cfo/">Discover Fractional CFO {{arrow}}</a>
        </div>
        <ul><li>Profitability and business performance</li><li>Cash flow and working capital needs</li><li>Scenarios and consequences of financial decisions</li><li>Regular discussions with management</li></ul>
      </article>
      <article class="service reveal">
        <div class="service-top"><span class="service-icon">{{icon:chart}}</span><span class="service-letter">BFE</span></div>
        <h3>Business Financial Evaluation (BFE)</h3>
        <p>Understand your company's financial position and the areas that need the most attention before deciding on the next step.</p>
        <a class="link-arrow" href="/layanan/evaluasi-keuangan-bisnis/">Explore BFE</a>
      </article>
      <article class="service reveal d1">
        <div class="service-top"><span class="service-icon">{{icon:users}}</span><span class="tag">Corporate Financial Training</span></div>
        <h3>Financial Training</h3>
        <p>Financial learning for management and company participants, designed around the context and goals of each program.</p>
        <a class="link-arrow" href="/layanan/pelatihan-keuangan/">Discuss a Training Program</a>
      </article>"""

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
    "description": ("Harsha Advisory (PT Harsha Dana Digital) adalah firma konsultasi keuangan bisnis yang "
                    "membantu pemilik usaha dan manajemen di seluruh Indonesia mengambil keputusan melalui "
                    "analisis keuangan dan pendampingan strategis: Fractional CFO, Business Financial "
                    "Evaluation, dan Corporate Financial Training."),
    "slogan": "Bisnis yang sehat adalah bisnis yang memahami angkanya",
    "email": EMAIL,
    "telephone": "+62-896-7314-4112",
    "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": "+62-896-7314-4112", "email": EMAIL, "areaServed": "ID", "availableLanguage": ["Indonesian", "English"]}],
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
    "sameAs": [INSTAGRAM, THREADS, LINKEDIN],
    "knowsAbout": [
        "Fractional CFO", "Business Financial Evaluation", "Profitabilitas dan arus kas perusahaan",
        "Pengendalian internal dan pencegahan fraud", "Proyeksi arus kas",
        "Retirement planning", "Financial planning", "Literasi keuangan karyawan",
        "Treasury advisory BPR", "Surat Berharga Negara (SBN)", "Sustainable finance",
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Layanan Harsha Advisory",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[0], "url": SITE + s[1]},
             **({"priceSpecification": {"@type": "PriceSpecification", "minPrice": PRICE_FROM, "priceCurrency": "IDR"}}
                if s[1] == CFO_URL else {})}
            for s in SERVICES
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

ORG_EN_DESC = ("Harsha Advisory (PT Harsha Dana Digital) is a business financial advisory firm helping owners "
               "and management across Indonesia make informed decisions through financial analysis and strategic "
               "guidance: Fractional CFO, Business Financial Evaluation, and Corporate Financial Training.")
FOUNDER_EN_DESC = ("Finance practitioner with more than 12 years of experience in banking and investment, who has "
                   "advised more than 200 financial planning clients in Indonesia, the United States, Japan, and Singapore.")


def org():
    if CUR["lang"] == "id":
        return ORG
    o = dict(ORG, description=ORG_EN_DESC, slogan=STR["en"]["slogan"])
    o["hasOfferCatalog"] = dict(ORG["hasOfferCatalog"], name="Harsha Advisory services", itemListElement=[
        dict(item, itemOffered={"@type": "Service", "name": n, "url": SITE + u})
        for item, (n, u) in zip(ORG["hasOfferCatalog"]["itemListElement"], services())])
    return o


def founder():
    return FOUNDER if CUR["lang"] == "id" else dict(FOUNDER, description=FOUNDER_EN_DESC, url=SITE + "/en/tentang/")


WEBSITE = {
    "@type": "WebSite",
    "@id": WEBSITE_ID,
    "url": SITE + "/",
    "name": "Harsha Advisory",
    "inLanguage": "id-ID",
    "publisher": {"@id": ORG_ID},
}


# ---------------------------------------------------------------- loading

def load_products(lang="id"):
    # Produk dengan "draft": true belum tayang (misalnya link Lynk belum ada).
    items = json.loads((ROOT / "_build" / "products.json").read_text(encoding="utf-8"))
    if lang == "en":
        f = ROOT / "_build" / "products_en.json"
        tr = {p["id"]: p for p in json.loads(f.read_text(encoding="utf-8"))} if f.is_file() else {}
        items = [dict(p, **{k: tr[p["id"]][k] for k in ("name", "lead", "body")}, lang="en")
                 for p in items if p["id"] in tr]
    return [p for p in items if not p.get("draft")]


def load_pages(folder=PAGES, lang="id"):
    pages = []
    if not folder.is_dir():
        return pages
    for f in sorted(folder.rglob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", raw, re.S)
        if not m:
            raise SystemExit(f"{f}: blok <!--meta--> tidak ditemukan")
        meta = json.loads(m.group(1))
        meta["body"] = raw[m.end():]
        meta["src"] = f
        meta["lang"] = lang
        meta["id_path"] = meta["path"]
        if lang == "en":
            meta["path"] = "/en" + meta["path"]
            meta["crumbs"] = [[label, lp(href, "en") if href else None] for label, href in meta.get("crumbs", [])]
        pages.append(meta)
    return pages


def out_path(path):
    if path.endswith(".html"):
        return ROOT / path.lstrip("/")
    return ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"


def esc(s):
    return html.escape(s, quote=True)


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {t('months')[d.month - 1]} {d.year}"


# ---------------------------------------------------------------- partials

def lang_switch(alt):
    """Tombol ID | EN. `alt` = path halaman padanan di bahasa lain (atau beranda)."""
    cur = CUR["lang"]
    other = "en" if cur == "id" else "id"
    here = '<span aria-current="true">' + cur.upper() + "</span>"
    there = (f'<a href="{alt}" hreflang="{other}" lang="{other}" '
             f'title="{STR[other]["lang_name"]}">{other.upper()}</a>')
    parts = [here, there] if cur == "id" else [there, here]
    return f'<div class="lang-switch" role="group" aria-label="{t("switch_label")}">{parts[0]}{parts[1]}</div>'


def header(active, alt):
    links = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        label = NAV_EN.get(key, label) if CUR["lang"] == "en" else label
        links.append(f'<a href="{lp(href)}"{cur}>{label}</a>')
    return f"""<a class="skip" href="#main">{t("skip")}</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="{lp("/")}" class="brand" aria-label="{t("home_aria")}">
      <img src="/assets/logo-mark.png" alt="" width="34" height="34">
      <span class="brand-name">Harsha <span>Advisory</span></span>
    </a>
    <nav class="nav" id="site-nav" aria-label="{t("menu")}">
      {' '.join(links)}
      <a href="{wa_link()}" class="btn btn-primary" target="_blank" rel="noopener">{t("cta")}</a>
    </nav>
    {lang_switch(alt)}
    <button class="nav-toggle" aria-label="{t("open_menu")}" aria-expanded="false" aria-controls="site-nav">{icon("menu")}</button>
  </div>
</header>"""


def social_links(cls="social"):
    links = [("Instagram", INSTAGRAM, "instagram"), ("Threads", THREADS, "threads"), ("LinkedIn", LINKEDIN, "linkedin")]
    a = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n} Harsha Advisory" title="{n}">{icon(i)}</a>' for n, u, i in links)
    return f'<div class="{cls}">{a}</div>'


def footer():
    svc = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in services())
    company = "".join(f'<li><a href="{lp(u)}">{n}</a></li>' for n, u in t("f_links"))
    wa = wa_link()
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <a href="{lp("/")}" class="brand"><img src="/assets/logo-mark.png" alt="" width="34" height="34"><span class="brand-name">Harsha <span>Advisory</span></span></a>
        <p class="footer-about">{t("f_about")}</p>
        {social_links()}
      </div>
      <div>
        <h4>{t("f_services")}</h4>
        <ul>{svc}</ul>
      </div>
      <div>
        <h4>{t("f_company")}</h4>
        <ul>{company}</ul>
      </div>
      <div>
        <h4>{t("f_contact")}</h4>
        <address>
          PT Harsha Dana Digital<br>
          Jl. Tukad Unda No.6, Denpasar Selatan<br>
          Bali 80226, Indonesia<br>
          <a href="mailto:{EMAIL}">{EMAIL}</a><br>
          <a href="{wa}" target="_blank" rel="noopener">WhatsApp {WA_DISPLAY}</a><br>
          {t("hours")}
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {datetime.date.today().year} Harsha Advisory · PT Harsha Dana Digital</span>
      <span>{t("slogan")}</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa}" target="_blank" rel="noopener" aria-label="{t("wa_aria")}">{icon("whatsapp")}<span>{t("wa_chat")}</span></a>
<div class="mobile-cta"><a href="{wa}" class="btn btn-wa" target="_blank" rel="noopener">{icon("whatsapp")} {t("cta")}</a></div>
<script src="{versioned("/script.js")}" defer></script>"""


def crumbs_html(crumbs):
    items = [f'<li><a href="{lp("/")}">{t("home")}</a></li>']
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


def glossary_html(terms):
    out = ['<dl class="glossary">']
    for name, slug, definition, link in terms:
        more = f' <a class="link-arrow" href="{link}">{"Learn more" if CUR["lang"] == "en" else "Selengkapnya"}</a>' if link else ""
        out.append(f'<div id="{slug}" class="reveal"><dt>{esc(name)}</dt><dd>{definition}{more}</dd></div>')
    out.append("</dl>")
    return "\n".join(out)


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def article_words(p):
    """Jumlah kata isi artikel (termasuk FAQ), tanpa daftar referensi dan kotak CTA."""
    body = p["body"].replace("{{faq}}", faq_html(p.get("faq", [])))
    body = re.sub(r'<div class="refs">.*?</div>', "", body, flags=re.S)
    return len(strip_tags(body).split())


def art(cls):
    return (f'<div class="art {cls}" aria-hidden="true"><svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice">'
            '<g fill="none" stroke="rgba(255,255,255,.16)" stroke-width="1.2">'
            '<circle cx="330" cy="40" r="60"/><circle cx="330" cy="40" r="110"/><circle cx="330" cy="40" r="160"/>'
            '<path d="M0 190 C60 170 90 120 150 130 S250 90 300 100 S370 60 400 50"/></g></svg></div>')


def thumb(p, loading="lazy"):
    if not p.get("image"):
        return art(p["art"])
    return (f'<span class="thumb"><img src="{p["image"]}" alt="" width="{p["image_w"]}" '
            f'height="{p["image_h"]}" loading="{loading}"></span>')


def post_card(p):
    return f"""<article class="post reveal">
  <a href="{p['path']}" tabindex="-1" aria-hidden="true">{thumb(p)}</a>
  <div class="body">
    <div class="post-meta"><span class="tag">{esc(p['category'])}</span><span>{p['minutes']} {t("min_read")}</span></div>
    <h3><a href="{p['path']}">{esc(p['title'])}</a></h3>
    <p>{esc(p['excerpt'])}</p>
    <a class="link-arrow" href="{p['path']}">{t("read_article")}</a>
  </div>
</article>"""


def post_feature(p):
    visual = (f'<a href="{p["path"]}" tabindex="-1" aria-hidden="true">{thumb(p, "eager")}</a>'
              if p.get("image") else art(p["art"]))
    return f"""<article class="post-feature reveal">
  {visual}
  <div class="body">
    <div class="post-meta"><span class="tag dark">{esc(p['category'])}</span><span>{p['minutes']} {t("min_read")} · {fmt_date(p['published'])}</span></div>
    <h2><a href="{p['path']}">{esc(p['title'])}</a></h2>
    <p>{esc(p['excerpt'])}</p>
    <a class="link-arrow" href="{p['path']}">{t("read_more")}</a>
  </div>
</article>"""


def rupiah(n):
    if CUR["lang"] == "en":
        return f"IDR {n:,}"
    return "Rp " + f"{n:,}".replace(",", ".")


def product_url(p):
    return lp(f"/katalog/{p['slug']}/")


def versioned(path):
    """Tambahkan ?v=<hash isi file> agar browser mengunduh ulang saat gambar diganti dengan nama yang sama."""
    f = ROOT / path.lstrip("/")
    return f"{path}?v={hashlib.md5(f.read_bytes()).hexdigest()[:8]}" if f.is_file() else path


def product_image(p):
    return versioned(p.get("image", f"/assets/katalog/{p['slug']}.webp"))


def price_html(p):
    strike = f' <s>{rupiah(p["normal_price"])}</s>' if p.get("normal_price") else ""
    return f'<span class="price"><b>{rupiah(p["price"])}</b>{strike}</span>'


def product_gallery(p):
    """Gambar utama + gambar tambahan (kunci "gallery") sebagai slider dengan thumbnail."""
    imgs = [product_image(p)] + [versioned(g) for g in p.get("gallery", [])]
    name = esc(p["name"])
    w, h = p["image_w"], p["image_h"]
    if len(imgs) == 1:
        return f'<img src="{imgs[0]}" alt="{name}" width="{w}" height="{h}">'
    n = len(imgs)
    slides = "".join(
        f'<img src="{src}" alt="{name}, {t("img_of").format(i=i, n=n)}" width="{w}" height="{h}" loading="{"eager" if i == 1 else "lazy"}">'
        for i, src in enumerate(imgs, start=1))
    thumbs = ""
    for i, src in enumerate(imgs, start=1):
        cur = ' aria-current="true"' if i == 1 else ""
        thumbs += (f'<button type="button" aria-label="{t("see_img").format(i=i, n=n)}"{cur}>'
                   f'<img src="{src}" alt="" width="{w}" height="{h}" loading="lazy"></button>')
    return f"""<div class="gallery" data-gallery>
        <div class="gallery-main">
          <div class="gallery-track" tabindex="0" role="region" aria-label="{t("gallery").format(name=name)}">{slides}</div>
          <button type="button" class="gallery-nav prev" aria-label="{t("prev_img")}">{icon("arrow")}</button>
          <button type="button" class="gallery-nav next" aria-label="{t("next_img")}">{icon("arrow")}</button>
        </div>
        <div class="gallery-thumbs">{thumbs}</div>
      </div>"""


def product_card(p):
    return f"""<article class="product reveal">
  <a href="{product_url(p)}" tabindex="-1" aria-hidden="true"><img src="{product_image(p)}" alt="" width="{p['image_w']}" height="{p['image_h']}" loading="lazy"></a>
  <div class="body">
    <h3><a href="{product_url(p)}">{esc(p['name'])}</a></h3>
    {price_html(p)}
    <a class="link-arrow" href="{product_url(p)}">{t("see_detail")}</a>
  </div>
</article>"""


def product_pages(products):
    """Halaman produk untuk bahasa yang sedang aktif (CUR)."""
    pages = []
    catalog = lp("/katalog/")
    for p in products:
        label = catalog_label(p["category"])
        buy = f"{LYNK}/{p['id']}" if p["needs_schedule"] else f"{LYNK}/{p['id']}/checkout"
        verb = t("buy_schedule") if p["needs_schedule"] else t("buy_now")
        note = t("note_schedule") if p["needs_schedule"] else t("note_buy")
        others = [o for o in products if o["category"] == p["category"] and o is not p][:3]
        crumbs = [[t("digital_products"), catalog], [p["name"], None]]
        pages.append({
            "layout": "product", "product": p, "title": p["name"], "nav": "katalog", "image": product_image(p),
            "description": f"{p['lead']} {t('price_word')} {rupiah(p['price'])}.",
            "path": product_url(p), "id_path": f"/katalog/{p['slug']}/", "lang": CUR["lang"],
            "src": "_build/products.json", "crumbs": crumbs,
            "body": f"""<section class="product-head">
  <div class="wrap">
    {crumbs_html(crumbs)}
    <div class="product-grid">
      {product_gallery(p)}
      <div>
        <span class="tag">{label}</span>
        <h1>{esc(p['name'])}</h1>
        <p class="lead">{esc(p['lead'])}</p>
        {price_html(p)}
        <div class="hero-cta"><a href="{buy}" class="btn btn-primary" target="_blank" rel="noopener">{verb} {ARROW}</a><a href="{wa_link()}" class="btn btn-ghost" target="_blank" rel="noopener">{icon("whatsapp")} {t("ask_first")}</a></div>
        <p class="price-note">{note}</p>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap wrap-narrow product-body">
{p['body']}
  </div>
</section>
<section class="section bg-paper">
  <div class="wrap">
    <div class="split-head"><div><span class="eyebrow">{label}</span><h2>{t("other_choices")}</h2></div><div><a class="link-arrow" href="{catalog}">{t("all_products")}</a></div></div>
    <div class="products">{''.join(product_card(o) for o in others)}</div>
  </div>
</section>""",
        })
    return pages


# ---------------------------------------------------------------- schema

ALT = {}  # (bahasa, path Indonesia) -> path halaman di bahasa itu
IN_LANG = {"id": "id-ID", "en": "en"}


def page_schema(p, url):
    lang = IN_LANG[CUR["lang"]]
    graph = [org(), WEBSITE]
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
        "inLanguage": lang,
        "dateModified": p.get("modified", p.get("lastmod", TODAY)),
    }
    if p["path"] != lp("/"):
        items = [{"@type": "ListItem", "position": 1, "name": t("home"), "item": SITE + lp("/")}]
        for i, (label, href) in enumerate(crumbs, start=2):
            items.append({"@type": "ListItem", "position": i, "name": label, "item": SITE + (href or p["path"])})
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": items})
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
    graph.append(webpage)
    if p.get("founder"):
        graph.append(founder())
    if p.get("service"):
        s = p["service"]
        default_aud = "Companies and business owners" if CUR["lang"] == "en" else "Perusahaan dan pemilik bisnis"
        graph.append({
            "@type": "Service", "@id": url + "#service", "name": s["name"], "serviceType": s.get("type", s["name"]),
            "description": s["description"], "provider": {"@id": ORG_ID}, "url": url,
            "areaServed": {"@type": "Country", "name": "Indonesia"}, "audience": {"@type": "BusinessAudience", "name": s.get("audience", default_aud)},
        })
    if p.get("faq"):
        graph.append({
            "@type": "FAQPage", "@id": url + "#faq",
            "mainEntity": [{"@type": "Question", "name": strip_tags(q),
                            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in p["faq"]],
        })
    if p.get("layout") == "article":
        graph.append({
            "@type": "Article", "@id": url + "#article", "headline": p["title"], "description": p["description"],
            "articleSection": p["category"], "inLanguage": lang, "wordCount": p["words"],
            "datePublished": p["published"], "dateModified": p["modified"],
            "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
            "image": SITE + p.get("image", "/assets/og-image.jpg"), "mainEntityOfPage": {"@id": url + "#webpage"},
        })
    if p.get("glossary"):
        set_name = ("Harsha Advisory Business Finance Glossary" if CUR["lang"] == "en"
                    else "Kamus Keuangan Bisnis Harsha Advisory")
        graph.append({
            "@type": "DefinedTermSet", "@id": url + "#kamus", "name": set_name,
            "inLanguage": lang, "publisher": {"@id": ORG_ID},
            "hasDefinedTerm": [{"@type": "DefinedTerm", "@id": url + "#" + slug, "name": name,
                                "description": strip_tags(d), "inDefinedTermSet": {"@id": url + "#kamus"},
                                "url": url + "#" + slug} for name, slug, d, _ in p["glossary"]],
        })
    if p.get("layout") == "product":
        item = p["product"]
        graph.append({
            "@type": "Product", "@id": url + "#product", "name": item["name"], "description": item["lead"],
            "sku": item["id"], "category": catalog_label(item["category"]),
            "image": [SITE + p["image"]] + [SITE + versioned(g) for g in item.get("gallery", [])],
            "brand": {"@id": ORG_ID}, "url": url,
            "offers": {"@type": "Offer", "price": item["price"], "priceCurrency": "IDR", "url": url,
                       "availability": "https://schema.org/InStock", "seller": {"@id": ORG_ID}},
        })
    for extra in p.get("schema", []):
        graph.append(extra)
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- render

def hreflang_links(p):
    id_url, en_url = ALT.get(("id", p["id_path"])), ALT.get(("en", p["id_path"]))
    if p.get("noindex") or not (id_url and en_url):
        return ""
    return (f'\n  <link rel="alternate" hreflang="id" href="{SITE}{id_url}">'
            f'\n  <link rel="alternate" hreflang="en" href="{SITE}{en_url}">'
            f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}{id_url}">')


def head(p, url):
    title = p["title"] if p.get("rawTitle") else f'{p["title"]} | Harsha Advisory'
    robots = "noindex, follow" if p.get("noindex") else "index, follow, max-image-preview:large"
    og_type = "article" if p.get("layout") == "article" else "website"
    extra = ""
    og_image = (f'<meta property="og:image" content="{SITE}{p["image"]}">' if p.get("image") else
                f'<meta property="og:image" content="{SITE}/assets/og-image.jpg">\n'
                '  <meta property="og:image:width" content="1200">\n'
                '  <meta property="og:image:height" content="630">')
    if p.get("image") and p.get("image_w"):
        og_image += (f'\n  <meta property="og:image:width" content="{p["image_w"]}">'
                     f'\n  <meta property="og:image:height" content="{p["image_h"]}">')
    if p.get("layout") == "article":
        extra = (f'\n  <meta name="twitter:image" content="{SITE}{p.get("image", "/assets/og-image.jpg")}">'
                 f'\n  <meta property="article:published_time" content="{p["published"]}">'
                 f'\n  <meta property="article:modified_time" content="{p["modified"]}">'
                 f'\n  <meta property="article:section" content="{esc(p["category"])}">')
    gsv = '\n  <meta name="google-site-verification" content="bTxXb9YGoeLd66LcHUGomCKRO3Yyi2kfCArZb8SdNls">' if p["path"] == "/" else ""
    locale = "en_US" if CUR["lang"] == "en" else "id_ID"
    return f"""<!DOCTYPE html>
<html lang="{CUR["lang"]}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(p['description'])}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">{hreflang_links(p)}
  <meta name="author" content="Harsha Advisory">
  <meta name="theme-color" content="#f7f5f0">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Harsha Advisory">
  <meta property="og:locale" content="{locale}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(p['description'])}">
  <meta property="og:url" content="{url}">
  {og_image}
  <meta name="twitter:card" content="summary_large_image">{extra}{gsv}
  <link rel="icon" type="image/png" sizes="64x64" href="/assets/favicon-64.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="alternate" type="text/plain" title="llms.txt" href="/llms.txt">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{versioned("/styles.css")}">
  <script type="application/ld+json">
{page_schema(p, url)}
  </script>
</head>"""


def article_main(p, articles):
    by_path = {a["path"]: a for a in articles}
    related = [by_path[lp(f"/insights/{s}/")] for s in p.get("related", []) if lp(f"/insights/{s}/") in by_path]
    rest = [a for a in articles if a["path"] != p["path"] and a not in related]
    others = (related + rest)[:3]
    figure = (f'\n<figure class="article-figure"><img src="{p["image"]}" alt="{esc(p["image_alt"])}" '
              f'width="{p["image_w"]}" height="{p["image_h"]}" loading="eager"></figure>') if p.get("image") else ""
    return f"""<section class="article-head">
  <div class="wrap wrap-narrow">
    {crumbs_html(p['crumbs'])}
    <span class="tag">{esc(p['category'])}</span>
    <h1>{esc(p['title'])}</h1>
    <div class="byline">
      <span class="who"><img src="/assets/logo-mark.png" alt="" width="36" height="36">{t("team")}</span>
      <span>{t("published")} <time datetime="{p['published']}">{fmt_date(p['published'])}</time></span>
      <span>{t("updated")} <time datetime="{p['modified']}">{fmt_date(p['modified'])}</time></span>
      <span>{p['minutes']} {t("min_read")}</span>
    </div>
  </div>
</section>{figure}
<article class="article">
  <div class="wrap">
{p['body']}
    <aside class="article-cta">
      <h2>{t("art_cta_h")}</h2>
      <p>{t("art_cta_p")}</p>
      <div class="hero-cta"><a href="{wa_link()}" class="btn btn-light" target="_blank" rel="noopener">{icon("whatsapp")} {t("cta")}</a></div>
    </aside>
  </div>
</article>
<section class="section bg-paper">
  <div class="wrap">
    <div class="split-head"><div><span class="eyebrow">{t("read_also")}</span><h2>{t("more_insights")}</h2></div><div><a class="link-arrow" href="{lp("/insights/")}">{t("all_articles")}</a></div></div>
    <div class="posts">{''.join(post_card(o) for o in others)}</div>
  </div>
</section>"""


def render(p, articles, products):
    url = SITE + p["path"]
    featured = next(a for a in articles if a.get("featured"))
    tokens = {
        "{{service_cards}}": SERVICE_CARDS_EN if CUR["lang"] == "en" else SERVICE_CARDS,  # lebih dulu: kartu berisi token lain
        "{{email}}": EMAIL,
        "{{wa}}": wa_link(),
        "{{wa_display}}": WA_DISPLAY,
        "{{instagram}}": INSTAGRAM,
        "{{linkedin}}": LINKEDIN,
        "{{social}}": social_links("social light"),
        "{{price}}": t("price"),
        "{{crumbs}}": crumbs_html(p.get("crumbs", [])),
        "{{faq}}": faq_html(p.get("faq", [])),
        "{{glossary}}": glossary_html(p.get("glossary", [])),
        "{{post_feature}}": post_feature(featured),
        "{{posts_rest}}": "".join(post_card(a) for a in articles if a is not featured),
        "{{posts_latest}}": "".join(post_card(a) for a in articles[:3]),
        "{{arrow}}": ARROW,
    }
    for key, _ in CATALOG:
        tokens[f"{{{{products:{key}}}}}"] = "".join(product_card(o) for o in products if o["category"] == key)
    body = p["body"]
    for k, v in tokens.items():
        body = body.replace(k, v)
    body = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), body)
    main = article_main(dict(p, body=body), articles) if p.get("layout") == "article" else body
    main = localize_links(main)
    p["main_html"] = main
    left = re.findall(r"\{\{[^}]+\}\}", main)
    if left:
        raise SystemExit(f"{p['src']}: token tidak dikenal {left}")
    other = "en" if CUR["lang"] == "id" else "id"
    alt = ALT.get((other, p["id_path"])) or lp("/", other)
    return f"""{head(p, url)}
<body>
{header(p.get('nav'), alt)}
<main id="main">
{main}
</main>
{footer()}
</body>
</html>
"""


def write_redirects():
    for old, new in REDIRECTS.items():
        target = SITE + new
        out = out_path(old)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Halaman dipindahkan | Harsha Advisory</title>
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{target}">
  <meta http-equiv="refresh" content="0; url={new}">
  <script>location.replace("{new}" + location.hash);</script>
</head>
<body>
  <p>Halaman ini telah dipindahkan ke <a href="{new}">{target}</a>.</p>
</body>
</html>
""", encoding="utf-8", newline="\n")
        print("redirect", old, "->", new)


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


MAIN_ORDER = ["/", CFO_URL, "/layanan/evaluasi-keuangan-bisnis/", "/layanan/pelatihan-keuangan/",
              "/sustainable-finance/", "/case-studies/", "/tentang/", "/kontak/",
              "/insights/", "/kamus-keuangan/", "/katalog/"]


def main_pages_sorted(pages):
    order = {path: i for i, path in enumerate(MAIN_ORDER)}
    main_pages = [p for p in pages if not p.get("noindex") and p.get("layout") != "article"]
    return sorted(main_pages, key=lambda p: order.get(p["id_path"], 99))


def write_llms(pages, articles, shop, en_pages):
    def line(p):
        return f"- [{p['title']}]({SITE}{p['path']}): {p['description']}"
    main_pages = main_pages_sorted(pages)
    en_main = main_pages_sorted(en_pages)
    english = ""
    if en_main:
        english = f"""
## English version
Seluruh halaman juga tersedia dalam bahasa Inggris di {SITE}/en/ . Halaman utama:
{chr(10).join(line(p) for p in en_main)}
"""
    text = f"""# Harsha Advisory

> Harsha Advisory (PT Harsha Dana Digital) adalah firma konsultasi keuangan bisnis yang membantu pemilik usaha dan manajemen di seluruh Indonesia mengambil keputusan melalui analisis keuangan dan pendampingan strategis. Layanan utama kami adalah Fractional CFO, dilengkapi Business Financial Evaluation (BFE) dan Corporate Financial Training.

Fakta utama:
- Nama: Harsha Advisory. Badan usaha: PT Harsha Dana Digital.
- Layanan: Fractional CFO (layanan unggulan), Business Financial Evaluation (BFE), dan Pelatihan Keuangan untuk manajemen dan peserta perusahaan.
- Founder & CEO: Anak Agung Ngurah Mustakawarman, CFP®, dengan lisensi Penasihat Investasi dari OJK. Lebih dari 12 tahun pengalaman perbankan dan 10 tahun pengalaman investasi; lebih dari 200 klien financial planning di 4 negara (Indonesia, Amerika Serikat, Jepang, Singapura).
- Penghargaan founder: Top 40 Youth Economic Leadership Program (Bank Indonesia Institute); Top 50 Startup Terbaik Indonesia (Kemenparekraf).
- Alamat: Jl. Tukad Unda No.6, Denpasar Selatan, Bali 80226. Melayani klien di seluruh Indonesia.
- Kontak: {EMAIL}, WhatsApp {WA_DISPLAY} ({WA.split("?")[0]}). Konsultasi awal 30 menit gratis via WhatsApp
- Klien pelatihan antara lain: British Petroleum, Petronas, Kangean Energy, Bank Indonesia, Komdigi, GoPay, BPR Lestari.
- Biaya: Fractional CFO mulai dari {PRICE_TEXT} per bulan, dengan periode kerja sama minimal 3 bulan; Business Financial Evaluation dan Corporate Financial Training disusun sesuai ruang lingkup. Penawaran akhir mengikuti kebutuhan dan cakupan pekerjaan.

## Halaman utama
{chr(10).join(line(p) for p in main_pages)}

## Produk digital
{chr(10).join(line(a) for a in shop)}

## Artikel dan panduan
{chr(10).join(line(a) for a in articles)}
{english}
## Opsional
- [Isi lengkap website dalam teks]({SITE}/llms-full.txt): seluruh halaman dan artikel dalam satu file teks.
"""
    (ROOT / "llms.txt").write_text(text, encoding="utf-8", newline="\n")


def html_to_text(s):
    s = re.sub(r"<(script|style|svg|form)\b.*?</\1>", "", s, flags=re.S)
    s = re.sub(r"<h([1-4])[^>]*>(.*?)</h\1>",
               lambda m: "\n\n" + "#" * (int(m.group(1)) + 1) + " " + strip_tags(m.group(2)) + "\n", s, flags=re.S)
    s = re.sub(r"<summary[^>]*>(.*?)</summary>", lambda m: "\n\nT: " + strip_tags(m.group(1)) + "\n", s, flags=re.S)
    s = re.sub(r"<dt[^>]*>(.*?)</dt>", lambda m: "\n- " + strip_tags(m.group(1)) + ": ", s, flags=re.S)
    s = re.sub(r"<li[^>]*>", "\n- ", s)
    s = re.sub(r"</(td|th)>", " | ", s)
    s = re.sub(r"</?(p|div|section|tr|table|ul|ol|dl|figure|blockquote|details|aside|br)\b[^>]*>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in s.splitlines()]
    s = "\n".join(l for l in lines if l and l != "|")
    return re.sub(r"\n(#+ )", r"\n\n\1", s).strip()


def write_llms_full(pages, articles, shop):
    order = {"/": 0}
    main_pages = [p for p in pages if not p.get("noindex") and p.get("layout") != "article"]
    main_pages.sort(key=lambda p: (order.get(p["path"], 2), p["path"]))
    parts = [f"# Harsha Advisory: isi lengkap website\n\nSumber: {SITE}/ . Diperbarui {TODAY}. "
             f"Ringkasan singkat ada di {SITE}/llms.txt"]
    for p in main_pages + shop + articles:
        parts.append(f"\n\n---\n\n# {p['title']}\n\nURL: {SITE}{p['path']}\n\n{html_to_text(p['main_html'])}")
    (ROOT / "llms-full.txt").write_text("".join(parts) + "\n", encoding="utf-8", newline="\n")


def prepare(lang, folder):
    """Muat semua halaman, artikel, dan produk untuk satu bahasa."""
    CUR["lang"] = lang
    pages = load_pages(folder, lang)
    if not pages:
        return None
    articles = sorted([p for p in pages if p.get("layout") == "article"], key=lambda a: a.get("order", 99))
    products = load_products(lang)
    shop = product_pages(products)
    katalog = next((p for p in pages if p["id_path"] == "/katalog/"), None)
    if katalog:
        katalog["schema"] = [{
            "@type": "ItemList", "name": ("Harsha Advisory Digital Products" if lang == "en" else "Produk Digital Harsha Advisory"),
            "itemListElement": [{"@type": "ListItem", "position": i, "name": o["name"], "url": SITE + product_url(o)}
                                for i, o in enumerate(products, start=1)],
        }]
    for p in pages:
        if p.get("layout") == "article":
            p.setdefault("crumbs", [["Insights", lp("/insights/")], [p["title"], None]])
            p["words"] = article_words(p)
            p["minutes"] = max(2, math.ceil(p["words"] / 200))
    return pages, articles, products, shop


def main():
    sites = {}
    for lang, folder in (("id", PAGES), ("en", PAGES_EN)):
        data = prepare(lang, folder)
        if data:
            sites[lang] = data
    ALT.clear()
    for lang, (pages, _, _, shop) in sites.items():
        for p in pages + shop:
            ALT[(lang, p["id_path"])] = p["path"]
    everything = []
    for lang, (pages, articles, products, shop) in sites.items():
        CUR["lang"] = lang
        for p in pages + shop:
            target = out_path(p["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(p, articles, products), encoding="utf-8", newline="\n")
            print("ok", p["path"])
        everything += pages + shop
    CUR["lang"] = "id"
    write_redirects()
    write_sitemap(everything)
    pages, articles, _, shop = sites["id"]
    en_pages = sites["en"][0] if "en" in sites else []
    write_llms(pages, articles, shop, en_pages)
    write_llms_full(pages, articles, shop)
    print(f"{len(everything)} halaman ({', '.join(sites)}), sitemap.xml, llms.txt, llms-full.txt")


if __name__ == "__main__":
    main()
