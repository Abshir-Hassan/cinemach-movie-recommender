import streamlit as st
from core.constants import DARK, LIGHT


def inject_css(dark_mode: bool = True) -> None:
    p = DARK if dark_mode else LIGHT

    nav_bg       = "rgba(0,0,0,0.90)"           if dark_mode else "rgba(249,244,239,0.95)"
    nav_border   = "rgba(229,9,20,0.22)"         if dark_mode else "rgba(217,201,181,0.95)"
    nav_label    = "rgba(245,245,245,0.65)"      if dark_mode else "rgba(17,24,39,0.58)"
    nav_label_hv = "#F5F5F5"                     if dark_mode else "#111827"
    nav_active   = p["primary"]
    sk0          = p["card2"]
    sk1          = p["surface"]
    sk2          = p["border"]

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {{
  --bg:        {p["bg"]};
  --surface:   {p["surface"]};
  --card:      {p["card"]};
  --card2:     {p["card2"]};
  --border:    {p["border"]};
  --primary:   {p["primary"]};
  --primary-d: {p["primary_d"]};
  --accent:    {p["accent"]};
  --text:      {p["text"]};
  --muted:     {p["muted"]};
  --dim:       {p["dim"]};
  --success:   {p["success"]};
  --nav-bg:      {nav_bg};
  --nav-border:  {nav_border};
  --nav-label:   {nav_label};
  --nav-label-hv:{nav_label_hv};
  --nav-active:  {nav_active};
}}

/* ── Reset & global font ── */
*, html, body {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body, [class*="css"], * {{
  font-family: 'Manrope', 'Inter', system-ui, -apple-system, sans-serif !important;
  -webkit-font-smoothing: antialiased;
}}
.stApp {{ background: var(--bg) !important; color: var(--text) !important; }}
.main .block-container {{
  padding: 1rem 2.5rem 4rem;
  max-width: 1440px;
}}

/* ── Streamlit native text — force dark-mode-safe colors ── */
.stMarkdown, .stMarkdown p, .element-container p {{
  color: var(--text) !important;
  font-size: 0.97rem !important;
  line-height: 1.72 !important;
}}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown h5 {{
  color: var(--text) !important;
  font-weight: 700 !important;
}}
.stMarkdown strong, .stMarkdown b {{
  color: var(--text) !important;
  font-weight: 700 !important;
}}
.stMarkdown li {{
  color: var(--text) !important;
  font-size: 0.94rem !important;
  line-height: 1.72 !important;
}}
.stMarkdown code {{
  background: var(--surface) !important;
  color: var(--primary) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.78rem !important;
  padding: 0.1rem 0.35rem !important;
  border-radius: 3px !important;
}}
/* Tables in markdown */
.stMarkdown table {{ color: var(--text) !important; }}
.stMarkdown td, .stMarkdown th {{
  color: var(--text) !important;
  font-size: 0.82rem !important;
  border-color: var(--border) !important;
}}

/* ── Sidebar hidden ── */
[data-testid="stSidebar"]        {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}

/* ── Navbar ── */
div[data-testid="stHorizontalBlock"]:first-of-type {{
  position: sticky;
  top: 0;
  z-index: 9000;
  background: var(--nav-bg) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--nav-border);
  padding: 0.55rem 2.5rem !important;
  align-items: center !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stRadio"] {{
  display: flex; align-items: center; justify-content: center;
}}
div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stRadio"] > div {{
  display: flex !important; flex-direction: row !important; gap: 0;
  align-items: center; flex-wrap: nowrap;
}}
div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stRadio"] input[type="radio"] {{
  display: none !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stRadio"] [data-testid="stWidgetLabel"] {{
  display: none !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stRadio"] label {{
  font-family: 'Manrope', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.025em !important;
  text-transform: none !important;
  color: var(--nav-label) !important;
  padding: 0.5rem 1.25rem 0.42rem !important;
  border-radius: 0 !important;
  border-bottom: 2px solid transparent !important;
  cursor: pointer;
  transition: color 0.18s ease, border-color 0.18s ease, background 0.18s ease !important;
  white-space: nowrap !important;
  background: transparent !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stRadio"] label:hover {{
  color: var(--nav-label-hv) !important;
  background: rgba(128,128,128,0.10) !important;
  border-bottom: 2px solid rgba(128,128,128,0.35) !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stRadio"] label:has(input:checked) {{
  color: var(--nav-label-hv) !important;
  font-weight: 600 !important;
  border-bottom: 2px solid var(--nav-active) !important;
  background: transparent !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {{
  font-family: 'Manrope', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  padding: 0.35rem 0.95rem !important;
  letter-spacing: 0.04em !important;
}}

