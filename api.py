"""Steam Store & Reviews API wrapper."""

import html
import re
import time
import requests

BASE = "https://store.steampowered.com"
SESSION = requests.Session()
SESSION.headers.update({"Accept-Language": "en"})

MAX_RETRIES = 3
RETRY_DELAY = 2

STEAM_LANGUAGES = {
    "all": "All languages",
    "arabic": "Arabic",
    "brazilian": "Portuguese (Brazil)",
    "bulgarian": "Bulgarian",
    "czech": "Czech",
    "danish": "Danish",
    "dutch": "Dutch",
    "english": "English",
    "finnish": "Finnish",
    "french": "French",
    "german": "German",
    "greek": "Greek",
    "hungarian": "Hungarian",
    "italian": "Italian",
    "japanese": "Japanese",
    "koreana": "Korean",
    "latam": "Spanish (Latin America)",
    "norwegian": "Norwegian",
    "polish": "Polish",
    "portuguese": "Portuguese",
    "romanian": "Romanian",
    "russian": "Russian",
    "schinese": "Chinese (Simplified)",
    "spanish": "Spanish",
    "swedish": "Swedish",
    "tchinese": "Chinese (Traditional)",
    "thai": "Thai",
    "turkish": "Turkish",
    "ukrainian": "Ukrainian",
    "vietnamese": "Vietnamese",
}


def _get(url: str, params: dict) -> requests.Response:
    """GET with automatic retry on 502/503 errors."""
    for attempt in range(MAX_RETRIES):
        resp = SESSION.get(url, params=params)
        if resp.status_code in (502, 503) and attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)
            continue
        resp.raise_for_status()
        return resp


