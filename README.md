```
 ______     ______   ______     ______     __    __        ______     ______     __   __   __     ______     __     __     ______
/\  ___\   /\__  _\ /\  ___\   /\  __ \   /\ "-./  \      /\  == \   /\  ___\   /\ \ / /  /\ \   /\  ___\   /\ \  _ \ \   /\  ___\
\ \___  \  \/_/\ \/ \ \  __\   \ \  __ \  \ \ \-./\ \     \ \  __<   \ \  __\   \ \ \'/   \ \ \  \ \  __\   \ \ \/ ".\ \  \ \___  \
 \/\_____\    \ \_\  \ \_____\  \ \_\ \_\  \ \_\ \ \_\     \ \_\ \_\  \ \_____\  \ \__|    \ \_\  \ \_____\  \ \__/".~\_\  \/\_____\
  \/_____/     \/_/   \/_____/   \/_/\/_/   \/_/  \/_/      \/_/ /_/   \/_____/   \/_/      \/_/   \/_____/   \/_/   \/_/   \/_____/
```

<h1 align="center">Steam Reviews Scraper & CLI Tool</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Steam-Store%20API-171A21?logo=steam&logoColor=white" alt="Steam">
  <img src="https://img.shields.io/badge/Rich-14.2+-4EC820?logo=terminal&logoColor=white" alt="Rich">
  <img src="https://img.shields.io/badge/Requests-2.32+-FF6600?logo=python&logoColor=white" alt="Requests">
  <img src="https://img.shields.io/badge/openpyxl-3.1+-217346?logo=microsoftexcel&logoColor=white" alt="openpyxl">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</p>

<p align="center">
  A terminal-based tool to browse the <a href="https://store.steampowered.com">Steam Store</a>, view game details,<br>
  compare system requirements, and bulk-download reviews to CSV/Excel.
</p>

```bash
git clone https://github.com/Imkun-on/steam_scraper_reviews_cli.git
cd steam_scraper_reviews_cli
pip install -r requirements.txt
python run.py
```

---

## Table of Contents

