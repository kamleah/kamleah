#!/usr/bin/env python3
"""Generate the animated SVG graphics used by README.md.

Run:  python scripts/generate_assets.py          (animated, for GitHub)
      python scripts/generate_assets.py --static (no animation, for previews)

All text comes from the CONTENT block below. Edit it and re-run to refresh assets/.
"""
from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
STATIC = "--static" in sys.argv

# ---------------------------------------------------------------- content
NAME = "Kamlesh Gupta"
TITLE = "Full-Stack Software Engineer"
CURRENT = "Software Engineer II at SimStar Asia"
ROTATING = [
    "Python  |  Django  |  FastAPI",
    "React  |  Next.js  |  React Native",
    "Serverless AWS  |  PostgreSQL  |  Docker",
    "Booking  |  Payments  |  Healthtech",
]
STATS = [
    ("6+", ["years building", "production software"]),
    ("6+", ["production platforms", "led end to end"]),
    ("25%", ["faster API responses", "via PostgreSQL tuning"]),
    ("3", ["payment gateways", "integrated"]),
]
# (label, start year fraction, end year fraction) on a 2020..2027 axis
TECHIBEARS = (2020.09, 2025.33)   # 04 Feb 2020 to 30 Apr 2025
CODILAR = (2025.40, 2025.50)      # 26 May to 30 Jun 2025
SERIOTON = (2025.57, 2025.64)     # 28 Jul to 22 Aug 2025
NEOSOFT = (2025.85, 2025.91)      # 07 to 30 Nov 2025
SIMSTAR = (2025.94, 2026.83)      # 09 Dec 2025 to present

PROJECTS = [
    dict(file="card-pi-play", name="Pi-Play", cat="Sports tech", tagline="Multi-city padel and pickleball booking",
         lines=["Turf search, slot booking and coupon checkout", "Split payments with Razorpay, plus SMS and WhatsApp OTPs"],
         chips=["FastAPI", "PostgreSQL", "React Native", "Razorpay"], visual="slots"),
    dict(file="card-just-padel", name="Just Padel", cat="Sports tech", tagline="Booking across web, admin and mobile",
         lines=["Django REST APIs, React admin and React Native apps", "Multi-location admin calendar and Amazon PayFort"],
         chips=["Django REST", "React.js", "React Native", "AWS"], visual="calendar"),
    dict(file="card-virtuscreening", name="VirtuScreening v2", cat="Healthtech", tagline="Dental screening on a serverless backend",
         lines=["Migrated from Amplify and DynamoDB to FastAPI", "Bulk Excel patient import and automated reports"],
         chips=["FastAPI", "MySQL", "AWS Lambda", "API Gateway"], visual="migration"),
]

TECH = [
    ("Languages", "#6D8BFF", ["Python", "TypeScript", "JavaScript", "SQL"]),
    ("Backend", "#46C2A8", ["Django", "Django REST", "FastAPI", "Node.js", "Express.js", "NestJS", "Fastify", "Odoo 18"]),
    ("Frontend", "#E3EE5A", ["React.js", "Next.js", "Angular", "Redux Toolkit", "MobX", "Tailwind CSS"]),
    ("Mobile", "#FF9F6B", ["React Native", "Expo"]),
    ("Data", "#B28CFF", ["PostgreSQL", "MySQL", "MongoDB", "DynamoDB", "Amazon RDS", "SQLite"]),
    ("Cloud and DevOps", "#5CC8F2", ["AWS Lambda", "S3", "EC2", "Amplify", "API Gateway", "Docker", "Kubernetes", "Nginx", "CI/CD"]),
    ("AI and automation", "#FF7FA8", ["LangChain", "LangGraph", "OpenCV", "PyTorch", "Scikit-learn", "Pandas", "NumPy"]),
    ("Integrations", "#F2C94C", ["Razorpay", "Amazon PayFort", "MyFatoorah", "Twilio", "WhatsApp Business API", "JWT", "OAuth2"]),
]

SECTIONS = [
    ("sec-career", "Career", "Feb 2020 to present"),
    ("sec-projects", "Selected projects", "Click a card for the case study"),
    ("sec-expertise", "Technical expertise", "What I use in production"),
    ("sec-github", "GitHub activity", "Updated daily"),
    ("sec-contact", "Contact", "Open to full-stack roles and client work"),
]

