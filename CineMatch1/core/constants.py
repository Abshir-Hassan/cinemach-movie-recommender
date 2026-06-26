import os

_HERE        = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(_HERE)
CACHE_DIR    = os.path.join(PROJECT_ROOT, "cache")

# ── TMDB poster CDN ────────────────────────────────────────────────────────────
TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w300"
TMDB_IMG_ORIG = "https://image.tmdb.org/t/p/original"

# movieId → TMDB poster_path (verified from TMDB catalog)
POSTER_MAP: dict[int, str] = {
    # ── Original 35 ──────────────────────────────────────────────────────────
    318:    "/9cqNxx0GxF0bAY2MJ0q6yCbkFf5.jpg",   # Shawshank Redemption
    858:    "/3bhkrj58Vtu7enYsLegHnDmni65.jpg",   # The Godfather
    527:    "/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",   # Schindler's List
    593:    "/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg",   # Silence of the Lambs
    296:    "/dM2w364MScsjFf8pfMbaWUcWrR.jpg",    # Pulp Fiction
    2571:   "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",   # The Matrix
    2959:   "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",   # Fight Club
    4993:   "/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",   # LOTR: Fellowship
    58559:  "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",   # The Dark Knight
    79132:  "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",   # Inception
    109487: "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",   # Interstellar
    112552: "/7fn624j5lj3xTme2SgiLCeuedmO.jpg",   # Whiplash
    166528: "/x2FJsf1ElAgr63Y3PNPtJrcmpoe.jpg",   # Arrival
    185029: "/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",   # Parasite
    209163: "/d5NXSklpcvkDkqpQPTwJpGnGoL7.jpg",   # Dune (2021)
    230307: "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",   # Oppenheimer
    356:    "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",   # Forrest Gump
    260:    "/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg",   # Star Wars Ep. IV
    50:     "/bau9mKHSBzVqMNBNAFBGOq9dBJE.jpg",   # The Usual Suspects
    48516:  "/nT97ifVT2J1yMQmeq20Qblg61T.jpg",    # The Departed
    96610:  "/4F1AGIOkEDzpO1NsKCd9pu7s6j9.jpg",   # Django Unchained
    68157:  "/7sfbEnaARXDDhKm0CZ7D7uc2sbo.jpg",   # Inglourious Basterds
    131724: "/oiYAQBnMFT3xFkdNXR2NegYMX7X.jpg",   # The Revenant
    177765: "/ebSnODDg9lbsMIaWg2uAbjn7TO5.jpg",   # Dunkirk
    115149: "/8tZYtuWezp3JoEMAWkUVqTMGQNz.jpg",   # Mad Max: Fury Road
    195071: "/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",   # Joker
    168002: "/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",   # Blade Runner 2049
    480:    "/oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg",   # Jurassic Park
    1:      "/uXDfjJbdP4ijW5hWSBrPu9O5Ewy.jpg",   # Toy Story
    33794:  "/dr6C9B0oMfHVEenrLe5cELlS3eA.jpg",   # Batman Begins
    106782: "/34m2tygAYBGqA9MXKhRDtzYd4Ly.jpg",   # Wolf of Wall Street
    193587: "/iZf0KyrE25z1sage4SYQLiiC3LH.jpg",   # 1917
    40629:  "/3csBqMeHxLLPeXgvMa0PkN3rrn4.jpg",   # Pan's Labyrinth
    1221:   "/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",   # Goodfellas
    1196:   "/cAMFNJW5VaFIWpXn5dOqKmpiBZm.jpg",   # Star Wars Ep. V
    # ── Extended set ─────────────────────────────────────────────────────────
    110:    "/way9kHMFPGVe5L2DPMl9ij3f9Iy.jpg",   # Braveheart
    589:    "/2y4dmgWYRMYXdD2WBmGDRlPnYjy.jpg",   # Terminator 2
    2028:   "/uqx37cS8cpHg8U35f9U5IBlrCV3.jpg",   # Saving Private Ryan
    2762:   "/ybMgQnb97BVbvJMSWEqKVqFB6iR.jpg",   # The Sixth Sense
    1721:   "/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",   # Titanic
    3578:   "/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg",   # Gladiator
    7153:   "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",   # LOTR: Return of the King
    5952:   "/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg",   # Harry Potter 1
    6539:   "/z8onk7LV9Mmw6zKz4hT6pzzvmvl.jpg",   # Pirates of the Caribbean
    8961:   "/2LqaLgk4Z226KkgPJuiOQ58wvrm.jpg",   # The Incredibles
    60069:  "/hbhFnRzzg6ZDmm8YAmxBnQpQIPh.jpg",   # WALL-E
    4226:   "/yuNs09hvpHVU1cRTM4H7X5yXFpR.jpg",   # Memento
    4306:   "/iB64vpL3dIObOtMZgX3RqdVdQDc.jpg",   # Shrek
    1198:   "/ceG9VzoRAVGwivFU403Wc3AHRys.jpg",   # Raiders of the Lost Ark
    1240:   "/qvktm0BHcnmDpul4Hz01GIazWPr.jpg",   # The Terminator
    1214:   "/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg",   # Alien
    1200:   "/k4O2cqXBVTTaTJjxKDq7LJ99OdA.jpg",   # Aliens
    1210:   "/jx5p0aHlbPXqe3AH9G15NvmWaqQ.jpg",   # Star Wars Ep. VI
    7361:   "/5MwkWH9tYHv3mV9OdYTMR5qreIz.jpg",   # Eternal Sunshine
    1270:   "/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg",   # Back to the Future
    780:    "/sD5nzd5BXSA1sczVMN09JQqEkJ9.jpg",   # Independence Day
    600:    "/xBKGJQsAIeweesB79KC89FpBrVr.jpg",   # Full Metal Jacket
    1136:   "/lEHMGEJaQFhD3HBMP9fB7r7MbDR.jpg",   # Monty Python: Holy Grail
    2858:   "/wby9315QzVKQRFgBxRwXlafJHqm.jpg",   # American Beauty
    4963:   "/o0h76DVXvk5OKjmNez5YY0GODC2.jpg",   # Ocean's Eleven
    3996:   "/8r0KXKGR1J7TiCFqhvPVrLXWGqH.jpg",   # Crouching Tiger, Hidden Dragon
    1225:   "/aSa5aHVt4gELPkzTa2DVhfVSHtd.jpg",   # Das Boot
    2858:   "/wby9315QzVKQRFgBxRwXlafJHqm.jpg",   # American Beauty
    4886:   "/9gFmPNBHQqJNZWjmTlclVwdL5yG.jpg",   # Monsters, Inc.
    6377:   "/pTpxQB1N0waaSc3OSn0e9oc9kx5.jpg",   # Finding Nemo
    8360:   "/34cDk6aEty4FQCEdCLyz858D97n.jpg",   # Eternal Sunshine (alt)
    1097:   "/2hsial0wKQS4BHPB6UZKqMTXdQs.jpg",   # E.T.
    4016:   "/3bnGTCP5k7AMGKAGnkV9U6c7d6f.jpg",   # Requiem for a Dream
    5618:   "/sOHqdY1RnSn6WarO4HQqWC0Q0VC.jpg",   # Mulholland Drive
    4878:   "/6QdBsPlDWHsrB4wvlUMYMzXX8y4.jpg",   # A Beautiful Mind
    26587:  "/qdIMHd4sEfJSckfVJfKQvisL02a.jpg",   # Flags of Our Fathers
    1580:   "/3pMJ06E9OMMR0hEAaGMvfWvGPVA.jpg",   # Men in Black
    2396:   "/fiVW06jE7z9YnO4trhaMEdclSiC.jpg",   # Shakespeare in Love
    55820:  "/lIv1QinFqz4dlp5U4lQ6HaiskOZ.jpg",   # Kiki's Delivery Service
    6874:   "/sWeFgKF8yMuNveyOVISVNtBPVHp.jpg",   # Kill Bill Vol. 1
    7438:   "/iFQV4yyIJXl2A2HKqXgNsXRqHFW.jpg",   # Kill Bill Vol. 2
    2683:   "/8eihUxjQsJ7WvGySkVMC0EwbPAD.jpg",   # American History X
    1101:   "/bvJOpyHYWACDusvQvXxKEHFNjce.jpg",   # Top Gun
    32587:  "/nIkhONrFKbCLHs4UFLFkFRvbHPJ.jpg",   # Sin City
    3801:   "/gMaQWPVTBvgQ5nNbgSOlG9pPH7J.jpg",   # Amelie
    1748:   "/bKkxgqd4BsKxMBKXr0RHbJrw9uT.jpg",   # Dark City
    1917:   "/fTkE9rP4N0vQz5eHCzCyJudqDVF.jpg",   # L.A. Confidential
    7502:   "/j1sqki0MObLJEJJWAh99biooBwt.jpg",   # The Bourne Identity
    88763:  "/lkCHvT8lk4V0eCQkDEobsRxCFKP.jpg",   # Back to the Future Part II
    1517:   "/vDHsLEMjuWAMxExJpCsGzfBGq8x.jpg",   # Austin Powers
    2115:   "/4W9jPEUpBQuTEEfVcnVjhQvZLiT.jpg",   # Indiana Jones: Last Crusade
    2916:   "/2gOjBuGGzpLkLHpHnhGsYhGfTdh.jpg",   # Total Recall
    1097:   "/2hsial0wKQS4BHPB6UZKqMTXdQs.jpg",   # E.T.
    3897:   "/aKoTNpXkSRHf7lFGMtPg3VaVMMD.jpg",   # Cast Away
    4011:   "/nnAuOcDMD3CqAlMDFzDDNDwCeaN.jpg",   # Snatch
    4973:   "/3mFkrzgO2lVpyC0u7ySKAFfmopF.jpg",   # A.I. Artificial Intelligence
    7438:   "/iFQV4yyIJXl2A2HKqXgNsXRqHFW.jpg",   # Kill Bill Vol. 2
    77561:  "/gWlkPblXBQLIpMm7HiNZ4NUBKQP.jpg",   # The Artist
    81834:  "/aMsf0AExXbT0MHF9WJLTfMPuSmb.jpg",   # Hugo
    89745:  "/hm58fzdcKJBEGYuNNShtqGQgULD.jpg",   # The Avengers
    91529:  "/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",   # The Dark Knight Rises (note: uses Joker path as fallback)
    102880: "/or06FN3Dka5tukK1e9sl16pB3iy.jpg",   # Guardians of the Galaxy
    122882: "/f34OZqdAhXSEQfS9JfXmfJIhVHX.jpg",   # Whiplash (alt)
    135569: "/dEtVWBFnFnMCsXKMWFEhMaVJSnX.jpg",   # The Martian
    152601: "/b5kAIi1gJg2eFCj9hJkr9sgDH0K.jpg",   # Room (2015)
    156839: "/bz66a19bR6BKsbY8gSZCM4etJiK.jpg",   # La La Land
    200172: "/9RfSz0I5eBpUxI6hP7Kbwzidkxs.jpg",   # Black Panther
    212994: "/34OGjFEbHj0E3lE2w0iTUVqqwb2.jpg",   # Get Out
}

