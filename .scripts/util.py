# util.py
import os
import json
import re
from datetime import datetime

import requests

# Constants
CACHE_EXPIRY_DAYS = 60

# Map extensions to languages
image_mapper = {
    "py": "python",
    "c": "c",
    "cpp": "cpp",
    "cs": "csharp",
    "go": "go",
    "hs": "haskell",
    "java": "java",
    "kt": "kotlin",
    "php": "php",
    "rb": "ruby",
    "js": "javascript",
}

# ---------- Icons ----------

def get_image(ext: str, size: int = 24) -> str:
    lang = image_mapper[ext]
    return (
        "https://raw.githubusercontent.com/abrahamcalf/"
        f"programming-languages-logos/master/src/{lang}/{lang}_{size}x{size}.png"
    )

# ---------- Cache helpers ----------

def get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def load_cached_difficulties(cache_file: str = "difficulty_cache.json") -> dict:
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error loading {cache_file}, resetting cache.")
            return {}
    return {}


def save_cached_difficulties(cache: dict, cache_file: str = "difficulty_cache.json") -> None:
    with open(cache_file, "w") as f:
        json.dump(cache, f, indent=4)

# ---------- Codeforces helpers ----------

_CF_PROBLEMS_BY_INDEX_AND_NAME = None  # (INDEX, norm_name) -> problem dict


def _normalize_name(name: str) -> str:
    """Lowercase, remove non-alphanumerics, collapse whitespace."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", " ", name)
    return " ".join(name.split())


def _parse_pid(pid: str):
    """
    From filename base like 'a_beautiful_matrix' return:
      index = 'A'
      raw_name = 'beautiful matrix'
    If it doesn't match expected pattern, return (None, None).
    """
    base = pid  # pid is already without extension
    parts = base.split("_")
    if len(parts) < 2:
        return None, None

    index = parts[0].upper()  # 'A'
    raw_name = " ".join(parts[1:])
    return index, raw_name


def _load_codeforces_index_map():
    """
    Load Codeforces problems once and build a map:
      key: "INDEX::normalized_name"
      val: problem dict
    """
    global _CF_PROBLEMS_BY_INDEX_AND_NAME
    if _CF_PROBLEMS_BY_INDEX_AND_NAME is not None:
        return _CF_PROBLEMS_BY_INDEX_AND_NAME

    url = "https://codeforces.com/api/problemset.problems"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"Error fetching Codeforces problems: {e}")
        _CF_PROBLEMS_BY_INDEX_AND_NAME = {}
        return _CF_PROBLEMS_BY_INDEX_AND_NAME

    if data.get("status") != "OK":
        print("Codeforces API returned non-OK status.")
        _CF_PROBLEMS_BY_INDEX_AND_NAME = {}
        return _CF_PROBLEMS_BY_INDEX_AND_NAME

    problems = data["result"]["problems"]
    mapping = {}

    for p in problems:
        idx = p.get("index")
        name = p.get("name")
        if not idx or not name:
            continue
        key = f"{idx.upper()}::{_normalize_name(name)}"
        mapping[key] = p

    _CF_PROBLEMS_BY_INDEX_AND_NAME = mapping
    return _CF_PROBLEMS_BY_INDEX_AND_NAME


def _find_problem_for_pid(pid: str):
    """
    Use filename-based pid (e.g., 'a_beautiful_matrix') to find the CF problem.
    """
    index, raw_name = _parse_pid(pid)
    if not index or not raw_name:
        return None, None, None  # problem, display_name, search_query

    norm_name = _normalize_name(raw_name)
    key = f"{index.upper()}::{norm_name}"

    mapping = _load_codeforces_index_map()
    problem = mapping.get(key)

    # Human display name like "A. Beautiful Matrix"
    pretty_name = " ".join(word.capitalize() for word in raw_name.split())
    display_name = f"{index}. {pretty_name}" if index else pretty_name

    # For a fallback search URL
    search_query = norm_name.replace(" ", "+")

    return problem, display_name, search_query


def get_problem_info(pid: str, cache: dict) -> dict:
    """
    Return a dict with information about a problem given a filename-style pid.

    pid: e.g. 'a_beautiful_matrix'

    Returns:
      {
        "difficulty": "800" or "N/A",
        "url": "<Codeforces URL or search URL>",
        "name": "A. Beautiful Matrix",
        "code": "263A" or pid (if unknown)
      }
    """
    # Difficulty from cache (if fresh)
    difficulty = None
    if pid in cache:
        last_updated = cache[pid].get("last_updated")
        if last_updated:
            last_updated_date = datetime.strptime(last_updated, "%Y-%m-%d")
            if (datetime.now() - last_updated_date).days <= CACHE_EXPIRY_DAYS:
                difficulty = cache[pid].get("difficulty")

    problem, display_name, search_query = _find_problem_for_pid(pid)

    if problem is not None:
        contest_id = problem.get("contestId")
        index = problem.get("index")
        rating = problem.get("rating")

        if difficulty is None:
            difficulty = str(rating) if rating is not None else "N/A"

        if contest_id is not None and index is not None:
            url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
            code = f"{contest_id}{index}"
        else:
            url = f"https://codeforces.com/problemset?search={search_query}"
            code = pid
    else:
        if difficulty is None:
            difficulty = "N/A"
        url = f"https://codeforces.com/problemset?search={search_query or pid}"
        code = pid
        if display_name is None:
            # Fallback if parsing failed totally
            display_name = pid.replace("_", " ").title()

    # Update cache with difficulty
    cache[pid] = {
        "difficulty": difficulty,
        "last_updated": get_current_date(),
    }

    return {
        "difficulty": difficulty,
        "url": url,
        "name": display_name,
        "code": code,
    }


def get_problem_difficulty(pid: str, cache: dict) -> str:
    """
    Backwards-compatible wrapper used in older scripts.
    """
    return get_problem_info(pid, cache)["difficulty"]

# ---------- TOC helpers ----------

def generate_slug(heading: str) -> str:
    heading = heading.replace("##", "").strip()
    heading = re.sub(r"[^\w\s-]", "", heading)
    return heading.lower().replace(" ", "-")


def generate_table_of_contents(lines):
    toc = ["## Table of Contents\n"]
    for line in lines:
        if line.startswith("## ") and not line.startswith("## Table of Contents"):
            heading_text = line.strip().replace("##", "").strip()
            heading_slug = generate_slug(heading_text)
            toc.append(f"- [{heading_text}](#{heading_slug})\n")
    return toc