/* ── Streamlit widget overrides ── */
.stButton > button {{
  background: var(--primary) !important; color: #fff !important;
  border: none !important; border-radius: 4px !important;
  font-family: 'Manrope', sans-serif !important;
  font-weight: 700 !important; font-size: 0.92rem !important;
  letter-spacing: 0.04em !important;
  padding: 0.6rem 1.8rem !important;
  transition: background 0.15s !important;
}}
.stButton > button:hover {{ background: var(--primary-d) !important; }}

/* Widget labels (slider, select, multiselect) */
label, .stSelectbox label, .stSlider label,
.stMultiSelect label, .stSelectSlider label {{
  color: var(--muted) !important;
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
}}
/* Select / multiselect — container background */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
  background: var(--card) !important;
  border-color: var(--border) !important;
}}
/* Select / input values */
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] input,
div[data-testid="stMultiSelect"] input {{
  color: var(--text) !important;
  font-family: 'Manrope', sans-serif !important;
  font-size: 0.88rem !important;
}}
/* Dropdown list */
[data-baseweb="popover"],
[data-baseweb="popover"] ul {{
  background: var(--card) !important;
  border-color: var(--border) !important;
}}
[data-baseweb="popover"] li,
[data-baseweb="menu"] li {{
  background: var(--card) !important;
  color: var(--text) !important;
  font-family: 'Manrope', sans-serif !important;
  font-size: 0.88rem !important;
}}
[data-baseweb="popover"] li:hover,
[data-baseweb="menu"] li:hover {{
  background: var(--surface) !important;
  color: var(--text) !important;
}}
/* Slider value label */
div[data-testid="stSlider"] [data-testid="stTickBarMin"],
div[data-testid="stSlider"] [data-testid="stTickBarMax"] {{
  color: var(--muted) !important; font-size: 0.75rem !important;
}}
div[data-testid="stMetricValue"] {{
  color: var(--primary) !important; font-weight: 800 !important;
  font-size: 1.1rem !important;
}}
.stAlert {{ border-radius: 4px !important; }}
.stAlert p {{ font-size: 0.9rem !important; }}

/* Glow focus */
div[data-testid="stSelectbox"]:focus-within,
div[data-testid="stMultiSelect"]:focus-within {{
  box-shadow: 0 0 0 2px var(--primary), 0 0 18px rgba(229,9,20,0.15) !important;
  border-radius: 4px;
  transition: box-shadow 0.2s;
}}

/* ── Skeleton shimmer ── */
@keyframes shimmer {{
  0%   {{ background-position: -1400px 0; }}
  100% {{ background-position:  1400px 0; }}
}}
.skeleton {{
  background: linear-gradient(
    90deg, {sk0} 0%, {sk1} 38%, {sk2} 50%, {sk1} 62%, {sk0} 100%
  );
  background-size: 1400px 100%;
  animation: shimmer 2s ease-in-out infinite;
  border-radius: 3px;
}}

/* ── Marquee ── */
@keyframes marquee-scroll {{
  from {{ transform: translateX(0); }}
  to   {{ transform: translateX(-50%); }}
}}
.marquee-wrap {{
  overflow: hidden; position: relative;
  margin: 0 -2.5rem 2.5rem;
  height: 182px;
  mask-image: linear-gradient(to right, transparent 0%, black 6%, black 94%, transparent 100%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 6%, black 94%, transparent 100%);
}}
.marquee-track {{
  display: flex; gap: 8px;
  animation: marquee-scroll 45s linear infinite;
  width: max-content; padding: 0 4px;
}}
.marquee-poster {{
  width: 120px; height: 182px;
  border-radius: 4px; overflow: hidden; flex-shrink: 0;
  background: var(--card2);
}}
.marquee-poster img {{
  width: 100%; height: 100%;
  object-fit: cover; object-position: top;
  opacity: 0.42; transition: opacity 0.3s;
}}
.marquee-poster img:hover {{ opacity: 0.72; }}