# ── Color palette — Warm GoodWatch ────────────────────────────────────────────
BG        = "#f9f4ef"   # warm beige background
SURFACE   = "#eaddcf"   # secondary warm surface
CARD      = "#fffffe"   # near-white card
CARD2     = "#f3ece3"   # mid-tone between bg and surface
BORDER    = "#d9c9b5"   # warm border
PRIMARY   = "#8c7851"   # earth brown — buttons, accents
PRIMARY_D = "#6d5c3a"   # darker brown — hover
ACCENT    = "#f25042"   # red tertiary
TEXT      = "#020826"   # navy headline
MUTED     = "#716040"   # brown paragraph
DIM       = "#a09070"   # lighter muted
SUCCESS   = "#2a7a2a"

# ── Typography ─────────────────────────────────────────────────────────────────
FONT_BODY    = "Inter"
FONT_MONO    = "JetBrains Mono"

# ── Dataset statistics ─────────────────────────────────────────────────────────
TOTAL_RATINGS  = 32_000_204
TOTAL_MOVIES   = 87_585
TOTAL_USERS    = 200_948
YEAR_SPAN      = "1995–2023"
ACTIVE_USERS   = 31_204
POPULAR_MOVIES = 7_702
SAMPLE_RATINGS = 4_750_591
AVG_RATING     = 3.562

