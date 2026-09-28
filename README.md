# Her Space Women's Clinic — Dr. Ruchi

Premium static website for **Her Space Women's Clinic by Dr. Ruchi** (Obstetrician & Gynaecologist), C-93 Geetanjali Marg, Shivalik Colony, Malviya Nagar, New Delhi 110017.

Pages: `index.html`, `about.html`, `services.html`, `contact.html` — plain HTML/CSS/JS, no framework.

## Editing
Pages are assembled from `src/` by a tiny script — edit the templates, then rebuild:

```bash
python3 build.py
```

- Shared header/footer/sprite: `src/_header.html`, `src/_footer.html`, `src/_sprite.svg`
- Page content: `src/index.html`, `src/about.html`, `src/services.html`, `src/contact.html`
- Titles, descriptions and schema: `build.py`
- Styles / behaviour: `assets/css/style.css`, `assets/js/main.js`

## To do / placeholders
- Replace the "Portrait of Dr. Ruchi" placeholder (home + about) with a real photo of the doctor.
- Photography is CC0 / public-domain stock (via Openverse) — swap in real clinic photos when available.
- Consultation timings and email are not published yet (contact page asks visitors to call).
- Appointment form and WhatsApp buttons use 92652 59256 — change in `src/_layout.html`, `src/index.html`, `assets/js/main.js` if a different WhatsApp number is preferred.