/* ── Hero — cinematic dark always ── */
.hero {{
  position: relative; min-height: 420px;
  background: #050818;
  border-radius: 8px; overflow: hidden; margin-bottom: 0;
  display: flex; align-items: flex-end;
  box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}}
.hero-backdrop {{
  position: absolute; inset: 0; overflow: hidden;
}}
.hero-bg-img {{
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover; object-position: center top;
  filter: brightness(0.36) saturate(0.7);
  display: block; transition: opacity 0.5s;
}}
.hero-gradient {{
  position: absolute; inset: 0;
  background: linear-gradient(
    90deg, rgba(5,8,24,0.97) 0%, rgba(5,8,24,0.80) 45%, rgba(5,8,24,0.18) 100%
  );
}}
.hero-content {{
  position: relative; z-index: 2;
  padding: 3rem 3.5rem; max-width: 620px;
}}
.hero-tag {{
  display: inline-block; background: var(--primary);
  color: #fff; padding: 0.22rem 0.75rem;
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  border-radius: 2px; margin-bottom: 1rem;
}}
.hero-title {{
  font-size: 3.8rem; font-weight: 800;
  color: #fff; letter-spacing: -2px;
  line-height: 0.95; margin-bottom: 0.55rem;
}}
.hero-tagline {{
  font-size: 1rem; font-weight: 400; font-style: italic;
  color: rgba(255,255,255,0.60); margin-bottom: 0.85rem;
}}
.hero-desc {{
  font-size: 0.9rem; color: rgba(255,255,255,0.52);
  line-height: 1.75; margin-bottom: 1.5rem;
}}
.hero-actions {{ display: flex; align-items: center; gap: 0.8rem; flex-wrap: wrap; }}
.hero-btn {{
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: var(--primary); color: #fff;
  padding: 0.6rem 1.4rem; border-radius: 4px;
  font-size: 0.88rem; font-weight: 700; letter-spacing: 0.03em;
  text-decoration: none; transition: background 0.15s;
}}
.hero-btn:hover {{ background: var(--primary-d); color: #fff !important; }}
.hero-btn, .hero-btn:link, .hero-btn:visited {{ color: #fff !important; text-decoration: none !important; }}
.btn-primary, .btn-primary:link, .btn-primary:visited {{ color: #fff !important; text-decoration: none !important; }}
.btn-ghost, .btn-ghost:link, .btn-ghost:visited {{ text-decoration: none !important; }}
.hero-badge {{
  display: inline-flex; align-items: center; gap: 0.35rem;
  background: rgba(229,9,20,0.14); border: 1px solid rgba(229,9,20,0.38);
  color: var(--accent); padding: 0.45rem 0.9rem;
  border-radius: 4px; font-size: 0.83rem; font-weight: 700;
}}
.hero-badge-muted {{
  display: inline-flex; align-items: center; gap: 0.35rem;
  border: 1px solid rgba(255,255,255,0.15);
  color: rgba(255,255,255,0.48);
  padding: 0.45rem 0.9rem; border-radius: 4px;
  font-size: 0.82rem; font-weight: 500;
}}
.hero-trailer {{
  position: absolute; right: 3rem; top: 50%; transform: translateY(-50%);
  width: 280px; height: 175px;
  border: 1px solid rgba(255,255,255,0.1); border-radius: 6px;
  background: rgba(5,8,24,0.55);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 0.8rem; z-index: 3;
}}
.hero-play-circle {{
  width: 54px; height: 54px; border-radius: 50%; background: var(--primary);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: background 0.15s, transform 0.15s;
}}
.hero-play-circle:hover {{ background: var(--primary-d); transform: scale(1.1); }}
.hero-play-circle svg {{ width: 22px; height: 22px; fill: #fff; margin-left: 3px; }}
.hero-btn svg {{ width: 16px; height: 16px; flex-shrink: 0; }}
.hero-trailer-lbl {{
  font-size: 0.7rem; font-weight: 700;
  color: rgba(255,255,255,0.32);
  text-transform: uppercase; letter-spacing: 0.2em;
}}

/* ── Stat band ── */
.stat-band {{
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 1px; background: var(--border);
  border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden; margin-bottom: 2.5rem;
}}
.stat-item {{
  background: var(--card); padding: 1.5rem 1rem;
  text-align: center; position: relative;
}}
.stat-item::after {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: var(--primary);
}}
.stat-val {{
  font-size: 1.9rem; font-weight: 800; color: var(--text);
  line-height: 1; letter-spacing: -1px;
}}
.stat-val b {{ color: var(--primary); }}
.stat-lbl {{
  font-size: 0.72rem; font-weight: 600; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.14em; margin-top: 0.4rem;
}}

/* ── Section header ── */
.sec-head {{
  display: flex; align-items: center; gap: 1rem;
  margin: 2.5rem 0 1.1rem;
}}
.sec-title {{
  font-size: 1rem; font-weight: 800; color: var(--text);
  text-transform: uppercase; letter-spacing: 0.1em; white-space: nowrap;
}}
.sec-title b {{ color: var(--primary); }}
.sec-line {{ flex: 1; height: 1px; background: var(--border); }}
.sec-count {{
  font-size: 0.62rem; font-weight: 600; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.1em;
  border: 1px solid var(--border); padding: 0.18rem 0.55rem; border-radius: 3px;
}}

/* ── Carousel ── */
.carousel-wrap {{
  overflow-x: auto; overflow-y: visible;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin; scrollbar-color: var(--primary) var(--surface);
  padding-bottom: 6px; margin-bottom: 0.25rem;
}}
.carousel-wrap::-webkit-scrollbar {{ height: 3px; }}
.carousel-wrap::-webkit-scrollbar-track {{ background: var(--surface); }}
.carousel-wrap::-webkit-scrollbar-thumb {{ background: var(--primary); border-radius: 2px; }}
.carousel {{ display: flex; gap: 10px; width: max-content; padding: 2px 2px 4px; }}
.carousel a {{ flex-shrink: 0; }}
.c-card {{
  width: 160px; background: var(--card); border: 1px solid var(--border);
  border-radius: 8px; overflow: hidden; cursor: pointer;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}}
.c-card:hover {{
  border-color: var(--primary); transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}}
.c-poster-wrap {{
  height: 240px; position: relative; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
}}
.c-poster-img {{
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; object-position: top; transition: transform 0.3s;
}}
.c-card:hover .c-poster-img {{ transform: scale(1.06); }}
.c-poster-init {{
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 2.5rem; font-weight: 900;
  color: rgba(255,255,255,0.1); letter-spacing: -2px; pointer-events: none;
}}
.c-overlay {{
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0) 60%);
  display: flex; align-items: flex-end; justify-content: center;
  padding-bottom: 0.7rem; opacity: 0; transition: opacity 0.2s;
}}
.c-card:hover .c-overlay {{ opacity: 1; }}
.c-rating {{ font-size: 0.85rem; font-weight: 800; color: var(--accent); }}
.c-info {{ padding: 0.6rem 0.8rem; }}
.c-title {{
  font-size: 0.82rem; font-weight: 700; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  margin-bottom: 0.2rem;
}}
.c-meta {{
  font-size: 0.70rem; color: var(--muted);
  display: flex; justify-content: space-between;
}}
.c-meta-score {{ color: var(--accent); font-weight: 700; }}

/* ── Skeleton carousel ── */
.sk-card {{
  width: 160px; flex-shrink: 0; background: var(--card);
  border: 1px solid var(--border); border-radius: 8px; overflow: hidden;
}}
.sk-poster {{ height: 240px; }}
.sk-body {{ padding: 0.6rem 0.8rem; }}
.sk-line {{ height: 10px; border-radius: 2px; margin-bottom: 6px; }}

/* ── Compact hover-overlay recommendation grid ── */
.nf-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 14px; margin-top: 1rem;
}}
.nf-card {{
  position: relative; border-radius: 8px; overflow: hidden;
  cursor: pointer; aspect-ratio: 2/3; background: var(--card2);
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  transition: transform 0.22s cubic-bezier(0.4,0,0.2,1), box-shadow 0.22s;
}}
.nf-card:hover {{
  transform: scale(1.04);
  box-shadow: 0 16px 50px rgba(0,0,0,0.55);
  z-index: 10;
}}
.nf-poster {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.nf-poster-img {{
  width: 100%; height: 100%;
  object-fit: cover; object-position: top; transition: transform 0.3s;
}}
.nf-card:hover .nf-poster-img {{ transform: scale(1.05); }}
.nf-poster-init {{
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 3rem; font-weight: 900; color: rgba(255,255,255,0.08);
  pointer-events: none;
}}
.nf-rank-badge {{
  position: absolute; top: 8px; left: 8px; z-index: 5;
  background: var(--primary); color: #fff;
  font-size: 0.76rem; font-weight: 800;
  padding: 0.22rem 0.52rem; border-radius: 3px; letter-spacing: 0.03em;
}}
.nf-rating-badge {{
  position: absolute; top: 8px; right: 8px; z-index: 5;
  background: rgba(0,0,0,0.75); color: var(--accent);
  font-size: 0.76rem; font-weight: 700;
  padding: 0.22rem 0.52rem; border-radius: 3px;
  display: flex; align-items: center; gap: 3px;
}}
.nf-hover-overlay {{
  position: absolute; bottom: 0; left: 0; right: 0; z-index: 4;
  border-radius: 0 0 8px 8px;
  background: linear-gradient(
    to top, rgba(0,0,0,0.97) 0%, rgba(0,0,0,0.88) 55%, rgba(0,0,0,0.0) 100%
  );
  padding: 3rem 1rem 0.9rem;
  transform: translateY(100%);
  transition: transform 0.26s cubic-bezier(0.4,0,0.2,1);
}}
.nf-card:hover .nf-hover-overlay {{ transform: translateY(0); }}
.nf-ov-title {{
  font-size: 1.02rem; font-weight: 800; color: #fff;
  line-height: 1.2; margin-bottom: 0.22rem;
}}
.nf-ov-meta {{
  font-size: 0.75rem; color: rgba(255,255,255,0.65); margin-bottom: 0.38rem;
}}
.nf-ov-genres {{
  display: flex; flex-wrap: wrap; gap: 3px; margin-bottom: 0.4rem;
}}
.g-pill {{
  background: rgba(255,255,255,0.13); border: 1px solid rgba(255,255,255,0.22);
  color: rgba(255,255,255,0.88);
  padding: 0.1rem 0.4rem; border-radius: 3px;
  font-size: 0.58rem; font-weight: 600; letter-spacing: 0.02em;
}}
.nf-ov-sim {{
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 0.2rem;
}}
.sim-lbl {{
  font-size: 0.58rem; color: rgba(255,255,255,0.55);
  text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;
}}
.sim-pct {{ font-size: 0.65rem; font-weight: 700; color: var(--primary); }}
.sim-bg {{
  background: rgba(255,255,255,0.15); border-radius: 2px; height: 2px;
  margin-bottom: 0.55rem;
}}
.sim-fill {{ background: var(--primary); border-radius: 2px; height: 2px; transition: width 0.5s; }}
.nf-ov-btns {{ display: flex; gap: 6px; }}
.btn-primary {{
  flex: 1; background: var(--primary); color: #fff;
  border: none; border-radius: 3px; padding: 0.32rem;
  font-size: 0.70rem; font-weight: 700; letter-spacing: 0.03em;
  text-align: center; text-decoration: none; display: block;
  cursor: pointer; transition: background 0.15s;
}}
.btn-primary:hover {{ background: var(--primary-d); color: #fff; }}
.btn-ghost {{
  background: transparent; color: rgba(255,255,255,0.7);
  border: 1px solid rgba(255,255,255,0.3); border-radius: 3px;
  padding: 0.32rem 0.55rem;
  font-size: 0.70rem; font-weight: 600;
  text-decoration: none; display: block; cursor: pointer;
  transition: all 0.15s; text-align: center;
}}
.btn-ghost:hover {{ border-color: var(--primary); color: var(--primary); }}

/* ── Dashboard metric band ── */
.dash-band {{
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 1px; background: var(--border);
  border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden; margin-bottom: 2rem;
}}
.dash-metric {{ background: var(--card); padding: 1.5rem 1.2rem; position: relative; }}
.dash-metric::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0;
  height: 3px; background: var(--primary);
}}
.dash-val {{
  font-size: 2.1rem; font-weight: 800; color: var(--text);
  line-height: 1; letter-spacing: -1px; margin-bottom: 0.35rem;
}}
.dash-val b {{ color: var(--primary); }}
.dash-lbl {{
  font-size: 0.72rem; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.14em;
}}
.dash-sub {{ font-size: 0.76rem; color: var(--dim); margin-top: 0.35rem; line-height: 1.45; }}

/* ── Info / algo box ── */
.info-box {{
  background: rgba(128,128,128,0.07);
  border-left: 3px solid var(--primary);
  border-radius: 0 4px 4px 0;
  padding: 0.9rem 1.2rem;
  font-size: 0.88rem; color: var(--muted);
  margin: 1rem 0; line-height: 1.75;
}}
.info-box strong {{ color: var(--text); font-weight: 700; }}
.info-box code {{
  background: var(--surface); color: var(--primary);
  padding: 0.12rem 0.38rem; border-radius: 3px;
  font-family: 'JetBrains Mono', monospace; font-size: 0.88rem;
}}

/* ── Form box ── */
.fbox {{
  background: var(--card); border: 1px solid var(--border);
  border-radius: 8px; padding: 1.5rem 2rem 1.8rem; margin-bottom: 1.5rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.12);
}}
.fbox-title {{
  font-size: 0.76rem; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.18em; margin-bottom: 1.2rem;
}}

/* ── Page title ── */
.page-title {{
  font-size: 2.3rem; font-weight: 800; color: var(--text);
  letter-spacing: -1px; line-height: 1; margin-bottom: 0.22rem;
}}
.page-title b {{ color: var(--primary); }}
.page-sub {{
  font-size: 0.88rem; color: var(--muted); margin-bottom: 1.5rem; line-height: 1.6;
}}

/* ── Recommend page headline ── */
.rec-headline {{
  font-size: 2.6rem; font-weight: 800; color: var(--text);
  letter-spacing: -1.5px; line-height: 1.05; margin: 1.5rem 0 0.4rem;
}}
.rec-headline span {{ color: var(--primary); }}
.rec-sub {{
  font-size: 0.92rem; color: var(--muted);
  margin-bottom: 1.8rem; line-height: 1.65;
}}

/* ── Empty state ── */
.empty-state {{ text-align: center; padding: 5rem 2rem; }}
.empty-icon {{
  font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.22; color: var(--primary);
}}
.empty-title {{
  font-size: 1.15rem; font-weight: 800; color: var(--text);
  text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.55rem;
}}
.empty-sub {{ font-size: 0.88rem; color: var(--muted); line-height: 1.65; }}

/* ── Pipeline steps ── */
.pipe-grid {{
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 1px; background: var(--border);
  border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden; margin: 1rem 0 2rem;
}}
.pipe-step {{ background: var(--card); padding: 1.1rem; }}
.pipe-n {{
  font-size: 1.9rem; font-weight: 900; color: var(--border);
  line-height: 1; margin-bottom: 0.3rem;
}}
.pipe-t {{ font-size: 0.82rem; font-weight: 700; color: var(--text); margin-bottom: 0.22rem; }}
.pipe-d {{ font-size: 0.73rem; color: var(--muted); line-height: 1.5; }}

/* ── Formula block ── */
.formula {{
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 4px; padding: 0.8rem 1.15rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem; color: var(--primary); margin: 0.5rem 0;
  overflow-x: auto;
}}

/* ══════════════════════════════════════════════════════════════
   RESPONSIVE BREAKPOINTS
   ══════════════════════════════════════════════════════════════ */

/* ── Tablet (≤ 960px) ── */
@media (max-width: 960px) {{
  .main .block-container {{ padding: 0.75rem 1.5rem 3rem; }}

  .hero {{ min-height: 340px; }}
  .hero-trailer {{ display: none; }}
  .hero-title {{ font-size: 2.8rem; letter-spacing: -1px; }}
  .hero-content {{ padding: 2rem 2rem; }}

  .stat-band {{ grid-template-columns: repeat(2, 1fr); }}
  .dash-band {{ grid-template-columns: repeat(2, 1fr); }}
  .pipe-grid {{ grid-template-columns: repeat(2, 1fr); }}

  .rec-headline {{ font-size: 2rem; letter-spacing: -0.8px; }}
  .page-title {{ font-size: 1.9rem; }}
  .dash-val {{ font-size: 1.7rem; }}
  .stat-val {{ font-size: 1.6rem; }}

  .marquee-wrap {{ margin: 0 -1.5rem 2rem; }}

  .nf-grid {{ grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }}
}}

/* ── Mobile (≤ 640px) ── */
@media (max-width: 640px) {{
  .main .block-container {{ padding: 0.5rem 0.75rem 2.5rem; }}

  /* Navbar */
  div[data-testid="stHorizontalBlock"]:first-of-type {{
    padding: 0.4rem 0.75rem !important;
    flex-wrap: nowrap !important;
  }}
  div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stRadio"] label {{
    font-size: 0.78rem !important;
    padding: 0.38rem 0.55rem 0.32rem !important;
    letter-spacing: 0 !important;
  }}

  /* Stack all non-navbar Streamlit columns */
  [data-testid="stHorizontalBlock"]:not(:first-of-type) {{
    flex-wrap: wrap !important;
  }}
  [data-testid="stHorizontalBlock"]:not(:first-of-type) > [data-testid="stVerticalBlock"] {{
    min-width: 100% !important;
    width: 100% !important;
  }}

  /* Hero */
  .hero {{ min-height: 260px; border-radius: 6px; }}
  .hero-trailer {{ display: none; }}
  .hero-content {{ padding: 1.5rem 1.25rem; max-width: 100%; }}
  .hero-gradient {{
    background: linear-gradient(
      to top, rgba(5,8,24,0.98) 0%, rgba(5,8,24,0.85) 55%, rgba(5,8,24,0.3) 100%
    );
  }}
  .hero-title {{ font-size: 2rem; letter-spacing: -0.5px; line-height: 1.05; }}
  .hero-tagline {{ font-size: 0.82rem; }}
  .hero-desc {{ font-size: 0.8rem; margin-bottom: 1rem; }}
  .hero-tag {{ font-size: 0.6rem; }}
  .hero-actions {{ gap: 0.5rem; }}
  .hero-btn {{ font-size: 0.8rem; padding: 0.5rem 1rem; }}
  .hero-badge, .hero-badge-muted {{ font-size: 0.74rem; padding: 0.35rem 0.65rem; }}

  /* Stat band */
  .stat-band {{ grid-template-columns: repeat(2, 1fr); }}
  .stat-val {{ font-size: 1.45rem; }}
  .stat-lbl {{ font-size: 0.62rem; }}

  /* Marquee */
  .marquee-wrap {{ margin: 0 -0.75rem 1.5rem; height: 140px; }}
  .marquee-poster {{ width: 90px; height: 140px; }}

  /* Section header */
  .sec-title {{ font-size: 0.88rem; }}
  .sec-head {{ margin: 1.8rem 0 0.8rem; gap: 0.6rem; }}

  /* Carousel cards */
  .c-card {{ width: 130px; }}
  .c-poster-wrap {{ height: 195px; }}
  .sk-card {{ width: 130px; }}
  .sk-poster {{ height: 195px; }}

  /* Recommendation grid */
  .nf-grid {{ grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 8px; }}
  .nf-ov-title {{ font-size: 0.88rem; }}

  /* Dashboard */
  .dash-band {{ grid-template-columns: repeat(2, 1fr); }}
  .dash-val {{ font-size: 1.5rem; }}
  .dash-lbl {{ font-size: 0.65rem; }}
  .dash-sub {{ font-size: 0.7rem; }}

  /* Pipeline */
  .pipe-grid {{ grid-template-columns: repeat(2, 1fr); }}

  /* Typography */
  .rec-headline {{ font-size: 1.65rem; letter-spacing: -0.5px; margin: 1rem 0 0.3rem; }}
  .rec-sub {{ font-size: 0.8rem; margin-bottom: 1.2rem; }}
  .page-title {{ font-size: 1.55rem; letter-spacing: -0.5px; }}
  .page-sub {{ font-size: 0.78rem; }}
  .info-box {{ font-size: 0.8rem; padding: 0.75rem 1rem; }}
  .formula {{ font-size: 0.75rem; padding: 0.65rem 0.85rem; }}
  .fbox {{ padding: 1rem 1rem 1.2rem; }}
  .fbox-title {{ font-size: 0.68rem; }}

  /* Empty state */
  .empty-state {{ padding: 3rem 1rem; }}
}}

/* ── Small mobile (≤ 400px) ── */
@media (max-width: 400px) {{
  .hero-title {{ font-size: 1.65rem; }}
  .nf-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .stat-band {{ grid-template-columns: repeat(2, 1fr); }}
  .dash-band {{ grid-template-columns: repeat(2, 1fr); }}
  .c-card {{ width: 110px; }}
  .c-poster-wrap {{ height: 165px; }}
  .sk-card {{ width: 110px; }}
  .sk-poster {{ height: 165px; }}
}}
</style>
""", unsafe_allow_html=True)
