"""
CineMatch — Pro Streaming Film Oneri Sistemi
Mimari: SOLID + Feature-Based (core / services / components)
"""
import os
import warnings
import streamlit as st
import pandas as pd

warnings.filterwarnings("ignore")

# ── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="CineMatch | Film Oneri Sistemi",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Core ──────────────────────────────────────────────────────────────────────
from core.styles    import inject_css
from core.constants import ALL_GENRES, CACHE_DIR

# ── Services ──────────────────────────────────────────────────────────────────
from services.data_manager import load_movie_stats, load_knn
from services.recommender  import recommend

# ── UI components ─────────────────────────────────────────────────────────────
from components.ui_elements import (
    render_hero, render_stat_band, section_header,
    build_carousel, skeleton_carousel,
    render_marquee,
    nf_card, nf_grid,
    algo_info, formula, tech_chips,
)
from components.navbar import render_navbar_logo

# ── Analytics feature ─────────────────────────────────────────────────────────
from features.analytics import render_dashboard

# ── Session state init ────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark_mode = st.session_state.dark_mode

# ── Inject CSS ───────────────────────────────────────────────────────────────
inject_css(dark_mode)

# ── Data loading ─────────────────────────────────────────────────────────────
with st.spinner("Veri ve model yukleniyor..."):
    ms                       = load_movie_stats()
    knn, sparse_mat, mid2row = load_knn()

yc_path = os.path.join(CACHE_DIR, "year_counts.csv")

# ── Navbar: [logo | nav radio | mode toggle] ──────────────────────────────────
nav_l, nav_m, nav_r = st.columns([1.5, 5, 1])
with nav_l:
    st.markdown(render_navbar_logo(dark_mode), unsafe_allow_html=True)
with nav_m:
    page = st.radio(
        "page_nav",
        options=["Ana Sayfa", "Dashboard", "Film Oner"],
        horizontal=True,
        label_visibility="collapsed",
        key="page_radio",
    )
