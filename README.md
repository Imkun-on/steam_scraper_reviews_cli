<div align="center">

```
 ______     ______   ______     ______     __    __        ______     ______     __   __   __     ______     __     __     ______
/\  ___\   /\__  _\ /\  ___\   /\  __ \   /\ "-./  \      /\  == \   /\  ___\   /\ \ / /  /\ \   /\  ___\   /\ \  _ \ \   /\  ___\
\ \___  \  \/_/\ \/ \ \  __\   \ \  __ \  \ \ \-./\ \     \ \  __<   \ \  __\   \ \ \'/   \ \ \  \ \  __\   \ \ \/ ".\ \  \ \___  \
 \/\_____\    \ \_\  \ \_____\  \ \_\ \_\  \ \_\ \ \_\     \ \_\ \_\  \ \_____\  \ \__|    \ \_\  \ \_____\  \ \__/".~\_\  \/\_____\
  \/_____/     \/_/   \/_____/   \/_/\/_/   \/_/  \/_/      \/_/ /_/   \/_____/   \/_/      \/_/   \/_____/   \/_/   \/_/   \/_____/
```

# Steam Reviews Scraper & CLI Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Steam-Store%20API-171A21?logo=steam&logoColor=white" alt="Steam">
  <img src="https://img.shields.io/badge/Rich-14.2+-4EC820?logo=terminal&logoColor=white" alt="Rich">
  <img src="https://img.shields.io/badge/Requests-2.32+-FF6600?logo=python&logoColor=white" alt="Requests">
  <img src="https://img.shields.io/badge/openpyxl-3.1+-217346?logo=microsoftexcel&logoColor=white" alt="openpyxl">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</p>

