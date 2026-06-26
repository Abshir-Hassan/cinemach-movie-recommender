"""
KNN + Bayesian hybrid recommendation engine (Single Responsibility).
Input: loaded DataFrames + fitted KNN model.
Output: ranked DataFrame of film recommendations.
"""
from __future__ import annotations
import pandas as pd


def recommend(
    ms: pd.DataFrame,
    knn,
    sparse,
    mid2row: dict,
    genres: list[str] | None = None,
    min_rat: float = 3.5,
    yr0: int = 1990,
    yr1: int = 2023,
    n: int = 10,
    liked_mid: int | None = None,
) -> pd.DataFrame:
    df   = ms.copy()
    mask = (
        (df["avg_rating"] >= min_rat)
        & (df["year"] >= yr0)
        & (df["year"] <= yr1)
        & (df["num_ratings"] >= 10)
    )
    if genres:
        mask &= df["genres"].apply(lambda g: any(x in str(g) for x in genres))
    fil = df[mask].copy()
    if fil.empty:
        return pd.DataFrame()

    # ── KNN cosine similarity ─────────────────────────────────────────────────
    if knn is not None and sparse is not None and mid2row:
        ref = liked_mid if (liked_mid and liked_mid in mid2row) else None
        if ref is None:
            best = fil.nlargest(1, "num_ratings")
            if not best.empty:
                cand = int(best.iloc[0]["movieId"])
                ref  = cand if cand in mid2row else None
        if ref:
            row        = sparse[mid2row[ref]]
            dist, idxs = knn.kneighbors(row, n_neighbors=min(100, sparse.shape[0]))
            idx2mid    = {v: k for k, v in mid2row.items()}
            smap       = {
                idx2mid[idxs[0][i]]: float(1 - dist[0][i])
                for i in range(len(idxs[0]))
            }
            fil["knn_sim"] = fil["movieId"].map(smap).fillna(0.40)
        else:
            fil["knn_sim"] = 0.50
    else:
        fil["knn_sim"] = 0.50

    # ── Bayesian weighted rating ──────────────────────────────────────────────
    # formula: score = (n/(n+m))*R + (m/(n+m))*C
    # where C = mean avg_rating, m = 40th percentile vote count
    C = fil["avg_rating"].mean()
    m = fil["num_ratings"].quantile(0.4)
    bayesian = (
        (fil["num_ratings"] / (fil["num_ratings"] + m)) * fil["avg_rating"]
        + (m / (fil["num_ratings"] + m)) * C
    )

    # ── Hybrid final score: 65% Bayesian + 35% KNN ───────────────────────────
    fil["score"] = bayesian * 0.65 + fil["knn_sim"] * 0.35
    return fil.nlargest(n, "score").reset_index(drop=True)