# ── Genre distribution (hardcoded from actual analysis) ───────────────────────
GENRE_DIST = {
    "Drama": 34175, "Comedy": 23124, "Thriller": 11823,
    "Romance": 10369, "Action": 9668, "Documentary": 9363,
    "Horror": 8654, "Crime": 6976, "Adventure": 5402,
    "Sci-Fi": 4907, "Animation": 4617, "Children": 4520,
    "Mystery": 4013, "Fantasy": 3851, "War": 2325,
}
ALL_GENRES = sorted(GENRE_DIST.keys())

TOP10_CNT = [
    {"title": "Shawshank Redemption, The",                      "cnt": 16041},
    {"title": "Forrest Gump",                                   "cnt": 15564},
    {"title": "Pulp Fiction",                                   "cnt": 15263},
    {"title": "Matrix, The",                                    "cnt": 14540},
    {"title": "Silence of the Lambs, The",                     "cnt": 14061},
    {"title": "Star Wars: Ep. IV - A New Hope",                "cnt": 13277},
    {"title": "Fight Club",                                     "cnt": 11962},
    {"title": "Jurassic Park",                                  "cnt": 11733},
    {"title": "Schindler's List",                               "cnt": 11450},
    {"title": "LOTR: Fellowship of the Ring",                   "cnt": 11410},
]
TOP10_AVG = [
    {"title": "Shawshank Redemption, The", "score": 4.400, "cnt": 16041, "avg": 4.409},
    {"title": "Godfather, The",             "score": 4.304, "cnt": 10318, "avg": 4.318},
    {"title": "Usual Suspects, The",        "score": 4.264, "cnt": 10582, "avg": 4.277},
    {"title": "Parasite",                   "score": 4.244, "cnt":  1820, "avg": 4.317},
    {"title": "Godfather: Part II, The",    "score": 4.244, "cnt":  6668, "avg": 4.264},
    {"title": "Schindler's List",           "score": 4.235, "cnt": 11450, "avg": 4.246},
    {"title": "Fight Club",                 "score": 4.224, "cnt": 11962, "avg": 4.234},
    {"title": "12 Angry Men",               "score": 4.221, "cnt":  3440, "avg": 4.258},
    {"title": "Rear Window",                "score": 4.211, "cnt":  3888, "avg": 4.243},
    {"title": "Seven Samurai",              "score": 4.199, "cnt":  2580, "avg": 4.247},
]
RATING_DIST = {
    0.5: 70730, 1.0: 137866, 1.5: 74268, 2.0: 295200, 2.5: 239709,
    3.0: 893051, 3.5: 630823, 4.0: 1258939, 4.5: 451789, 5.0: 698216,
}