**A terminal-based tool to browse the [Steam Store](https://store.steampowered.com), view game details, compare system requirements, and bulk-download reviews to CSV/Excel.**

[🎮 Features](#-features) • [📦 Installation](#-installation) • [🚀 Usage & Examples](#-usage--examples) • [🏗️ Architecture](#%EF%B8%8F-architecture)

</div>

---

## 📋 Project Description

This project provides a **fully interactive CLI** for exploring the Steam Store and scraping game reviews at scale. Instead of navigating the Steam website manually, you get a single terminal interface that lets you search games, browse storefront categories, inspect detailed metadata, and export complete review datasets — all with a polished Rich UI.

The tool is designed for:

- **Data analysts** who need review datasets for sentiment analysis or NLP research
- **Gamers** who want a quick terminal overview of any game's details and reception
- **Developers** interested in Steam Store API integration patterns

---

## 🎮 Features

### Steam Store (website) vs Steam Reviews CLI

| Feature | Steam Store (website) | Steam Reviews CLI |
|---|---|---|
| **Browse** | Navigate pages manually | Browse New & Trending, Top Sellers, Coming Soon, Specials, Free to Play from one menu |
| **Search** | Basic store search | Search by name or paste a Steam URL to jump directly to game details |
| **Game details** | Scattered across tabs | Single panel: metadata, packages with discount pricing, description, system requirements |
| **System requirements** | Read and compare manually | Auto-detects your PC specs and shows them side-by-side with min/recommended |
| **Review counts** | Total count only | Per-language review breakdown with rating labels (Overwhelmingly Positive, Mixed, etc.) |
| **Reviews export** | Not available | Bulk download all reviews to CSV or Excel with author name, Steam ID, playtime, date |
| **UI** | Web browser required | Terminal-native with colored tables, progress bars, structured descriptions |

---

## 📦 Installation

### Requirements

Requires **Python 3.10+**.

```bash
git clone https://github.com/Imkun-on/steam_scraper_reviews_cli.git
cd steam_scraper_reviews_cli
pip install -r requirements.txt
python run.py
```

Or install dependencies manually:

```bash
pip install requests rich openpyxl
```

> `openpyxl` is optional — only needed for Excel export. CSV export works without it.

---

## 📚 Libraries Used & Why

### Third-Party Dependencies

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

## 🚀 Usage & Examples

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
  │  S   │ Search by name or URL    │
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
  Enter a game name or Steam URL: Resident Evil 4

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

### Example 2: Direct URL lookup

You can paste a Steam Store URL directly to skip the search and jump straight to the game details:

```
  Choose an option: s
  Enter a game name or Steam URL: https://store.steampowered.com/app/2050650/Resident_Evil_4/

  → Detected Steam URL  App ID: 2050650

  ⠋ Loading game details...

  ╔══════════════════════════ Resident Evil 4 ══════════════════════════╗
  ║                                                                     ║
  ║     · Release date: 23 Mar, 2023                                    ║
  ║     · Developer: CAPCOM Co., Ltd.                                   ║
  ║     · Publisher: CAPCOM Co., Ltd.                                   ║
  ║     · Tags: Action, Adventure                                       ║
  ║     · Price: 15,99€  (-60%  base: 39,99€)                           ║
  ║       ▸ Resident Evil 4  39,99€  15,99€                             ║
  ║       ▸ Resident Evil 4 Gold Edition  49,99€  19,99€                ║
  ║     ...                                                             ║
  ╚═════════════════════════════════════════════════════════════════════╝

  Download reviews? [y/n]:
```

> Supported URL formats:
> - `https://store.steampowered.com/app/2050650/Resident_Evil_4/`
> - `https://store.steampowered.com/app/2050650`
> - `http://store.steampowered.com/app/730/`

---

### Example 3: Browse Top Sellers

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

### Example 4: Download reviews

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

## 🎯 Game Details Panel

Selecting a game displays a comprehensive info panel with all relevant data in one place:

<table>
<tr>
<td width="180"><strong>📋 Metadata</strong></td>
<td>Release date, developer, publisher, genre tags, franchise</td>
</tr>
<tr>
<td><strong>💰 Packages</strong></td>
<td>All available editions with original price <s>struck through</s> and discounted price highlighted in green</td>
</tr>
<tr>
<td><strong>⭐ Reviews</strong></td>
<td>Total count with positive/negative breakdown and percentage</td>
</tr>
<tr>
<td><strong>📖 Description</strong></td>
<td>Structured with section headers (bold cyan), bullet points (yellow markers), and automatic text wrapping</td>
</tr>
<tr>
<td><strong>🖥️ System Requirements</strong></td>
<td>Your PC specs auto-detected and displayed side-by-side with minimum and recommended requirements</td>
</tr>
</table>

---

## 🔍 Review Scraping

The scraper downloads **all reviews** for a game in a selected language via the Steam API.

### How it works

1. **Language selection** — shows a table with all 30 supported languages, each with its review count and rating label (fetched in parallel, ~3 seconds)
2. **Download** — fetches reviews in batches of 100 with cursor-based pagination and a real-time progress bar with ETA
3. **Preview** — displays the first 5 reviews in a formatted table
4. **Export** — saves to CSV, Excel, or both

### Review Data Fields

| Field | Description |
|-------|-------------|
| `steam_id` | Unique Steam ID of the reviewer (primary key) |
| `author` | Display name of the reviewer |
| `review` | Full review text (no truncation) |
| `review_type` | `positive` or `negative` |
| `purchase_type` | `steam` or `key/other` |
| `language` | Language code of the review |
| `playtime` | Total playtime (e.g., `27h 45m`) |
| `date` | Review submission date |

### Rating Labels

The language filter table shows Steam's rating label for each language:

| Label | Color |
|-------|-------|
| Overwhelmingly Positive | Bright green |
| Very Positive | Green |
| Positive / Mostly Positive | Green |
| Mixed | Yellow |
| Mostly Negative / Negative | Red |
| Very Negative / Overwhelmingly Negative | Bright red |

---

## 📁 Export Formats

| Format | File | Details |
|--------|------|---------|
| **CSV** | `reviews_{Game}_{lang}.csv` | Standard CSV, UTF-8 encoded, compatible with any spreadsheet or data tool |
| **Excel** | `reviews_{Game}_{lang}.xlsx` | Styled workbook with bold headers (Steam dark theme `#1B2838`), auto-sized columns, ready to filter and sort |

Both formats include all 8 fields: `steam_id`, `author`, `review`, `review_type`, `purchase_type`, `language`, `playtime`, `date`.

---

## 🏗️ Architecture

### Project Structure

```
steam_scraper_reviews_cli/
│
├── run.py              Entry point
├── cli.py              Rich terminal UI (menus, tables, panels, progress bars)
├── api.py              Steam Store API wrapper (search, details, reviews, categories)
├── specs.py            PC hardware detection via PowerShell (Windows)
└── requirements.txt    Python dependencies
```

### System Diagram

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
  │                 ├── Win32_VideoController      → GPU name
  │                 └── Win32_ComputerSystem       → RAM total
  │
  └── Rich (terminal UI)
          Tables, Panels, Progress bars, Styled text
```

### API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/storesearch/` | GET | Search games by name |
| `/api/appdetails/` | GET | Full game metadata (description, prices, packages, requirements) |
| `/api/featuredcategories/` | GET | Storefront categories (New & Trending, Top Sellers, Coming Soon, Specials) |
| `/search/` | GET + scrape | Free to Play game listings |
| `/appreviews/{appid}` | GET | Review data, per-language counts, and rating labels |

---

## ⚙️ Configuration

Constants in `api.py`:

| Constant | Default | Description |
|---|---|---|
| `MAX_RETRIES` | 3 | Retry attempts on 502/503 errors |
| `RETRY_DELAY` | 2s | Wait between retries |
| `SESSION` | persistent | Reuses HTTP connection with `Accept-Language: en` |

> The Steam Store API is undocumented and rate-limited. The tool uses a persistent session and automatic retries to handle transient errors gracefully.

---

## 🖥️ Cross-platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Windows** | Full support | Automatic PC specs detection (CPU, GPU, RAM via PowerShell) |
| **macOS** | Functional | PC specs detection shows "N/A" — all Steam API features work |
| **Linux** | Functional | PC specs detection shows "N/A" — all Steam API features work |

UTF-8 output is automatically configured on Windows terminals.

---

## 📄 License

This project is licensed under the MIT License.
