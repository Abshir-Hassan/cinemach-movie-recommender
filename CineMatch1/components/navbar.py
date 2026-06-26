"""Navbar logo HTML component."""
from __future__ import annotations

_FILM_SVG = (
    '<svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22" '
    'style="display:inline-block;vertical-align:middle;margin-right:7px;flex-shrink:0">'
    '<path d="M18 3v2h-2V3H8v2H6V3H4v18h2v-2h2v2h8v-2h2v2h2V3h-2zM8 17H6v-2h2v2zm0-4H6'
    'v-2h2v2zm0-4H6V7h2v2zm10 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"/>'
    '</svg>'
)


def render_navbar_logo(dark_mode: bool) -> str:
    primary = "#E50914" if dark_mode else "#8c7851"
    text    = "#FFFFFF" if dark_mode else "#020826"
    return (
        f'<div style="display:flex;align-items:center;height:100%;padding:0.15rem 0">'
        f'<div style="font-family:Inter,sans-serif;font-size:1.2rem;font-weight:900;'
        f'color:{primary};letter-spacing:2px;line-height:1;'
        f'display:flex;align-items:center;white-space:nowrap">'
        f'<span style="color:{primary}">{_FILM_SVG}</span>'
        f'CINE<span style="color:{text}">MATCH</span>'
        f'</div>'
        f'</div>'
    )
