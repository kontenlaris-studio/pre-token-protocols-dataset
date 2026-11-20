---
license: cc-by-4.0
language: [en]
tags: [defi, crypto, pre-token, tvl, defillama, airdrop-watch]
pretty_name: Pre-Token Protocols (DefiLlama snapshot)
---

# Pre-Token Protocols — Dataset

**838 DeFi protocols that have real traction (TVL ≥ $1M) but have not issued a listed token** — the watchlist for future launches, airdrops and token sales, derived from a full DefiLlama snapshot dated **2026-11-20**.

| | |
|---|---|
| Rows | 838 protocols |
| Combined TVL | $201.5B (includes tracked CEX reserves) |
| Source universe | 9,079 protocols on DefiLlama |
| Files | `data/pre_token_protocols.csv` · `data/pre_token_protocols.jsonl` · `data/stats.json` |
| Rebuild | `python3 build_dataset.py` (stdlib only, fetches a fresh snapshot) |

## Why this exists

Finding pre-token protocols normally means scrolling thousands of listings and checking each one for a token by hand. This dataset does that filtering once, documents exactly how, and ships in analysis-ready CSV/JSONL.

## Definition — read this before citing

A protocol is **pre-token** in this dataset when, in the DefiLlama snapshot:

1. it has **no CoinGecko id and no market cap** (no listed token), **and**
2. its **brand** (first word of its name) does not match the brand of any tokenized protocol — this removes sibling entries such as "Aave V3", whose token lives on the "Aave V2" entry (100 rows excluded this way), **and**
3. its TVL is **≥ $1,000,000**.

Notes: CEX rows are DefiLlama's tracked exchange-reserve entities (exchanges have no protocol token in this mapping). TVL for multi-chain protocols is the aggregate. "Pre-token" is a data statement about the snapshot date — not a promise that a token will ever launch.

## Schema

| Column | Meaning |
|---|---|
| `name`, `slug` | Protocol name and DefiLlama slug |
| `category` | DefiLlama category (Dexs, Lending, Liquid Staking, …) |
| `tvl_usd` | Total value locked, USD, snapshot date |
| `change_1d_pct`, `change_7d_pct` | TVL change percentages |
| `primary_chain`, `chain_count` | Main chain and number of chains deployed |
| `listed_at`, `age_days` | When DefiLlama first tracked it, and its age in days |
| `audits` | Audit count reported by DefiLlama |
| `url`, `description` | Project site and short description (truncated to 400 chars) |

## Top categories

Dexs 161 · Liquid Staking 81 · Lending 74 · Bridge 50 · Yield 50 · CEX 49 · Risk Curators 48 · Derivatives 38 · RWA 35 · Onchain Capital Allocator 27

## Companion tool

This dataset powers the free **[Token Radar](https://pre-token-screener.skillsafe.ai)** screener, which ranks these protocols by an implied-value model (TVL × category multiple × 7-day momentum × age).

## Attribution & license

Source data: [DefiLlama](https://defillama.com) public API (`api.llama.fi/protocols`), retrieved 2026-11-20. The compilation, filtering and schema are © Kontenlaris Studio under **CC BY 4.0** — reuse freely with attribution to this repo and to DefiLlama. Underlying protocol data remains subject to DefiLlama's terms.

---

<sub>Built by [Kontenlaris Studio](https://github.com/kontenlaris-studio) · More: [RingkasBot](https://t.me/KontenlarisRingkasBot) · [InvoiceKit](https://kontenlaris-studio.github.io/invoicekit/) · [SkillAudit](https://kontenlaris-studio.github.io/skill-audit/)</sub>