# ---------------------------------------------------------------- helpers
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
INK, MUTED, SOFT = "#ECEFF3", "#98A2B0", "#B6C0D0"
ACCENT, BALL = "#6D8BFF", "#E3EE5A"
BG1, BG2 = "#0A0F1F", "#16204A"


def svg(w: int, h: int, body: str, css: str = "", title: str = "") -> str:
    anim = "" if STATIC else css
    reduce = "" if STATIC else "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
    t = f"<title>{escape(title)}</title>" if title else ""
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'font-family="{FONT}">{t}<style>{anim}{reduce}</style>'
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/>'
        f'<stop offset="1" stop-color="{BG2}"/></linearGradient>'
        f'<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<line x1="0" y1="0" x2="0" y2="7" stroke="#ffffff" stroke-opacity="0.16" stroke-width="2"/></pattern></defs>'
        f"{body}</svg>\n"
    )


def write(name: str, content: str) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.svg").write_text(content, encoding="utf-8")


def chip_w(text: str, size: float = 13) -> float:
    return len(text) * size * 0.56 + 26


def cell(x, y, w, h, kind="idle", cls="", style=""):
    if kind == "taken":
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="url(#hatch)" stroke="#fff" stroke-opacity="0.1"/>')
    return (f'<rect class="{cls}" style="{style}" x="{x}" y="{y}" width="{w}" height="{h}" rx="9" '
            f'fill="#fff" fill-opacity="0.05" stroke="#fff" stroke-opacity="0.14"/>')


def pick(x, y, w, h, delay, period=9):
    """A highlighted slot that switches on and off like a user picking it."""
    return (f'<rect class="pick" style="animation-delay:{delay}s;animation-duration:{period}s" x="{x}" y="{y}" '
            f'width="{w}" height="{h}" rx="9" fill="{BALL}" opacity="{1 if STATIC and delay < 3 else 0}"/>')


PICK_CSS = "@keyframes pick{0%,8%{opacity:0}16%,60%{opacity:1}70%,100%{opacity:0}}.pick{animation:pick 9s ease-in-out infinite}"
FADE_CSS = "@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}.fade{animation:fade .8s cubic-bezier(.2,.7,.2,1) both}"


# ---------------------------------------------------------------- banner
def banner() -> str:
    gx, gy, cw, ch, gap = 716, 62, 40, 40, 8
    taken = {(1, 1), (3, 0), (0, 3), (2, 4), (4, 2), (1, 4)}
    picks = [(0, 1, 0.0), (1, 2, 0.7), (2, 2, 1.4), (3, 3, 2.1), (4, 0, 2.8), (2, 0, 3.5), (3, 4, 4.2)]
    cells = []
    for r in range(5):
        for c in range(5):
            x, y = gx + c * (cw + gap), gy + r * (ch + gap)
            cells.append(cell(x, y, cw, ch, "taken" if (c, r) in taken else "idle"))
    for c, r, d in picks:
        cells.append(pick(gx + c * (cw + gap), gy + r * (ch + gap), cw, ch, d))

    rot = []
    n = len(ROTATING)
    for i, line in enumerate(ROTATING):
        style = f"animation-delay:{i * 3}s"
        base = 1 if (STATIC and i == 0) else 0
        rot.append(f'<text class="rot" style="{style}" x="56" y="262" font-size="19" fill="{SOFT}" opacity="{base}">{escape(line)}</text>')

    css = (
        PICK_CSS + FADE_CSS
        + f"@keyframes rot{{0%{{opacity:0;transform:translateY(6px)}}4%,22%{{opacity:1;transform:none}}26%,100%{{opacity:0}}}}"
        + f".rot{{animation:rot {n * 3}s ease infinite}}"
        + "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}.dot{animation:pulse 2s ease-in-out infinite}"
        + ".d1{animation-delay:.05s}.d2{animation-delay:.2s}.d3{animation-delay:.35s}"
    )
    body = f"""
<clipPath id="bc"><rect width="1000" height="340" rx="26"/></clipPath>
<rect width="1000" height="340" rx="26" fill="url(#bg)"/>
<g clip-path="url(#bc)"><circle cx="840" cy="170" r="210" fill="{ACCENT}" fill-opacity="0.16"/>
<circle cx="880" cy="60" r="120" fill="{BALL}" fill-opacity="0.06"/></g>
<rect x="0.5" y="0.5" width="999" height="339" rx="25.5" fill="none" stroke="#fff" stroke-opacity="0.12"/>
<g class="fade d1"><rect x="56" y="52" width="{chip_w(CURRENT, 14) + 22:.0f}" height="34" rx="17" fill="#fff" fill-opacity="0.08"/>
<circle class="dot" cx="76" cy="69" r="5" fill="{BALL}"/>
<text x="92" y="74" font-size="14" fill="{SOFT}">{escape(CURRENT)}</text></g>
<text class="fade d2" x="54" y="160" font-size="64" font-weight="700" fill="{INK}" letter-spacing="-2">{escape(NAME)}</text>
<text class="fade d3" x="56" y="208" font-size="27" font-weight="600" fill="{ACCENT}">{escape(TITLE)}</text>
{''.join(rot)}
<g aria-hidden="true">{''.join(cells)}</g>
<text x="716" y="318" font-size="12.5" fill="{MUTED}">Slot selection, the core of what I build</text>
"""
    return svg(1000, 340, body, css, f"{NAME}, {TITLE}")


