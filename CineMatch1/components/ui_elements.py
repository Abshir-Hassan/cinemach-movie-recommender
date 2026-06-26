"""
Consolidated UI element library (Single Responsibility per function).
All functions return HTML strings for st.markdown(unsafe_allow_html=True).
Poster images: TMDB CDN — loads from cache/poster_paths.csv (all 7,679 films)
with fallback to hardcoded POSTER_MAP, then warm gradient art.
"""
from __future__ import annotations
import os
import streamlit as st
import pandas as pd

from core.constants import (
    GENRE_BG, GENRE_BG_DARK, FEATURED,
    POSTER_MAP, TMDB_IMG_BASE, TMDB_IMG_ORIG,
    TOTAL_RATINGS, TOTAL_MOVIES, TOTAL_USERS, AVG_RATING,
    ACTIVE_USERS, POPULAR_MOVIES, SAMPLE_RATINGS, YEAR_SPAN,
    CACHE_DIR,
)


@st.cache_resource(show_spinner=False)
def _load_runtime_poster_map() -> dict[int, str]:
    """Load poster_paths.csv once per app process (Streamlit resource cache)."""
    csv_path = os.path.join(CACHE_DIR, "poster_paths.csv")
    if not os.path.exists(csv_path):
        return {}
    try:
        df = pd.read_csv(csv_path)
        df = df.dropna(subset=["poster_path"])
        df = df[df["poster_path"].astype(str).str.strip() != ""]
        return dict(zip(df["movieId"].astype(int), df["poster_path"].astype(str)))
    except Exception:
        return {}

# ── SVG icon tokens (no external dependencies) ────────────────────────────────

_PLAY_SVG = (
    '<svg viewBox="0 0 24 24" fill="currentColor" width="100%" height="100%">'
    '<path d="M8 5v14l11-7z"/></svg>'
)
_STAR_SVG = (
    '<svg viewBox="0 0 24 24" fill="currentColor" width="13" height="13">'
    '<path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 '
    '8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'
)


# ── Poster helpers ────────────────────────────────────────────────────────────

def _poster_bg(genres_str: str, dark_mode: bool = False) -> str:
    table = GENRE_BG_DARK if dark_mode else GENRE_BG
    for g in str(genres_str).split("|"):
        if g.strip() in table:
            return table[g.strip()]
    return "#111111" if dark_mode else "#eaddcf"


def _initials(title: str) -> str:
    words = title.replace(",", "").split()[:2]
    return "".join(w[0].upper() for w in words if w)[:2]


def _poster_url(movie_id: int, size: str = TMDB_IMG_BASE) -> str:
    mid  = int(movie_id)
    # CSV has fresh TMDB API paths — always prefer over stale hardcoded map
    path = _load_runtime_poster_map().get(mid) or POSTER_MAP.get(mid, "")
    return f"{size}{path}" if path else ""


# ── Hero section ──────────────────────────────────────────────────────────────

_BTN_PLAY_SVG = (
    '<svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16" '
    'style="flex-shrink:0">'
    '<path d="M8 5v14l11-7z"/></svg>'
)


def render_hero() -> str:
    f          = FEATURED
    genres_str = " · ".join(f["genres"])
    backdrop   = _poster_url(230307, TMDB_IMG_ORIG)   # Oppenheimer
    bg_img     = (
        f'<img class="hero-bg-img" src="{backdrop}" alt="" loading="eager" '
        f'onerror="this.style.display=\'none\'">'
        if backdrop else ""
    )
    return f"""
<div class="hero">
  <div class="hero-backdrop">{bg_img}</div>
  <div class="hero-gradient"></div>
  <div class="hero-trailer">
    <div class="hero-play-circle">{_PLAY_SVG}</div>
    <span class="hero-trailer-lbl">Fragman</span>
  </div>
  <div class="hero-content">
    <div class="hero-tag">One Cikan Film</div>
    <div class="hero-title">{f["title"].upper()}</div>
    <div class="hero-tagline">{f["tagline"]}</div>
    <div class="hero-desc">{f["description"]}</div>
    <div class="hero-actions">
      <a class="hero-btn" href="{f["imdb_url"]}" target="_blank">
        {_BTN_PLAY_SVG} Hemen Izle
      </a>
      <span class="hero-badge">{_STAR_SVG} {f["rating"]} &nbsp;·&nbsp; {f["votes"]} puan</span>
      <span class="hero-badge-muted">{f["year"]} &nbsp;·&nbsp; {genres_str}</span>
    </div>
  </div>
</div>"""


# ── Stat band ─────────────────────────────────────────────────────────────────

def render_stat_band() -> str:
    return f"""
<div class="stat-band">
  <div class="stat-item">
    <div class="stat-val">32<b>M+</b></div>
    <div class="stat-lbl">Toplam Puanlama</div>
  </div>
  <div class="stat-item">
    <div class="stat-val"><b>{TOTAL_MOVIES:,}</b></div>
    <div class="stat-lbl">Film</div>
  </div>
  <div class="stat-item">
    <div class="stat-val"><b>{TOTAL_USERS:,}</b></div>
    <div class="stat-lbl">Kullanici</div>
  </div>
  <div class="stat-item">
    <div class="stat-val"><b>{AVG_RATING}</b></div>
    <div class="stat-lbl">Ort. Puan / 5.0</div>
  </div>
</div>"""


