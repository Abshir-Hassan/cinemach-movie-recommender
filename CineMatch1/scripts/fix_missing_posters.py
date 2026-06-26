"""
Targeted re-fetch for films that got no poster_path in the first run.
Tries /movie/{id} then /tv/{id} (covers TV mini-series in MovieLens).

Usage:
    python scripts/fix_missing_posters.py --api-key YOUR_KEY
"""
import os
import sys
import time
import argparse
import requests
import pandas as pd


def fetch(session: requests.Session, url: str, params: dict) -> dict | None:
    for attempt in range(3):
        try:
            r = session.get(url, params=params, timeout=8)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 10)))
            elif r.status_code == 404:
                return None
        except requests.RequestException:
            time.sleep(2)
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True)
    parser.add_argument(
        "--cache-dir",
        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache"),
    )
    args = parser.parse_args()

    stats_path   = os.path.join(args.cache_dir, "movie_stats.csv")
    posters_path = os.path.join(args.cache_dir, "poster_paths.csv")

    ms = pd.read_csv(stats_path)
    pp = pd.read_csv(posters_path)

    # Find rows in poster_paths.csv where poster_path is null/empty
    null_mask = pp["poster_path"].isna() | (pp["poster_path"].astype(str).str.strip() == "")
    missing_ids = set(pp[null_mask]["movieId"].astype(int))

    # Also find film IDs in movie_stats that are completely absent from poster_paths
    covered_ids = set(pp["movieId"].astype(int))
    absent_ids  = set(ms["movieId"].astype(int)) - covered_ids
    target_ids  = missing_ids | absent_ids

    targets = ms[ms["movieId"].isin(target_ids) & ms["tmdbId"].notna()].copy()
    print(f"Targeting {len(targets)} films (null poster or absent from CSV)...")

    session = requests.Session()
    params  = {"api_key": args.api_key, "language": "en-US"}
    updates = {}

    for i, row in enumerate(targets.itertuples(), 1):
        movie_id = int(row.movieId)
        tmdb_id  = int(row.tmdbId)

        # Try /movie first, then /tv
        path = ""
        for media in ("movie", "tv"):
            url  = f"https://api.themoviedb.org/3/{media}/{tmdb_id}"
            data = fetch(session, url, params)
            if data:
                path = data.get("poster_path") or ""
                if path:
                    break

        if path:
            updates[movie_id] = path
            print(f"  [{i:>3}/{len(targets)}] movieId={movie_id:7d}  FOUND  {path}")
        else:
            print(f"  [{i:>3}/{len(targets)}] movieId={movie_id:7d}  no poster on TMDB")

        time.sleep(1 / 35)

    # Patch poster_paths.csv
    if updates:
        for movie_id, path in updates.items():
            mask = pp["movieId"].astype(int) == movie_id
            if mask.any():
                pp.loc[mask, "poster_path"] = path
            else:
                new_row = pd.DataFrame([{"movieId": movie_id, "poster_path": path}])
                pp = pd.concat([pp, new_row], ignore_index=True)

        pp.to_csv(posters_path, index=False)
        print(f"\nUpdated {len(updates)} poster paths in {posters_path}")
    else:
        print("\nNo new poster paths found.")

    print("Restart Streamlit to pick up the changes.")


if __name__ == "__main__":
    main()