# ---------------------------------------------------------------- stats
def stats() -> str:
    parts = []
    for i, (num, lines) in enumerate(STATS):
        x = i * 256
        parts.append(
            f'<g class="fade" style="animation-delay:{0.1 + i * 0.12}s">'
            f'<rect x="{x}" y="0" width="232" height="128" rx="20" fill="url(#bg)"/>'
            f'<rect x="{x + 0.5}" y="0.5" width="231" height="127" rx="19.5" fill="none" stroke="#fff" stroke-opacity="0.12"/>'
            f'<text x="{x + 24}" y="64" font-size="44" font-weight="700" fill="{BALL if i == 2 else INK}" letter-spacing="-1.5">{num}</text>'
            f'<text x="{x + 24}" y="92" font-size="14" fill="{SOFT}">{escape(lines[0])}</text>'
            f'<text x="{x + 24}" y="111" font-size="14" fill="{SOFT}">{escape(lines[1])}</text></g>'
        )
    return svg(1000, 128, "".join(parts), FADE_CSS, "Career highlights")


# ---------------------------------------------------------------- timeline
def timeline() -> str:
    x0, x1, y0, y1 = 50, 950, 2020, 2027
    X = lambda yr: x0 + (yr - y0) * (x1 - x0) / (y1 - y0)
    ticks = "".join(
        f'<line x1="{X(y):.1f}" y1="164" x2="{X(y):.1f}" y2="176" stroke="#3A4663"/>'
        f'<text x="{X(y):.1f}" y="198" text-anchor="middle" font-size="13" fill="{MUTED}">{y}</text>'
        for y in range(y0, y1 + 1)
    )
    tb, ss = X(TECHIBEARS[0]), X(SIMSTAR[0])
    tb_w, ss_w = X(TECHIBEARS[1]) - tb, X(SIMSTAR[1]) - ss
    css = (
        "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        ".bar{transform-box:fill-box;transform-origin:left center;animation:grow 1.1s cubic-bezier(.2,.7,.2,1) both}"
        "@keyframes ping{0%{transform:scale(1);opacity:.7}100%{transform:scale(3);opacity:0}}"
        ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2s ease-out infinite}"
        + FADE_CSS
    )
    small = [
        (CODILAR, "Codilar Technologies, Lead Software Engineer, May to Jun 2025", 226, 1.1),
        (SERIOTON, "Serioton LLP (HAANAA), Software Engineer I, Jul to Aug 2025", 248, 1.3),
        (NEOSOFT, "Neosoft Pvt Ltd, Senior Software Engineer, Nov 2025", 270, 1.5),
    ]
    marks = []
    for (a, b), label, ly, d in small:
        x, w = X(a), max(X(b) - X(a), 7)
        cx = x + w / 2
        marks.append(
            f'<rect class="bar" style="animation-delay:{d}s" x="{x:.1f}" y="118" width="{w:.1f}" height="36" rx="4" fill="{SOFT}"/>'
            f'<line x1="{cx:.1f}" y1="154" x2="{cx:.1f}" y2="{ly - 12}" stroke="#3A4663" stroke-dasharray="3 3"/>'
            f'<text class="fade" style="animation-delay:{d + 0.2}s" x="{cx + 4:.1f}" y="{ly}" text-anchor="end" font-size="13" fill="{SOFT}">{escape(label)}</text>'
        )
    body = f"""
<rect width="1000" height="296" rx="26" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="999" height="295" rx="25.5" fill="none" stroke="#fff" stroke-opacity="0.12"/>
<line x1="{x0}" y1="170" x2="{x1}" y2="170" stroke="#3A4663" stroke-width="2"/>
{ticks}
<g class="fade" style="animation-delay:.2s">
<text x="{tb:.0f}" y="48" font-size="19" font-weight="700" fill="{INK}">Techibears Pvt Ltd</text>
<text x="{tb:.0f}" y="70" font-size="14.5" fill="{SOFT}">Senior Software Developer</text>
<text x="{tb:.0f}" y="92" font-size="13" fill="{MUTED}">Feb 2020 to Apr 2025</text></g>
<rect class="bar" style="animation-delay:.3s" x="{tb:.1f}" y="118" width="{tb_w:.1f}" height="36" rx="12" fill="{ACCENT}"/>
<text class="fade" style="animation-delay:.9s" x="{tb + 18:.0f}" y="141" font-size="14" font-weight="600" fill="#0A0F1F">6+ production platforms: sports tech, healthtech, gaming</text>
{''.join(marks)}
<g class="fade" style="animation-delay:.6s" text-anchor="end">
<text x="{X(SIMSTAR[1]):.0f}" y="48" font-size="19" font-weight="700" fill="{INK}">SimStar Asia Ltd</text>
<text x="{X(SIMSTAR[1]):.0f}" y="70" font-size="14.5" fill="{SOFT}">Software Engineer II</text>
<text x="{X(SIMSTAR[1]):.0f}" y="92" font-size="13" fill="{MUTED}">Dec 2025 to present</text></g>
<rect class="bar" style="animation-delay:1.7s" x="{ss:.1f}" y="118" width="{ss_w:.1f}" height="36" rx="12" fill="{BALL}"/>
<circle class="ping" cx="{ss + ss_w:.1f}" cy="136" r="6" fill="{BALL}"/>
<circle cx="{ss + ss_w:.1f}" cy="136" r="6" fill="{BALL}"/>
"""
    return svg(1000, 296, body, css, "Career timeline from 2020 to 2026")