# ── Section header ────────────────────────────────────────────────────────────

def section_header(left: str, highlight: str, count: str | None = None) -> str:
    cnt = f'<div class="sec-count">{count}</div>' if count else ""
    return (
        f'<div class="sec-head">'
        f'<div class="sec-title">{left} <b>{highlight}</b></div>'
        f'<div class="sec-line"></div>{cnt}'
        f"</div>"
    )


# ── Carousel card ─────────────────────────────────────────────────────────────

def carousel_card(
    movie_id: int,
    title: str,
    year: int | str,
    avg_rating: float,
    genres: str,
    imdb_url: str = "",
    tmdb_url: str = "",
    **_,
) -> str:
    bg     = _poster_bg(genres)
    ini    = _initials(title)
    short  = (title[:18] + "…") if len(title) > 18 else title
    genre1 = str(genres).split("|")[0]
    poster = _poster_url(movie_id)
    img_tag = (
        f'<img class="c-poster-img" src="{poster}" '
        f'loading="lazy" onerror="this.remove()" alt="">'
        if poster else ""
    )
    href = imdb_url or tmdb_url or "#"
    target = 'target="_blank"' if href != "#" else ""
    return f"""
<a href="{href}" {target} style="text-decoration:none;color:inherit;display:block;flex-shrink:0">
<div class="c-card" style="width:160px">
  <div class="c-poster-wrap" style="background:{bg}">
    {img_tag}
    <div class="c-poster-init">{ini}</div>
    <div class="c-overlay">
      <div class="c-rating">{_STAR_SVG} {avg_rating:.2f}</div>
    </div>
  </div>
  <div class="c-info">
    <div class="c-title">{short}</div>
    <div class="c-meta">
      <span>{genre1}</span>
      <span class="c-meta-score">{year}</span>
    </div>
  </div>
</div>
</a>"""


def build_carousel(films: list[dict], wrap_id: str = "c") -> str:
    cards = "".join(carousel_card(**f) for f in films)
    return (
        f'<div class="carousel-wrap" id="cw-{wrap_id}">'
        f'<div class="carousel">{cards}</div>'
        f"</div>"
    )


# ── Marquee strip ─────────────────────────────────────────────────────────────

def render_marquee(films: list[dict]) -> str:
    """Scrolling poster strip — uses top films, duplicated for seamless loop."""
    posters = []
    for f in films:
        url = _poster_url(int(f.get("movie_id", 0)))
        if url:
            posters.append(
                f'<div class="marquee-poster">'
                f'<img src="{url}" loading="lazy" onerror="this.parentElement.remove()" alt="">'
                f'</div>'
            )
    if not posters:
        return ""
    strip = "".join(posters)
    return (
        f'<div class="marquee-wrap">'
        f'<div class="marquee-track">{strip}{strip}</div>'
        f'</div>'
    )


# ── Skeleton carousel ─────────────────────────────────────────────────────────

def skeleton_carousel(n: int = 8) -> str:
    sk = (
        '<div class="sk-card">'
        '<div class="sk-poster skeleton"></div>'
        '<div class="sk-body">'
        '<div class="sk-line skeleton" style="width:78%"></div>'
        '<div class="sk-line skeleton" style="width:52%"></div>'
        "</div></div>"
    ) * n
    return (
        '<div class="carousel-wrap">'
        f'<div class="carousel">{sk}</div>'
        "</div>"
    )


# ── Compact hover-overlay recommendation card ─────────────────────────────────

def nf_card(
    rank: int,
    movie_id: int,
    title: str,
    year: int | str,
    avg_rating: float,
    genres: str,
    num_ratings: int,
    knn_sim: float,
    bayesian_score: float,
    imdb_url: str = "",
    tmdb_url: str = "",
    liked_film: str = "",
    **_,
) -> str:
    bg      = _poster_bg(genres, dark_mode=True)
    ini     = _initials(title)
    sim_pct = max(5, int(knn_sim * 100))
    poster  = _poster_url(movie_id)
    img_tag = (
        f'<img class="nf-poster-img" src="{poster}" '
        f'loading="lazy" onerror="this.remove()" alt="">'
        if poster else ""
    )
    genres_h = "".join(
        f'<span class="g-pill">{g.strip()}</span>'
        for g in str(genres).split("|")[:3]
        if g.strip() and g.strip() != "(no genres listed)"
    )
    card_url = imdb_url or tmdb_url
    onclick  = f'onclick="window.open(\'{card_url}\',\'_blank\')"' if card_url else ""
    imdb_btn = (
        f'<a class="btn-primary" href="{imdb_url}" target="_blank" onclick="event.stopPropagation()">IMDb</a>'
        if imdb_url
        else '<span class="btn-primary" style="opacity:.35;cursor:default">IMDb Yok</span>'
    )
    tmdb_btn = (
        f'<a class="btn-ghost" href="{tmdb_url}" target="_blank" onclick="event.stopPropagation()">TMDB</a>'
        if tmdb_url else ""
    )
    return f"""
<div class="nf-card" {onclick}>
  <div class="nf-poster" style="background:{bg}">
    {img_tag}
    <div class="nf-poster-init">{ini}</div>
  </div>
  <div class="nf-rank-badge">#{rank:02d}</div>
  <div class="nf-rating-badge">{_STAR_SVG} {avg_rating:.2f}</div>
  <div class="nf-hover-overlay">
    <div class="nf-ov-title">{title[:42]}</div>
    <div class="nf-ov-meta">{year} &nbsp;·&nbsp; {int(num_ratings):,} puan</div>
    <div class="nf-ov-genres">{genres_h}</div>
    <div class="nf-ov-sim">
      <span class="sim-lbl">KNN Benzerlik</span>
      <span class="sim-pct">%{sim_pct}</span>
    </div>
    <div class="sim-bg"><div class="sim-fill" style="width:{sim_pct}%"></div></div>
    <div class="nf-ov-btns">{imdb_btn}{tmdb_btn}</div>
  </div>
</div>"""


