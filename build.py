#!/usr/bin/env python3
"""Static site builder: wraps src/<page>.html in src/_layout.html and writes to the repo root.
Run:  python3 build.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
SITE = "https://mbl9645964-cell.github.io/her-space-womens-clinic/"

PAGES = {
    "index": ("Her Space Women’s Clinic · Dr. Ruchi — Gynaecologist in Malviya Nagar, New Delhi",
              "Her Space Women’s Clinic by Dr. Ruchi (MBBS, DGO, DNB, MRCOG, FMAS, DMAS), Obstetrician & Gynaecologist in Malviya Nagar, New Delhi — pregnancy care, PCOS, menstrual disorders, infertility and menopause wellness.",
              "index.html", "home"),
    "about": ("About Dr. Ruchi · Obstetrician & Gynaecologist · Her Space Women’s Clinic",
              "Meet Dr. Ruchi — Obstetrician & Gynaecologist (MBBS, DGO, DNB, MRCOG, FMAS, DMAS) at Her Space Women’s Clinic, Malviya Nagar, New Delhi.",
              "about.html", "about"),
    "services": ("Services · Pregnancy, PCOS, Infertility & Menopause Care · Her Space Women’s Clinic",
                 "Antenatal & pregnancy care, gynaecological care, PCOS & hormonal disorders, menstrual disorders, infertility care and menopause wellness with Dr. Ruchi in Malviya Nagar, New Delhi.",
                 "services.html", "services"),
    "contact": ("Contact & Book an Appointment · Her Space Women’s Clinic, Malviya Nagar",
                "Book an appointment with Dr. Ruchi at Her Space Women’s Clinic, C-93 Geetanjali Marg, Shivalik Colony, Malviya Nagar, New Delhi 110017. Call 92652 59256 or 96544 47293.",
                "contact.html", "contact"),
}

JSONLD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": ["MedicalClinic", "LocalBusiness"],
            "@id": SITE + "#clinic",
            "name": "Her Space Women's Clinic",
            "alternateName": "Her Space Women's Clinic by Dr. Ruchi",
            "slogan": "Your Health. Your Space. Our Care.",
            "url": SITE,
            "image": SITE + "assets/img/og-image.jpg",
            "telephone": ["+91-9265259256", "+91-9654447293"],
            "medicalSpecialty": ["Obstetric", "Gynecologic"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "C-93, Geetanjali Marg, C Block, Shivalik Colony, Malviya Nagar",
                "addressLocality": "New Delhi",
                "addressRegion": "Delhi",
                "postalCode": "110017",
                "addressCountry": "IN",
            },
            "employee": {"@id": SITE + "#dr-ruchi"},
        },
        {
            "@type": "Physician",
            "@id": SITE + "#dr-ruchi",
            "name": "Dr. Ruchi",
            "jobTitle": "Obstetrician & Gynaecologist",
            "medicalSpecialty": ["Obstetric", "Gynecologic"],
            "description": "MBBS, DGO, DNB, MRCOG, FMAS, DMAS",
            "worksFor": {"@id": SITE + "#clinic"},
        },
    ],
}

def main():
    layout = (SRC / "_layout.html").read_text()
    sprite = (SRC / "_sprite.svg").read_text()
    footer = (SRC / "_footer.html").read_text()
    header_t = (SRC / "_header.html").read_text()
    ld = json.dumps(JSONLD, ensure_ascii=False)
    for key, (title, desc, path, nav) in PAGES.items():
        header = header_t.replace(f'data-nav="{nav}"', f'data-nav="{nav}" aria-current="page"')
        body = (SRC / f"{key}.html").read_text()
        html = (layout.replace("{{TITLE}}", title.replace("&", "&amp;"))
                .replace("{{DESC}}", desc.replace("&", "&amp;"))
                .replace("{{SITE}}", SITE).replace("{{PATH}}", "" if path == "index.html" else path)
                .replace("{{KEY}}", key).replace("{{JSONLD}}", ld)
                .replace("{{SPRITE}}", sprite).replace("{{HEADER}}", header)
                .replace("{{BODY}}", body).replace("{{FOOTER}}", footer))
        (ROOT / path).write_text(html)
        print("built", path)

    urls = "".join(f"  <url><loc>{SITE}{'' if p=='index.html' else p}</loc></url>\n" for _, (_, _, p, _) in PAGES.items())
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")

if __name__ == "__main__":
    main()