# ---------------------------------------------------------------- section headers
def section(name: str, title: str, sub: str) -> str:
    css = (
        FADE_CSS
        + "@keyframes sweep{0%{transform:translateX(-200px)}100%{transform:translateX(1000px)}}"
        + ".sweep{animation:sweep 5s ease-in-out infinite}"
    )
    body = f"""
<clipPath id="c"><rect width="1000" height="64" rx="18"/></clipPath>
<rect width="1000" height="64" rx="18" fill="url(#bg)"/>
<g clip-path="url(#c)"><rect class="sweep" x="0" y="0" width="140" height="64" fill="{ACCENT}" fill-opacity="0.12" transform="skewX(-20)"/></g>
<rect x="0.5" y="0.5" width="999" height="63" rx="17.5" fill="none" stroke="#fff" stroke-opacity="0.12"/>
<rect x="24" y="20" width="8" height="24" rx="4" fill="{BALL}"/>
<text x="46" y="41" font-size="24" font-weight="700" fill="{INK}" letter-spacing="-0.5">{escape(title)}</text>
<text x="976" y="39" text-anchor="end" font-size="14" fill="{MUTED}">{escape(sub)}</text>
"""
    return svg(1000, 64, body, css, title)


# ---------------------------------------------------------------- project cards
def visual_slots(ox, oy):
    out, taken = [], {(2, 0), (0, 2), (3, 2), (1, 3)}
    cw, ch, g = 54, 40, 8
    for r in range(4):
        for c in range(5):
            x, y = ox + c * (cw + g), oy + r * (ch + g)
            out.append(cell(x, y, cw, ch, "taken" if (c, r) in taken else "idle"))
    for c, r, d in [(1, 1, 0.0), (2, 1, 0.8), (3, 3, 1.6)]:
        out.append(pick(ox + c * (cw + g), oy + r * (ch + g), cw, ch, d, 7))
    return "".join(out)