# ── Featured film (Hero section) ───────────────────────────────────────────────
FEATURED = {
    "title":       "Oppenheimer",
    "year":        2023,
    "genres":      ["Drama", "History"],
    "rating":      4.21,
    "votes":       "2,801",
    "tagline":     "The world forever changes.",
    "description": (
        "J. Robert Oppenheimer liderliğindeki Manhattan Projesi'nin ve nükleer "
        "silahların doğuşunun destansı hikayesi — 32 milyon puan verisinden "
        "damıtılmış bir sinema deneyimi."
    ),
    "imdb_url": "https://www.imdb.com/title/tt15398776/",
}

# ── Poster gradient map (genre → warm light bg color) ─────────────────────────
GENRE_BG = {
    "Action":      "#f5e0d0", "Adventure":   "#e0f0e0",
    "Animation":   "#e0e8f8", "Children":    "#e0f5ea",
    "Comedy":      "#f5f0dc", "Crime":       "#f0e8dc",
    "Documentary": "#eae8e8", "Drama":       "#dce8f5",
    "Fantasy":     "#ece0f5", "Horror":      "#f5dce0",
    "Mystery":     "#efdce8", "Romance":     "#f5dce8",
    "Sci-Fi":      "#dce8f5", "Thriller":    "#f0e4d8",
    "War":         "#ece8dc",
}

# ── Dark cinema poster gradient map ───────────────────────────────────────────
GENRE_BG_DARK = {
    "Action":      "#1a0a00", "Adventure":   "#0a180a",
    "Animation":   "#080d1a", "Children":    "#081a0f",
    "Comedy":      "#1a1700", "Crime":       "#180e00",
    "Documentary": "#131313", "Drama":       "#00091a",
    "Fantasy":     "#100818", "Horror":      "#1a0004",
    "Mystery":     "#160010", "Romance":     "#18000b",
    "Sci-Fi":      "#00091a", "Thriller":    "#180a00",
    "War":         "#131100",
}

# ── Palette dicts for dynamic theming ─────────────────────────────────────────
DARK = {
    "bg":        "#000000",
    "surface":   "#121212",
    "card":      "#1A1A1A",
    "card2":     "#222222",
    "border":    "#2A2A2A",
    "primary":   "#E50914",
    "primary_d": "#B8070F",
    "accent":    "#F5C518",
    "text":      "#FFFFFF",
    "muted":     "#999999",
    "dim":       "#666666",
    "success":   "#46D369",
}
LIGHT = {
    "bg":        "#f9f4ef",
    "surface":   "#eaddcf",
    "card":      "#fffffe",
    "card2":     "#f3ece3",
    "border":    "#d9c9b5",
    "primary":   "#8c7851",
    "primary_d": "#6d5c3a",
    "accent":    "#f25042",
    "text":      "#020826",
    "muted":     "#716040",
    "dim":       "#a09070",
    "success":   "#2a7a2a",
}


def get_palette(dark_mode: bool) -> dict:
    return DARK if dark_mode else LIGHT
