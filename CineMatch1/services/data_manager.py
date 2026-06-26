"""
Data loading and cache management (Single Responsibility).
Handles: movie_stats.csv, KNN model, sparse matrix, index.
All functions are decorated with @st.cache_* for performance.
"""
import os, pickle, warnings
import streamlit as st
import pandas as pd
import numpy as np

from core.constants import CACHE_DIR

warnings.filterwarnings("ignore")


@st.cache_data(show_spinner=False)
def load_movie_stats() -> pd.DataFrame:
    p = os.path.join(CACHE_DIR, "movie_stats.csv")
    if os.path.exists(p):
        df = pd.read_csv(p)
        if "imdb_url" not in df.columns:
            df["imdb_url"] = ""
        if "tmdbId" not in df.columns:
            df["tmdbId"] = float("nan")
        if "title_clean" not in df.columns:
            df["title_clean"] = (
                df["title"].str.replace(r"\s*\(\d{4}\)", "", regex=True).str.strip()
            )
        return df
    # Fallback demo when cache absent (32M dataset not yet processed)
    rows = [
        (318,   "Shawshank Redemption, The (1994)", "Crime|Drama",             1994, 4.409, 16041, "https://www.imdb.com/title/tt0111161/"),
        (858,   "Godfather, The (1972)",             "Crime|Drama",             1972, 4.318, 10318, "https://www.imdb.com/title/tt0068646/"),
        (527,   "Schindler's List (1993)",           "Drama|War",               1993, 4.246, 11450, "https://www.imdb.com/title/tt0108052/"),
        (593,   "Silence of the Lambs, The (1991)", "Crime|Horror|Thriller",   1991, 4.183, 14061, "https://www.imdb.com/title/tt0102926/"),
        (296,   "Pulp Fiction (1994)",               "Comedy|Crime|Drama",      1994, 4.186, 15263, "https://www.imdb.com/title/tt0110912/"),
        (2571,  "Matrix, The (1999)",                "Action|Sci-Fi|Thriller",  1999, 4.155, 14540, "https://www.imdb.com/title/tt0133093/"),
        (2959,  "Fight Club (1999)",                 "Action|Crime|Drama",      1999, 4.234, 11962, "https://www.imdb.com/title/tt0137523/"),
        (4993,  "Lord of the Rings: Fellowship (2001)", "Adventure|Fantasy",   2001, 4.141, 11410, "https://www.imdb.com/title/tt0120737/"),
        (58559, "Dark Knight, The (2008)",           "Action|Crime|Drama",      2008, 4.268,  8979, "https://www.imdb.com/title/tt0468569/"),
        (79132, "Inception (2010)",                  "Action|Crime|Sci-Fi",     2010, 4.156,  8540, "https://www.imdb.com/title/tt1375666/"),
        (109487,"Interstellar (2014)",               "Sci-Fi",                  2014, 4.175,  7020, "https://www.imdb.com/title/tt0816692/"),
        (112552,"Whiplash (2014)",                   "Drama",                   2014, 4.166,  2490, "https://www.imdb.com/title/tt2582802/"),
        (185029,"Parasite (2019)",                   "Comedy|Drama|Thriller",   2019, 4.317,  1820, "https://www.imdb.com/title/tt6751668/"),
        (230307,"Oppenheimer (2023)",                "Drama|History",           2023, 4.210,  2801, "https://www.imdb.com/title/tt15398776/"),
        (356,   "Forrest Gump (1994)",               "Comedy|Drama|Romance",    1994, 4.004, 15564, "https://www.imdb.com/title/tt0109830/"),
        (260,   "Star Wars: Ep. IV (1977)",          "Action|Adventure|Sci-Fi", 1977, 4.110, 13277, "https://www.imdb.com/title/tt0076759/"),
        (50,    "Usual Suspects, The (1995)",        "Crime|Mystery|Thriller",  1995, 4.277, 10582, "https://www.imdb.com/title/tt0114814/"),
        (48516, "Departed, The (2006)",              "Crime|Drama|Thriller",    2006, 4.174,  7623, "https://www.imdb.com/title/tt0407887/"),
        (96610, "Django Unchained (2012)",           "Action|Drama|Western",    2012, 4.108,  6128, "https://www.imdb.com/title/tt1853728/"),
        (1,     "Toy Story (1995)",                  "Animation|Children|Comedy",1995,3.887, 12748, "https://www.imdb.com/title/tt0114709/"),
    ]
    df = pd.DataFrame(
        rows,
        columns=["movieId", "title", "genres", "year", "avg_rating", "num_ratings", "imdb_url"],
    )
    df["title_clean"] = df["title"].str.replace(r"\s*\(\d{4}\)", "", regex=True).str.strip()
    df["tmdbId"] = float("nan")
    df["tmdb_url"] = ""
    C = df["avg_rating"].mean()
    m = df["num_ratings"].quantile(0.4)
    df["bayesian_score"] = (
        (df["num_ratings"] / (df["num_ratings"] + m)) * df["avg_rating"]
        + (m / (df["num_ratings"] + m)) * C
    )
    df["top_tags"] = ""
    return df


@st.cache_resource(show_spinner=False)
def load_knn():
    kp = os.path.join(CACHE_DIR, "knn_model.pkl")
    sp = os.path.join(CACHE_DIR, "pivot_sparse.npz")
    ip = os.path.join(CACHE_DIR, "pivot_index.npy")
    if all(os.path.exists(x) for x in [kp, sp, ip]):
        try:
            from scipy.sparse import load_npz
            with open(kp, "rb") as f:
                knn = pickle.load(f)
            sparse    = load_npz(sp)
            movie_ids = np.load(ip)
            mid2row   = {int(mid): i for i, mid in enumerate(movie_ids)}
            return knn, sparse, mid2row
        except Exception as e:
            st.warning(f"Model yüklenemedi: {e}. Demo modda çalışılıyor.")
    return None, None, {}