- [What it does](#what-it-does)
- [Libraries Used & Why](#libraries-used--why)
- [Requirements & Installation](#requirements--installation)
- [Usage & Examples](#usage--examples)
  - [Main Menu](#main-menu)
  - [Example 1: Search by name](#example-1-search-by-name)
  - [Example 2: Browse Top Sellers](#example-2-browse-top-sellers)
  - [Example 3: Download reviews](#example-3-download-reviews)
- [Game Details Panel](#game-details-panel)
- [Review Scraping](#review-scraping)
- [Export Formats](#export-formats)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Cross-platform support](#cross-platform-support)
- [License](#license)

---

## What it does

| Feature | Steam Store (website) | Steam Reviews CLI |
|---|---|---|
| **Browse** | Navigate pages manually | Browse New & Trending, Top Sellers, Coming Soon, Specials, Free to Play from one menu |
| **Search** | Basic store search | Search by name with enriched results (release date, languages, price) |
| **Game details** | Scattered across tabs | Single panel: metadata, packages with discount pricing, description, system requirements |
| **System requirements** | Read and compare manually | Auto-detects your PC specs and shows them side-by-side with min/recommended |
| **Review counts** | Total count only | Per-language review breakdown with rating labels (Overwhelmingly Positive, Mixed, etc.) |
| **Reviews export** | Not available | Bulk download all reviews to CSV or Excel with author name, Steam ID, playtime, date |
| **UI** | Web browser required | Terminal-native with colored tables, progress bars, structured descriptions |

---

## Libraries Used & Why

| Library | Version | Purpose | Why this library? |
|---------|---------|---------|-------------------|
| `requests` | >= 2.32 | HTTP client for all Steam Store API calls (search, app details, reviews) | The standard Python HTTP library. Handles all communication with Steam's undocumented store API, including retry logic on 502/503 errors and session-based requests with persistent headers |
| `rich` | >= 14.2 | Terminal UI — tables, panels, progress bars, spinners, colored/styled text | Transforms raw API data into a polished CLI experience. `Table` for search results and language selection, `Panel` for game details, `Progress` with real-time ETA for review downloads, `Text.from_markup` for structured descriptions with section headers and bullet points |
| `openpyxl` | >= 3.1 | Excel (.xlsx) export with styled headers and formatted columns | Optional but included — lets users export reviews as proper Excel workbooks with bold headers, Steam-themed colors, and auto-sized columns. Used only when the user selects Excel export format |

### Standard Library Modules (no install needed)

| Module | Purpose |
|--------|---------|
| `concurrent.futures` | Parallel HTTP requests — fetches review counts for all 30 languages simultaneously via `ThreadPoolExecutor` (10 workers) |
| `subprocess` | PC hardware detection on Windows via PowerShell (`Win32_Processor`, `Win32_VideoController`, `Win32_ComputerSystem`) |
| `platform` | OS detection for system requirements comparison |
| `csv` | CSV export of downloaded reviews |
| `re` | HTML stripping from Steam API responses, package price parsing |
| `html` | Unescaping HTML entities in game descriptions |

---

## Requirements & Installation

### Python

Requires **Python 3.10+**.

### Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests rich openpyxl
```

`openpyxl` is optional — only needed for Excel export. CSV export works without it.

---

## Usage & Examples

```bash
python run.py
```

### Main Menu

The interactive main menu appears after the banner:

```
                    Main Menu
  ┌──────┬──────────────────────────┐
  │  #   │ Option                   │
  ├──────┼──────────────────────────┤
  │  S   │ Search by name           │
  │  1   │ New & Trending           │
  │  2   │ Top Sellers              │
  │  3   │ Coming Soon              │
  │  4   │ Specials                 │
  │  5   │ Free to Play             │
  │  Q   │ Quit                     │
  └──────┴──────────────────────────┘

  Choose an option:
```

Press `q` at any point to go back to this menu.

---

### Example 1: Search by name

```
  Choose an option: s
  Search a game on Steam: Resident Evil 4

  ⠋ Searching 'Resident Evil 4'...
  ⠋ Loading details...

                          Search Results (10)
  ┌────┬──────────────────────┬──────────┬──────────────┬──────────┬──────────────┐
  │  # │ Title                │  App ID  │ Release Date │Languages │        Price │
  ├────┼──────────────────────┼──────────┼──────────────┼──────────┼──────────────┤
  │  1 │ Resident Evil 4      │ 2050650  │ 23 Mar, 2023 │ English  │    15.99 EUR │
  │  2 │ Resident Evil 4 (... │  254700  │ 27 Feb, 2014 │ English  │    19.99 EUR │
  │ .. │ ...                  │   ...    │     ...      │   ...    │         ...  │
  └────┴──────────────────────┴──────────┴──────────────┴──────────┴──────────────┘
  Enter q to go back

  Select a game (number) or q to go back: 1
```

---

### Example 2: Browse Top Sellers

```
  Choose an option: 2

  ⠋ Loading Top Sellers...
  ⠋ Loading details...

                          Top Sellers (10)
  ┌────┬──────────────────────┬──────────┬──────────────┬──────────┬──────────────────────┐
  │  # │ Title                │  App ID  │ Release Date │Languages │                Price │
  ├────┼──────────────────────┼──────────┼──────────────┼──────────┼──────────────────────┤
  │  1 │ Crimson Desert       │ 3321460  │  5 Jun, 2025 │ English  │              69.99€  │
  │  2 │ Road to Vostok       │ 1963610  │ 18 Oct, 2024 │ English  │ 14.62€ (-25% 19.50€) │
  │ .. │ ...                  │   ...    │     ...      │   ...    │                 ...  │
  └────┴──────────────────────┴──────────┴──────────────┴──────────┴──────────────────────┘
  Enter q to go back

  Select a game (number) or q to go back: 1
```

---

### Example 3: Download reviews

After selecting a game and viewing its details:

```
  Download reviews? [y/n]: y

  ──────────────── Review Scraping ────────────────

  ⠋ Fetching review counts per language...

                        Language Filter (30)
  ┌──────┬──────────────┬───────────────────────────┬──────────┬──────────────────────────────┐
  │  #   │ Code         │ Language                  │  Reviews │           Rating             │
  ├──────┼──────────────┼───────────────────────────┼──────────┼──────────────────────────────┤
  │  1   │ all          │ All languages             │  238,456 │  Overwhelmingly Positive     │
  │  2   │ arabic       │ Arabic                    │        1 │  N/A                         │
  │  ... │ ...          │ ...                       │      ... │  ...                         │
  │  8   │ english      │ English                   │   86,192 │  Overwhelmingly Positive     │
  │  14  │ italian      │ Italian                   │    1,425 │  Overwhelmingly Positive     │
  │  ... │ ...          │ ...                       │      ... │  ...                         │
  └──────┴──────────────┴───────────────────────────┴──────────┴──────────────────────────────┘

  Select language (number): 14

  → Filter: Italian

  ⠋ Downloading reviews  ██████████████████████████  100%  1,425/1,425  │ 0:00:45 → 0:00:00

  ✓ Downloaded: 1,425 reviews

                    Preview (first 5 reviews)
  ┌──────────────────────┬────────────┬──────────────────────────┬──────────┬──────────┐
  │ Steam ID             │ Author     │ Review                   │   Type   │   Date   │
  ├──────────────────────┼────────────┼──────────────────────────┼──────────┼──────────┤
  │ 76561198805746665    │ wangangelo │ troppo bello             │ positive │ 2025-... │
  │ 76561198026019530    │ rei4       │ Uno dei migliori capi... │ positive │ 2025-... │
  │ ...                  │ ...        │ ...                      │   ...    │   ...    │
  └──────────────────────┴────────────┴──────────────────────────┴──────────┴──────────┘

  Save format [csv/excel/both/skip] (csv): both

  ╔══════════ ✅ Export Complete ══════════╗
  ║  Reviews     1,425                     ║
  ║  Language    Italian                   ║
  ║  Format      both                      ║
  ║  ✓ Saved     reviews_Resident_Evil_4_italian.csv   ║
  ║  ✓ Saved     reviews_Resident_Evil_4_italian.xlsx  ║
  ╚════════════════════════════════════════╝
```

---

## Game Details Panel

Selecting a game displays a full info panel:

- **Metadata** — release date, developer, publisher, genre tags, franchise
- **Packages** — all available editions with original price ~~struck through~~ and discounted price highlighted
- **Reviews** — total count with positive/negative breakdown and percentage
- **Description** — structured with section headers, bullet points, and text wrapping
- **System Requirements** — your PC specs auto-detected and shown side-by-side with minimum and recommended requirements

---

## Review Scraping

The scraper downloads **all reviews** for a game in a selected language via the Steam API:

- Fetches in batches of 100 with cursor-based pagination
- Real-time progress bar with ETA
- Each review includes: **Steam ID**, **author name**, **full review text**, **positive/negative**, **purchase type** (Steam/key), **language**, **playtime**, **date**

---

## Export Formats

| Format | File | Details |
|--------|------|---------|
| **CSV** | `reviews_{Game}_{lang}.csv` | Standard CSV, UTF-8 encoded, compatible with any spreadsheet or data tool |
| **Excel** | `reviews_{Game}_{lang}.xlsx` | Styled workbook with bold headers (Steam dark theme), auto-sized columns, ready to filter and sort |

Both formats include all fields: `steam_id`, `author`, `review`, `review_type`, `purchase_type`, `language`, `playtime`, `date`.

---

## Architecture

```
steam_scraper_reviews_cli/
│
├── run.py              Entry point
├── cli.py              Rich terminal UI (menus, tables, panels, progress bars)
├── api.py              Steam Store API wrapper (search, details, reviews, categories)
├── specs.py            PC hardware detection via PowerShell (Windows)
└── requirements.txt    Python dependencies
```

```
cli.py
  │
  ├── api.py ──── Steam Store API (store.steampowered.com)
  │                 ├── /api/storesearch/         → game search
  │                 ├── /api/appdetails/           → game metadata, description, requirements
  │                 ├── /api/featuredcategories/   → New & Trending, Top Sellers, Coming Soon, Specials
  │                 ├── /search/                   → Free to Play listings
  │                 └── /appreviews/{appid}        → review data and per-language counts
  │
  ├── specs.py ── PowerShell (Windows)
  │                 ├── Win32_Processor            → CPU name
  │                 ├── Win32_VideoController       → GPU name
  │                 └── Win32_ComputerSystem        → RAM total
  │
  └── Rich (terminal UI)
          Tables, Panels, Progress bars, Styled text
```

---

## Configuration

Constants in `api.py`:

| Constant | Default | Description |
|---|---|---|
| `MAX_RETRIES` | 3 | Retry attempts on 502/503 errors |
| `RETRY_DELAY` | 2s | Wait between retries |
| `SESSION` | persistent | Reuses HTTP connection with `Accept-Language: en` |

The Steam Store API is undocumented and rate-limited. The tool uses a persistent session and automatic retries to handle transient errors gracefully.

---

## Cross-platform support

- **Windows** — full support including automatic PC specs detection (CPU, GPU, RAM via PowerShell)
- **macOS / Linux** — fully functional, but PC specs detection shows "N/A" (Steam API data still works)
- UTF-8 output is automatically configured on Windows terminals

---

## License

This project is licensed under the MIT License.