def visual_calendar(ox, oy):
    cw, ch, g = 62, 40, 8
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    out = [f'<text x="{ox + c * (cw + g) + cw / 2}" y="{oy - 8}" text-anchor="middle" font-size="12" fill="{MUTED}">{d}</text>' for c, d in enumerate(days)]
    blocks = {(0, 0, 2): ACCENT, (1, 1, 1): "#fff", (2, 0, 1): ACCENT, (2, 2, 2): "#fff", (3, 1, 2): BALL, (4, 0, 1): "#fff", (4, 3, 1): ACCENT}
    for c in range(5):
        for r in range(4):
            out.append(cell(ox + c * (cw + g), oy + r * (ch + g), cw, ch))
    for (c, r, span), color in blocks.items():
        h = span * ch + (span - 1) * g
        op = 0.85 if color != "#fff" else 0.16
        out.append(f'<rect x="{ox + c * (cw + g)}" y="{oy + r * (ch + g)}" width="{cw}" height="{h}" rx="9" fill="{color}" fill-opacity="{op}"/>')
    return "".join(out)


def visual_migration(ox, oy):
    def node(x, y, w, t, s, hot=False):
        f = ACCENT if hot else "#fff"
        return (f'<rect x="{x}" y="{y}" width="{w}" height="56" rx="14" fill="{f}" fill-opacity="{0.22 if hot else 0.06}" '
                f'stroke="{f}" stroke-opacity="{0.6 if hot else 0.16}"/>'
                f'<text x="{x + 14}" y="{y + 24}" font-size="14" font-weight="700" fill="{INK}">{t}</text>'
                f'<text x="{x + 14}" y="{y + 43}" font-size="12" fill="{MUTED}">{s}</text>')
    return (
        f'<text x="{ox}" y="{oy + 2}" font-size="12" fill="{MUTED}">Version 1</text>'
        + node(ox, oy + 12, 292, "AWS Amplify", "Lambda, API Gateway, DynamoDB")
        + f'<text x="{ox + 146}" y="{oy + 96}" text-anchor="middle" font-size="12" fill="{BALL}">migrated to version 2</text>'
        + f'<line x1="{ox}" y1="{oy + 92}" x2="{ox + 40}" y2="{oy + 92}" stroke="#3A4663"/><line x1="{ox + 252}" y1="{oy + 92}" x2="{ox + 292}" y2="{oy + 92}" stroke="#3A4663"/>'
        + node(ox, oy + 112, 92, "API", "Gateway", True) + node(ox + 100, oy + 112, 92, "Lambda", "FastAPI", True) + node(ox + 200, oy + 112, 92, "MySQL", "Data store", True)
    )


def card(p: dict) -> str:
    chips, x = [], 40
    for c in p["chips"]:
        w = chip_w(c)
        chips.append(
            f'<rect x="{x:.0f}" y="206" width="{w:.0f}" height="30" rx="15" fill="{ACCENT}" fill-opacity="0.16" stroke="{ACCENT}" stroke-opacity="0.45"/>'
            f'<text x="{x + w / 2:.0f}" y="226" text-anchor="middle" font-size="13" fill="{INK}">{escape(c)}</text>'
        )
        x += w + 10
    vis = {"slots": visual_slots, "calendar": visual_calendar, "migration": visual_migration}[p["visual"]]
    oy = 40 if p["visual"] == "slots" else 46 if p["visual"] == "calendar" else 42
    body = f"""
<clipPath id="cc"><rect width="1000" height="260" rx="26"/></clipPath>
<rect width="1000" height="260" rx="26" fill="url(#bg)"/>
<g clip-path="url(#cc)"><circle cx="800" cy="130" r="170" fill="{ACCENT}" fill-opacity="0.10"/></g>
<rect x="0.5" y="0.5" width="999" height="259" rx="25.5" fill="none" stroke="#fff" stroke-opacity="0.12"/>
<text x="40" y="52" font-size="14" fill="{BALL}">{escape(p['cat'])}</text>
<text x="40" y="94" font-size="36" font-weight="700" fill="{INK}" letter-spacing="-1">{escape(p['name'])}</text>
<text x="40" y="124" font-size="18" fill="{SOFT}">{escape(p['tagline'])}</text>
<text x="40" y="160" font-size="14.5" fill="{MUTED}">{escape(p['lines'][0])}</text>
<text x="40" y="182" font-size="14.5" fill="{MUTED}">{escape(p['lines'][1])}</text>
{''.join(chips)}
<g aria-hidden="true">{vis(610, oy)}</g>
<text x="960" y="244" text-anchor="end" font-size="13" fill="{ACCENT}">Read the case study</text>
"""
    return svg(1000, 260, body, PICK_CSS, f"{p['name']}: {p['tagline']}")


