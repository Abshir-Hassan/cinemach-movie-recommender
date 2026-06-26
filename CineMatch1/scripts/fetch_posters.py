"""
One-time script to fetch TMDB poster paths for all 7,679 films.

Usage:
    python scripts/fetch_posters.py --api-key YOUR_KEY

Get a FREE API key (takes 60 seconds):
    1. Go to: https://www.themoviedb.org/signup
    2. Verify your email
    3. Go to: https://www.themoviedb.org/settings/api
    4. Request an API key (select "Developer")
    5. Copy the "API Key (v3 auth)" value

Runtime: ~5 minutes for 7,676 films (rate-limited to 35 req/s).
Output: cache/poster_paths.csv  (loaded automatically by the app)
"""
import os
import sys
import time
import argparse

import requests
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch TMDB poster paths")
    parser.add_argument("--api-key", required=True, help="TMDB API v3 key")
    parser.add_argument(
        "--cache-dir",
        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache"),
        help="Path to cache directory (default: ../cache)",
    )
    args = parser.parse_args()

    stats_path = os.path.join(args.cache_dir, "movie_stats.csv")
    out_path   = os.path.join(args.cache_dir, "poster_paths.csv")

    if not os.path.exists(stats_path):
        print(f"ERROR: {stats_path} not found. Run the data pipeline first.")
        sys.exit(1)

    df = pd.read_csv(stats_path)
    if "tmdbId" not in df.columns:
        print("ERROR: movie_stats.csv has no 'tmdbId' column.")
        sys.exit(1)

    df_valid = df[df["tmdbId"].notna() & (df["tmdbId"] > 0)].copy()
    total    = len(df_valid)
    print(f"Fetching posters for {total} films via TMDB API...")
    print("Estimated time: ~5 minutes\n")

    results = []
    session = requests.Session()
    base_url = "https://api.themoviedb.org/3/movie/{tmdb_id}"
    params   = {"api_key": args.api_key, "language": "en-US"}
    delay    = 1 / 35  # 35 requests/second, safely under TMDB's 40/s limit

    for i, row in enumerate(df_valid.itertuples(), 1):
        tmdb_id  = int(row.tmdbId)
        movie_id = int(row.movieId)
        url      = base_url.format(tmdb_id=tmdb_id)

        for attempt in range(3):
            try:
                resp = session.get(url, params=params, timeout=8)
                if resp.status_code == 200:
                    poster_path = resp.json().get("poster_path") or ""
                    results.append({"movieId": movie_id, "poster_path": poster_path})
                    break
                elif resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 10))
                    print(f"\n  Rate limited — waiting {wait}s...")
                    time.sleep(wait)
                elif resp.status_code == 404:
                    results.append({"movieId": movie_id, "poster_path": ""})
                    break
                else:
                    time.sleep(1)
            except requests.RequestException:
                time.sleep(2)
        else:
            results.append({"movieId": movie_id, "poster_path": ""})

        time.sleep(delay)

        if i % 200 == 0 or i == total:
            covered = sum(1 for r in results if r["poster_path"])
            pct     = covered / i * 100
            eta     = (total - i) * delay
            print(f"  [{i:>5}/{total}]  {covered} with poster ({pct:.0f}%)  ETA ~{eta:.0f}s")

    # Save
    out_df   = pd.DataFrame(results)
    out_df.to_csv(out_path, index=False)
    covered  = (out_df["poster_path"] != "").sum()
    print(f"\nDone!  {covered}/{total} films have poster paths.")
    print(f"Saved to: {out_path}")
    print("\nRestart Streamlit — all film posters will now load automatically.")


if __name__ == "__main__":
    main()