def _strip_html(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return text.strip()


BROWSE_CATEGORIES = {
    "new_releases": "New & Trending",
    "top_sellers": "Top Sellers",
    "coming_soon": "Coming Soon",
    "specials": "Specials",
    "free": "Free to Play",
}


def browse_category(category: str, max_results: int = 10) -> list[dict]:
    """Fetch games from a Steam storefront category."""
    if category == "free":
        return _browse_free(max_results)

    resp = _get(f"{BASE}/api/featuredcategories/", params={"cc": "IT", "l": "english"})
    data = resp.json()
    items = data.get(category, {}).get("items", [])[:max_results]

    results = []
    for it in items:
        final = it.get("final_price", 0)
        original = it.get("original_price")
        discount = it.get("discount_percent", 0)

        if final == 0:
            price_str = "Free"
        elif discount > 0 and original:
            price_str = f"{final / 100:.2f}€  (-{discount}%  base: {original / 100:.2f}€)"
        else:
            price_str = f"{final / 100:.2f}€"

        results.append({
            "appid": it["id"],
            "name": it["name"],
            "price": price_str,
        })
    return results


def _browse_free(max_results: int = 10) -> list[dict]:
    """Scrape top free-to-play games from Steam search."""
    resp = _get(f"{BASE}/search/", params={
        "maxprice": "free", "category1": "998",
        "cc": "IT", "l": "english",
    })
    appids = []
    seen = set()
    for m in re.finditer(r'data-ds-appid="(\d+)"', resp.text):
        aid = int(m.group(1))
        if aid not in seen:
            seen.add(aid)
            appids.append(aid)
        if len(appids) >= max_results:
            break

    results = []
    for aid in appids:
        details = get_app_details(aid)
        if details:
            results.append({
                "appid": aid,
                "name": details.get("name", "N/A"),
                "price": "Free",
            })
    return results


def search_games(query: str, max_results: int = 10) -> list[dict]:
    resp = _get(f"{BASE}/api/storesearch/", params={"term": query, "l": "english", "cc": "IT"})
    data = resp.json()
    items = data.get("items", [])[:max_results]
    results = []
    for it in items:
        price_info = it.get("price", {})
        if price_info:
            price = price_info.get("final", 0) / 100
            currency = price_info.get("currency", "EUR")
            price_str = f"{price:.2f} {currency}"
        else:
            price_str = "Free"
        results.append({"appid": it["id"], "name": it["name"], "price": price_str})
    return results


def enrich_search_results(results: list[dict]) -> list[dict]:
    """Fetch release date and supported languages for each search result."""
    for game in results:
        try:
            details = get_app_details(game["appid"])
            if details:
                game["release_date"] = details.get("release_date", {}).get("date", "N/A")
                langs = details.get("supported_languages", "N/A")
                game["languages"] = _strip_html(langs) if langs else "N/A"
            else:
                game["release_date"] = "N/A"
                game["languages"] = "N/A"
        except Exception:
            game["release_date"] = "N/A"
            game["languages"] = "N/A"
    return results


def get_app_details(appid: int) -> dict | None:
    resp = _get(f"{BASE}/api/appdetails", params={"appids": appid, "l": "english", "cc": "IT"})
    payload = resp.json().get(str(appid), {})
    if not payload.get("success"):
        return None
    return payload["data"]


def parse_metadata(data: dict) -> dict:
    price_info = data.get("price_overview")
    if price_info:
        price_str = price_info.get("final_formatted", "N/A")
        if price_info.get("discount_percent", 0) > 0:
            price_str += f"  (-{price_info['discount_percent']}%  base: {price_info.get('initial_formatted', '')})"
    elif data.get("is_free"):
        price_str = "Free"
    else:
        price_str = "N/A"

    packages = []
    for pkg in data.get("package_groups", []):
        for sub in pkg.get("subs", []):
            packages.append(_strip_html(sub.get("option_text", "N/A")))

    return {
        "title": data.get("name", "N/A"),
        "description": _strip_html(
            data.get("detailed_description") or data.get("short_description") or "N/A"
        ),
        "release_date": data.get("release_date", {}).get("date", "N/A"),
        "developer": ", ".join(data.get("developers", ["N/A"])),
        "publisher": ", ".join(data.get("publishers", ["N/A"])),
        "tags": [g["description"] for g in data.get("genres", [])],
        "franchise": data.get("franchise", "N/A") if data.get("franchise") else "N/A",
        "price": price_str,
        "packages": packages,
        "requirements_min": _strip_html(
            data.get("pc_requirements", {}).get("minimum", "N/A")
            if isinstance(data.get("pc_requirements"), dict) else "N/A"
        ),
        "requirements_rec": _strip_html(
            data.get("pc_requirements", {}).get("recommended", "N/A")
            if isinstance(data.get("pc_requirements"), dict) else "N/A"
        ),
    }


def get_review_counts_by_language(appid: int) -> dict[str, dict]:
    """Return {lang_code: {"total": int, "desc": str}} for every language, fetched in parallel."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    lang_codes = list(STEAM_LANGUAGES.keys())

    def _fetch_count(lang: str) -> tuple[str, dict]:
        try:
            resp = _get(
                f"{BASE}/appreviews/{appid}",
                params={"json": 1, "language": lang, "purchase_type": "all",
                        "num_per_page": 0, "filter": "recent"},
            )
            qs = resp.json().get("query_summary", {})
            return lang, {
                "total": qs.get("total_reviews", 0),
                "desc": qs.get("review_score_desc", "N/A"),
            }
        except Exception:
            return lang, {"total": 0, "desc": "N/A"}

    counts = {}
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(_fetch_count, lang): lang for lang in lang_codes}
        for fut in as_completed(futures):
            lang, info = fut.result()
            counts[lang] = info
    return counts


def get_review_summary(appid: int) -> dict:
    resp = _get(
        f"{BASE}/appreviews/{appid}",
        params={"json": 1, "language": "all", "purchase_type": "all", "num_per_page": 0, "filter": "recent"},
    )
    summary = resp.json().get("query_summary", {})
    return {
        "total": summary.get("total_reviews", 0),
        "positive": summary.get("total_positive", 0),
        "negative": summary.get("total_negative", 0),
    }


def fetch_reviews(appid: int, language: str = "all", on_batch=None) -> list[dict]:
    cursor = "*"
    all_reviews: list[dict] = []
    total = None

    while True:
        resp = _get(
            f"{BASE}/appreviews/{appid}",
            params={
                "json": 1, "language": language, "purchase_type": "all",
                "num_per_page": 100, "filter": "recent", "cursor": cursor,
            },
        )
        body = resp.json()

        if total is None:
            total = body.get("query_summary", {}).get("total_reviews", 0)

        reviews = body.get("reviews", [])
        if not reviews:
            break

        for r in reviews:
            playtime_min = r["author"].get("playtime_forever", 0)
            all_reviews.append({
                "steam_id": r["author"]["steamid"],
                "author": r["author"].get("personaname", r["author"]["steamid"]),
                "review": r["review"],
                "review_type": "positive" if r["voted_up"] else "negative",
                "purchase_type": "steam" if r.get("steam_purchase") else "key/other",
                "language": r.get("language", "N/A"),
                "playtime": f"{playtime_min // 60}h {playtime_min % 60}m",
                "date": r["timestamp_created"],
            })

        new_cursor = body.get("cursor")
        if not new_cursor or new_cursor == cursor:
            break
        cursor = new_cursor

        if on_batch and total:
            on_batch(len(all_reviews), total)

    if on_batch and total:
        on_batch(len(all_reviews), total)

    return all_reviews