# ---------------------------------------------------------------- tech grid
def tech() -> str:
    rows, y, idx = [], 30, 0
    for label, color, items in TECH:
        x, line_y, parts = 214, y, []
        parts.append(f'<text x="36" y="{y + 21}" font-size="14.5" font-weight="700" fill="{INK}">{escape(label)}</text>')
        parts.append(f'<rect x="20" y="{y + 7}" width="4" height="18" rx="2" fill="{color}"/>')
        for it in items:
            w = chip_w(it)
            if x + w > 964:
                x, line_y = 214, line_y + 40
            parts.append(
                f'<g class="fade" style="animation-delay:{idx * 0.03:.2f}s">'
                f'<rect x="{x:.0f}" y="{line_y}" width="{w:.0f}" height="32" rx="16" fill="{color}" fill-opacity="0.14" stroke="{color}" stroke-opacity="0.5"/>'
                f'<text x="{x + w / 2:.0f}" y="{line_y + 21}" text-anchor="middle" font-size="13" fill="{INK}">{escape(it)}</text></g>'
            )
            x += w + 10
            idx += 1
        rows.append("".join(parts))
        y = line_y + 52
    h = y - 4
    body = (f'<rect width="1000" height="{h}" rx="26" fill="url(#bg)"/>'
            f'<rect x="0.5" y="0.5" width="999" height="{h - 1}" rx="25.5" fill="none" stroke="#fff" stroke-opacity="0.12"/>' + "".join(rows))
    return svg(1000, h, body, FADE_CSS, "Technical expertise")


# ---------------------------------------------------------------- footer
def footer() -> str:
    css = (
        "@keyframes drift{from{transform:translateX(0)}to{transform:translateX(-500px)}}"
        ".w1{animation:drift 14s linear infinite}.w2{animation:drift 22s linear infinite reverse}"
    )
    wave = lambda amp, y: "M0 {y} ".format(y=y) + " ".join(f"q125 {-amp if i % 2 == 0 else amp} 250 0" if i == 0 else f"t250 0" for i in range(9))
    body = f"""
<clipPath id="c"><rect width="1000" height="210" rx="26"/></clipPath>
<rect width="1000" height="210" rx="26" fill="url(#bg)"/>
<g clip-path="url(#c)">
<path class="w2" d="{wave(18, 150)} V210 H0 Z" fill="{ACCENT}" fill-opacity="0.14"/>
<path class="w1" d="{wave(14, 172)} V210 H0 Z" fill="{BALL}" fill-opacity="0.10"/></g>
<rect x="0.5" y="0.5" width="999" height="209" rx="25.5" fill="none" stroke="#fff" stroke-opacity="0.12"/>
<text x="500" y="88" text-anchor="middle" font-size="38" font-weight="700" fill="{INK}" letter-spacing="-1">Let’s build something reliable.</text>
<text x="500" y="124" text-anchor="middle" font-size="17" fill="{SOFT}">Booking, payments, healthtech and serverless AWS, from API to mobile app.</text>
"""
    return svg(1000, 210, body, css, "Let’s build something reliable")


def main() -> None:
    write("banner", banner())
    write("stats", stats())
    write("timeline", timeline())
    write("tech", tech())
    write("footer", footer())
    for name, title, sub in SECTIONS:
        write(name, section(name, title, sub))
    for p in PROJECTS:
        write(p["file"], card(p))
    print(f"Wrote {len(list(OUT.glob('*.svg')))} SVGs to {OUT}")


if __name__ == "__main__":
    main()
