import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.constants import (
    TOP10_CNT, TOP10_AVG, RATING_DIST, GENRE_DIST,
    TOTAL_RATINGS, TOTAL_MOVIES, TOTAL_USERS, YEAR_SPAN,
    ACTIVE_USERS, POPULAR_MOVIES, SAMPLE_RATINGS, AVG_RATING,
    CACHE_DIR,
    DARK, LIGHT,
)

_ZERO = "rgba(0,0,0,0)"


def _lay(_FC: str, h: int = 300, **kw) -> dict:
    return dict(
        paper_bgcolor=_ZERO, plot_bgcolor=_ZERO,
        font=dict(color=_FC, family="Inter", size=10),
        margin=dict(l=0, r=55, t=10, b=10),
        height=h, **kw,
    )


def _sec(left: str, bold: str) -> str:
    return (
        f'<div class="sec-head">'
        f'<div class="sec-title">{left} <b>{bold}</b></div>'
        f'<div class="sec-line"></div></div>'
    )


def render_dashboard(yc_path: str) -> None:
    dark_mode = st.session_state.get("dark_mode", True)
    p         = DARK if dark_mode else LIGHT
    _FC       = p["text"]
    _MU       = p["muted"]
    PRIMARY   = p["primary"]
    ACCENT    = p["accent"]
    bar_lo    = p["surface"] if dark_mode else "#eaddcf"
    bar_lo2   = p["surface"] if dark_mode else "#f9f0ec"

    st.markdown(
        '<div class="page-title">DATA<b>BOARD</b></div>'
        '<div class="page-sub">MovieLens ml-32m '
        '&middot; 5M satirlik ornekleme '
        '&middot; Gercek istatistikler</div>',
        unsafe_allow_html=True,
    )

    # ── Metric band ──────────────────────────────────────────────────────────
    st.markdown(f"""
<div class="dash-band">
  <div class="dash-metric">
    <div class="dash-val">32<b>M+</b></div>
    <div class="dash-lbl">Toplam Puanlama</div>
    <div class="dash-sub">{TOTAL_RATINGS:,} kayit</div>
  </div>
  <div class="dash-metric">
    <div class="dash-val"><b>{TOTAL_MOVIES:,}</b></div>
    <div class="dash-lbl">Film</div>
    <div class="dash-sub">{POPULAR_MOVIES:,} aktif (&ge;50 puan)</div>
  </div>
  <div class="dash-metric">
    <div class="dash-val"><b>{TOTAL_USERS:,}</b></div>
    <div class="dash-lbl">Kullanici</div>
    <div class="dash-sub">{ACTIVE_USERS:,} aktif (&ge;20 puan)</div>
  </div>
  <div class="dash-metric">
    <div class="dash-val"><b>{AVG_RATING}</b></div>
    <div class="dash-lbl">Ort. Puan / 5.0</div>
    <div class="dash-sub">{YEAR_SPAN} &middot; {SAMPLE_RATINGS:,} ornekleme</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Charts row 1 ─────────────────────────────────────────────────────────
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown(_sec("EN COK", "PUANLANAN"), unsafe_allow_html=True)
        df_c = pd.DataFrame(TOP10_CNT)
        fig  = go.Figure(go.Bar(
            x=df_c["cnt"], y=df_c["title"].str[:32],
            orientation="h",
            marker=dict(
                color=df_c["cnt"],
                colorscale=[[0, bar_lo], [1, PRIMARY]],
                line=dict(width=0),
            ),
            text=df_c["cnt"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(color=_FC, size=9),
        ))
        fig.update_layout(**_lay(_FC))
        fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig.update_yaxes(showgrid=False, tickfont=dict(size=8, color=_FC), autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(_sec("EN YUKSEK", "BAYESIAN PUANLI"), unsafe_allow_html=True)
        df_a = pd.DataFrame(TOP10_AVG)
        fig2 = go.Figure(go.Bar(
            x=df_a["score"], y=df_a["title"].str[:32],
            orientation="h",
            marker=dict(
                color=df_a["score"],
                colorscale=[[0, bar_lo2], [1, ACCENT]],
                line=dict(width=0),
            ),
            text=df_a["score"].round(3),
            textposition="outside",
            textfont=dict(color=_FC, size=9),
        ))
        fig2.update_layout(**_lay(_FC))
        fig2.update_xaxes(showgrid=False, showticklabels=False, zeroline=False, range=[0, 4.7])
        fig2.update_yaxes(showgrid=False, tickfont=dict(size=8, color=_FC), autorange="reversed")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Charts row 2 ─────────────────────────────────────────────────────────
    c3, c4 = st.columns(2, gap="large")

    with c3:
        st.markdown(_sec("PUAN", "DAGILIMI"), unsafe_allow_html=True)
        rx, ry = list(RATING_DIST.keys()), list(RATING_DIST.values())
        bar_mid = "#444444" if dark_mode else "#c4a87a"
        fig3   = go.Figure(go.Bar(
            x=rx, y=ry,
            marker=dict(
                color=ry,
                colorscale=[[0, bar_lo], [0.5, bar_mid], [1, PRIMARY]],
                line=dict(width=0),
            ),
            text=[f"{v:,}" for v in ry],
            textposition="outside",
            textfont=dict(color=_FC, size=8),
        ))
        fig3.update_layout(**_lay(_FC, 240))
        fig3.update_xaxes(
            showgrid=False, tickvals=rx,
            tickfont=dict(color=_MU, size=9),
            title_text="Puan Degeri",
            title_font=dict(color=_MU, size=9),
        )
        fig3.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown(_sec("TUR", "DAGILIMI"), unsafe_allow_html=True)
        gd   = sorted(GENRE_DIST.items(), key=lambda x: x[1])
        fig4 = go.Figure(go.Bar(
            x=[v for _, v in gd], y=[k for k, _ in gd],
            orientation="h",
            marker=dict(
                color=[v for _, v in gd],
                colorscale=[[0, bar_lo], [1, PRIMARY]],
                line=dict(width=0),
            ),
            text=[f"{v:,}" for _, v in gd],
            textposition="outside",
            textfont=dict(color=_FC, size=8),
        ))
        fig4.update_layout(**_lay(_FC, 240))
        fig4.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig4.update_yaxes(showgrid=False, tickfont=dict(size=8, color=_FC))
        st.plotly_chart(fig4, use_container_width=True)

    # ── Year trend ────────────────────────────────────────────────────────────
    if os.path.exists(yc_path):
        st.markdown(_sec("YILA GORE", "FILM SAYISI"), unsafe_allow_html=True)
        yc   = pd.read_csv(yc_path)
        yc   = yc[yc["year"].between(1960, 2023)].dropna()
        fig5 = go.Figure()
        fill_c = "rgba(229,9,20,0.12)" if dark_mode else "rgba(140,120,81,0.1)"
        fig5.add_trace(go.Scatter(
            x=yc["year"], y=yc["movieId"],
            fill="tozeroy",
            fillcolor=fill_c,
            line=dict(color=PRIMARY, width=2),
            mode="lines",
            hovertemplate="<b>%{x:.0f}</b><br>%{y} film<extra></extra>",
        ))
        fig5.update_layout(**_lay(_FC, 180))
        fig5.update_xaxes(showgrid=False, tickfont=dict(color=_MU))
        fig5.update_yaxes(showgrid=False, showticklabels=False)
        st.plotly_chart(fig5, use_container_width=True)

    # ── Pipeline ──────────────────────────────────────────────────────────────
    st.markdown(_sec("VERI", "PIPELINE"), unsafe_allow_html=True)
    steps = [
        ("1", "Ham Veri Yukleme",  "nrows=5M — RAM korumasi"),
        ("2", "Kalite Filtresi",   ">= 50 puan film, >= 20 puan kullanici"),
        ("3", "Temizleme",         "dropna() + drop_duplicates()"),
        ("4", "Ozellik Cikarimi",  "Yil regex, tur split, top-5 etiket"),
        ("5", "Sparse Matris",     "7702x31204 pivot -> CSR (12 MB)"),
        ("6", "KNN Egitimi",       "k=20, cosine, brute, n_jobs=-1"),
        ("7", "Hibrit Skor",       "0.65 x Bayesian + 0.35 x KNN sim"),
        ("8", "Oneri & IMDb",      "Filtrele > Sirala > IMDb linki"),
    ]
    cols = st.columns(4)
    for i, (n, t, d) in enumerate(steps):
        with cols[i % 4]:
            st.markdown(
                f'<div class="pipe-step">'
                f'<div class="pipe-n">{n}</div>'
                f'<div class="pipe-t">{t}</div>'
                f'<div class="pipe-d">{d}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── Before/After table ───────────────────────────────────────────────────
    st.markdown(_sec("TEMIZLEME", "ONCESI / SONRASI"), unsafe_allow_html=True)
    ca, cb, cc = st.columns(3, gap="large")
    with ca:
        st.markdown(
            "**Ham Veri**\n\n"
            "| Metrik | Deger |\n|--------|-------|\n"
            "| Satir | 32,000,204 |\n| Film | 87,585 |\n"
            "| Kullanici | 200,948 |\n| Boyut | ~830 MB |"
        )
    with cb:
        st.markdown(
            "**Uygulanan Islemler**\n\n"
            "1. `nrows=5M` ornekleme\n"
            "2. >= 50 puan filmler\n"
            "3. >= 20 puan kullanicilar\n"
            "4. `drop_duplicates()`\n"
            "5. `merge(movieId)`\n"
            "6. Regex yil cikarimi\n"
            "7. Pipe split tur ayristirma"
        )
    with cc:
        st.markdown(
            "**Temiz Veri**\n\n"
            "| Metrik | Deger |\n|--------|-------|\n"
            "| Satir | 4,750,591 |\n| Film | 7,702 |\n"
            "| Kullanici | 31,204 |\n| RAM | ~340 MB |\n"
            "| Seyreklik | %98.02 |"
        )