def nf_grid(cards_html: str) -> str:
    return f'<div class="nf-grid">{cards_html}</div>'


# ── Sidebar blocks ────────────────────────────────────────────────────────────

def sidebar_logo() -> str:
    return """
<div style="text-align:center;padding:2rem 0 2.5rem;border-bottom:1px solid #d9c9b5">
  <div style="font-family:'Inter',sans-serif;font-size:1.8rem;font-weight:900;
              color:#8c7851;letter-spacing:3px;line-height:1">
    CINE<span style="color:#020826">MATCH</span>
  </div>
  <div style="font-size:0.55rem;color:#a09070;letter-spacing:0.28em;
              text-transform:uppercase;margin-top:0.4rem;font-weight:700">
    Film Oneri Sistemi
  </div>
</div>"""


def sidebar_info() -> str:
    return f"""
<div style="border-top:1px solid #d9c9b5;margin:1rem 0;padding-top:1rem">
  <div style="font-size:0.58rem;color:#a09070;letter-spacing:0.12em;font-weight:700;
              text-transform:uppercase;margin-bottom:0.7rem">Veri Seti</div>
  <div style="font-size:0.68rem;color:#716040;line-height:2.1;font-weight:600">
    MovieLens ml-32m<br>
    {TOTAL_RATINGS:,} Puanlama<br>
    {TOTAL_MOVIES:,} Film<br>
    {TOTAL_USERS:,} Kullanici<br>
    {YEAR_SPAN}
  </div>
</div>
<div style="border-top:1px solid #d9c9b5;margin:1rem 0;padding-top:1rem">
  <div style="font-size:0.58rem;color:#a09070;letter-spacing:0.12em;font-weight:700;
              text-transform:uppercase;margin-bottom:0.7rem">Algoritma</div>
  <div style="font-size:0.68rem;color:#716040;line-height:2.1;font-weight:600">
    KNN (K=20)<br>
    Cosine Similarity<br>
    Bayesian Scoring<br>
    SciPy Sparse CSR<br>
    Scikit-learn
  </div>
</div>"""


# ── Info boxes ────────────────────────────────────────────────────────────────

def info_box(html: str) -> str:
    return f'<div class="info-box">{html}</div>'


def algo_info(has_knn: bool, n_results: int | None = None) -> str:
    mode   = "KNN + Bayesian Hibrit" if has_knn else "Bayesian Siralama (Demo)"
    detail = (
        "Kullanici-Film matrisi (<code>7702×31204</code>, seyreklik %98.02) "
        "SciPy CSR formatindadir. KNN <code>metric='cosine'</code>, "
        "<code>n_neighbors=20</code>. "
        "Nihai skor: <code>0.65×bayesian + 0.35×knn_sim</code>"
    )
    res = (
        f"<br><strong>&#10003; {n_results} sonuc listelendi.</strong>"
        if n_results is not None else ""
    )
    return info_box(f"<strong>Algoritma: {mode}</strong><br>{detail}{res}")


# ── Formula block ─────────────────────────────────────────────────────────────

def formula(expr: str) -> str:
    return f'<div class="formula">{expr}</div>'


# ── Tech chips ────────────────────────────────────────────────────────────────

def tech_chips() -> str:
    names = [
        "Python 3.x", "Pandas", "Scikit-learn",
        "SciPy", "NumPy", "Streamlit", "Plotly", "IMDb",
    ]
    html = ""
    for name in names:
        html += (
            f'<span style="display:inline-block;background:var(--card);'
            f'border:1px solid var(--border);border-radius:4px;padding:0.35rem 0.85rem;'
            f'font-size:0.78rem;color:var(--text);font-weight:600;margin:0.22rem;'
            f'font-family:\'Manrope\',sans-serif;letter-spacing:0.02em">'
            f'{name}</span>'
        )
    return html