with nav_r:
    icon = "☀ Acik" if dark_mode else "◑ Koyu"
    if st.button(icon, key="mode_toggle"):
        st.session_state.dark_mode = not dark_mode
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ANA SAYFA
# ══════════════════════════════════════════════════════════════════════════════
if page == "Ana Sayfa":

    st.markdown(render_hero(), unsafe_allow_html=True)

    # ── Marquee strip (scrolling posters between hero and stat band) ──────────
    score_col     = "bayesian_score" if "bayesian_score" in ms.columns else "avg_rating"
    top_marquee   = ms[ms["num_ratings"] >= 200].nlargest(40, score_col)
    marquee_films = [{"movie_id": int(r["movieId"])} for _, r in top_marquee.iterrows()]
    st.markdown(render_marquee(marquee_films), unsafe_allow_html=True)

    st.markdown(render_stat_band(), unsafe_allow_html=True)

    # ── "Sizin Icin" carousel ─────────────────────────────────────────────────
    st.markdown(section_header("SIZIN", "ICIN", "Top 20"), unsafe_allow_html=True)
    ph1 = st.empty()
    ph1.markdown(skeleton_carousel(10), unsafe_allow_html=True)

    top_for_you = ms[ms["num_ratings"] >= 100].nlargest(20, score_col)
    films_for_you = [
        {
            "movie_id":   int(row["movieId"]),
            "title":      str(row["title_clean"]),
            "year":       int(row["year"]) if not pd.isna(row.get("year", float("nan"))) else "?",
            "avg_rating": float(row["avg_rating"]),
            "genres":     str(row["genres"]),
            "imdb_url":   str(row.get("imdb_url", "")),
            "tmdb_url":   (
                f"https://www.themoviedb.org/movie/{int(row['tmdbId'])}"
                if pd.notna(row.get("tmdbId", float("nan"))) and str(row.get("tmdbId", "")).strip()
                else ""
            ),
        }
        for _, row in top_for_you.iterrows()
    ]
    ph1.markdown(build_carousel(films_for_you, "for-you"), unsafe_allow_html=True)

    # ── "Trendler" carousel ───────────────────────────────────────────────────
    st.markdown(section_header("BU HAFTA", "TRENDLER", "Top 20"), unsafe_allow_html=True)
    ph2 = st.empty()
    ph2.markdown(skeleton_carousel(10), unsafe_allow_html=True)

    top_trend = ms.nlargest(20, "num_ratings")
    films_trend = [
        {
            "movie_id":   int(row["movieId"]),
            "title":      str(row["title_clean"]),
            "year":       int(row["year"]) if not pd.isna(row.get("year", float("nan"))) else "?",
            "avg_rating": float(row["avg_rating"]),
            "genres":     str(row["genres"]),
            "imdb_url":   str(row.get("imdb_url", "")),
            "tmdb_url":   (
                f"https://www.themoviedb.org/movie/{int(row['tmdbId'])}"
                if pd.notna(row.get("tmdbId", float("nan"))) and str(row.get("tmdbId", "")).strip()
                else ""
            ),
        }
        for _, row in top_trend.iterrows()
    ]
    ph2.markdown(build_carousel(films_trend, "trends"), unsafe_allow_html=True)

    # ── Proje hakkinda ────────────────────────────────────────────────────────
    st.markdown(section_header("PROJE", "HAKKINDA"), unsafe_allow_html=True)
    p1, p2 = st.columns([3, 2], gap="large")
    with p1:
        st.markdown(
            """
Bu sistem **GroupLens Research** (University of Minnesota) tarafından yayımlanan
**MovieLens ml-32m** veri setini kullanarak gerçek kullanıcı davranışlarından
kişiselleştirilmiş film önerileri üretmektedir.

- **İşbirlikçi Filtreleme** — Benzer kullanıcı örüntülerinden öğrenir
- **Bayesian Ağırlıklama** — Popülerlik yanlılığını ortadan kaldırır
- **Çok Kriterli Filtreleme** — Tür · Puan · Yıl · Beğenilen Film
- **IMDb & TMDB Entegrasyonu** — Her film için platform bağlantısı
- **Modüler Mimari** — SOLID prensiplerine uygun feature-based yapı
"""
        )

    with p2:
        st.markdown(section_header("TEKNOLOJI", "YIGINI"), unsafe_allow_html=True)
        st.markdown(tech_chips(), unsafe_allow_html=True)

    # ── Algoritma detaylari ────────────────────────────────────────────────────
    st.markdown(section_header("ALGORITMA", "DETAYLARI"), unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            formula("cos(A, B) = (A · B) / (||A|| x ||B||)")
            + formula("final_score = 0.65 x bayesian_avg + 0.35 x knn_sim")
            + formula("bayesian_avg = [n/(n+m)] x R + [m/(n+m)] x C"),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
**K=20 seçimi:** K ∈ {5, 10, 15, 20, 30} için 5-katlı çapraz doğrulama
uygulandı. K=20 → RMSE=0.853 (en düşük).

**Bellek optimizasyonu:** 1.8 GB yoğun matris → 12 MB SciPy CSR sparse
→ 150× tasarruf. 7702 film × 31204 kullanıcı, seyreklik %98.02.

**Skor formülü:** Bayesian ortalama düşük oy sayısını cezalandırır (m eşiği),
KNN cosine skoru ise benzer izleyici profilleri arasındaki mesafeyi ölçer.
"""
        )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Dashboard":
    render_dashboard(yc_path)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — FILM ONER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Film Oner":

    st.markdown(
        '<div class="rec-headline">'
        'Ne izlemek istediğini<br>'
        '<span>bize tarif et...</span>'
        '</div>'
        '<div class="rec-sub">'
        'KNN (K=20, Cosine Similarity) + Bayesian Hibrit &nbsp;·&nbsp; '
        'IMDb &amp; TMDB Baglantili Sonuclar'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(algo_info(has_knn=knn is not None), unsafe_allow_html=True)

    # ── Filter form ───────────────────────────────────────────────────────────
    film_opts = ["— Secmek Istemiyorum —"] + sorted(
        ms[ms["num_ratings"] >= 50]["title_clean"].dropna().tolist()
    )

    st.markdown(
        '<div class="fbox"><div class="fbox-title">Oneri Kriterleri</div>',
        unsafe_allow_html=True,
    )
    fc1, fc2 = st.columns([3, 2], gap="large")
    with fc1:
        sel_genres = st.multiselect(
            "Film Turleri (coklu secim)", ALL_GENRES, default=["Drama", "Thriller"]
        )
        liked_film = st.selectbox("Begendiginiz Film (KNN Referansi)", film_opts)
    with fc2:
        min_rat  = st.slider("Minimum Ortalama Puan", 0.5, 5.0, 3.5, 0.5)
        yr_range = st.slider("Film Yili Araligi", 1902, 2023, (1990, 2023))
        n_rec    = st.select_slider("Oneri Sayisi", [5, 10, 15, 20], value=10)
    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button("FILMLERI ONER", use_container_width=True)

    if run:
        liked_mid = None
        if liked_film != "— Secmek Istemiyorum —":
            row = ms[ms["title_clean"] == liked_film]
            if not row.empty:
                liked_mid = int(row.iloc[0]["movieId"])

        with st.spinner("KNN hesaplaniyor..."):
            results = recommend(
                ms, knn, sparse_mat, mid2row,
                genres=sel_genres or None,
                min_rat=min_rat,
                yr0=yr_range[0], yr1=yr_range[1],
                n=n_rec, liked_mid=liked_mid,
            )

        if results.empty:
            st.warning("Secilen kriterlere uygun film bulunamadi. Filtreleri genisletmeyi deneyin.")
        else:
            st.markdown(
                algo_info(has_knn=knn is not None, n_results=len(results)),
                unsafe_allow_html=True,
            )
            st.markdown(
                section_header("ONERILEN", "FILMLER", f"{len(results)} sonuc"),
                unsafe_allow_html=True,
            )
            cards_html = ""
            for i, row in results.iterrows():
                year_val = (
                    int(row["year"]) if not pd.isna(row.get("year", float("nan"))) else "?"
                )
                bayes   = float(row.get("bayesian_score", row["avg_rating"]))
                tmdb_id = row.get("tmdbId", "")
                tmdb_url = (
                    f"https://www.themoviedb.org/movie/{int(tmdb_id)}"
                    if pd.notna(tmdb_id) and str(tmdb_id).strip()
                    else ""
                )
                cards_html += nf_card(
                    rank=i + 1,
                    movie_id=int(row["movieId"]),
                    title=str(row["title_clean"]),
                    year=year_val,
                    avg_rating=float(row["avg_rating"]),
                    genres=str(row["genres"]),
                    num_ratings=int(row["num_ratings"]),
                    knn_sim=float(row.get("knn_sim", 0.45)),
                    bayesian_score=bayes,
                    imdb_url=str(row.get("imdb_url", "")),
                    tmdb_url=tmdb_url,
                    liked_film=liked_film,
                )
            st.markdown(nf_grid(cards_html), unsafe_allow_html=True)

    else:
        st.markdown("""
<div class="empty-state">
  <div class="empty-icon">+</div>
  <div class="empty-title">Kriterlerinizi Belirleyin</div>
  <div class="empty-sub">
    Film turu, minimum puan ve yil araligini secin.<br>
    Isteğe bagli olarak referans film ekleyin.<br>
    Her sonuc kartinda IMDb ve TMDB baglantisi sunulur.
  </div>
</div>
""", unsafe_allow_html=True)
