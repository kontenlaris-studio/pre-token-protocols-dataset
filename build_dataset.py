#!/usr/bin/env python3
"""Build the Pre-Token Protocols dataset from a DefiLlama /protocols snapshot.

A protocol counts as pre-token when DefiLlama has no CoinGecko id and no
market cap for it (it has not issued a listed token). We keep protocols with
TVL >= $1M — below that, the long tail is mostly abandoned forks.
Output: data/pre_token_protocols.csv + .jsonl with a fixed, documented schema.
"""
import csv
import json
import os
import sys
from datetime import datetime, timezone

SNAPSHOT_DATE = datetime.now(timezone.utc).date().isoformat()
MIN_TVL = 1_000_000

FIELDS = ["name", "slug", "category", "tvl_usd", "change_1d_pct", "change_7d_pct",
          "primary_chain", "chain_count", "listed_at", "age_days", "audits",
          "url", "description"]


def build(src="/tmp/protocols.json", outdir="data"):
    raw = json.load(open(src))
    now = datetime.now(timezone.utc).timestamp()
    # Brands that already have a token: their sub-entries (e.g. "Aave V3" under
    # a tokenized parent "Aave") are not pre-token launches — exclude them.
    # Brands that already have a token: their sibling entries (e.g. "Aave V3",
    # whose token sits on the "Aave V2" entry) are not pre-token launches.
    # Brand = first word of a tokenized protocol's name.
    tokenized_brands = set()
    for p in raw:
        if p.get("gecko_id") or p.get("mcap"):
            name = (p.get("name") or "").strip()
            if name:
                tokenized_brands.add(name.split()[0].lower())
    def is_sub_of_tokenized(name):
        parts = name.lower().split()
        return bool(parts) and parts[0] in tokenized_brands
    rows = []
    excluded_sub = 0
    for p in raw:
        if p.get("gecko_id") or p.get("mcap"):
            continue  # already has a listed token
        tvl = p.get("tvl") or 0
        if tvl < MIN_TVL:
            continue
        if is_sub_of_tokenized(p.get("name") or ""):
            excluded_sub += 1
            continue
        listed = p.get("listedAt")
        rows.append({
            "name": p.get("name", ""),
            "slug": p.get("slug", ""),
            "category": p.get("category", ""),
            "tvl_usd": round(tvl, 2),
            "change_1d_pct": p.get("change_1d"),
            "change_7d_pct": p.get("change_7d"),
            "primary_chain": p.get("chain", ""),
            "chain_count": len(p.get("chains") or []),
            "listed_at": datetime.fromtimestamp(listed, timezone.utc).date().isoformat() if listed else "",
            "age_days": int((now - listed) // 86400) if listed else "",
            "audits": p.get("audits", ""),
            "url": p.get("url", ""),
            "description": (p.get("description") or "").replace("\n", " ").strip()[:400],
        })
    rows.sort(key=lambda r: r["tvl_usd"], reverse=True)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "pre_token_protocols.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(outdir, "pre_token_protocols.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    cats = {}
    for r in rows:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    stats = {
        "snapshot_date": SNAPSHOT_DATE,
        "source_protocols_total": len(raw),
        "excluded_subprotocols_of_tokenized_parents": excluded_sub,
        "pre_token_with_tvl_over_1m": len(rows),
        "combined_tvl_usd": round(sum(r["tvl_usd"] for r in rows), 2),
        "top_categories": dict(sorted(cats.items(), key=lambda x: -x[1])[:10]),
    }
    json.dump(stats, open(os.path.join(outdir, "stats.json"), "w"), indent=2)
    return stats


if __name__ == "__main__":
    print(json.dumps(build(*sys.argv[1:]), indent=2))
