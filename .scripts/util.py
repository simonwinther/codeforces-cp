# util.py
import os
import json
import re
import time
from datetime import datetime
from urllib.parse import quote

import requests

# Constants
CACHE_EXPIRY_DAYS = 60
SOLUTIONS_DIR = "solutions"
REPO_BLOB_URL = "https://github.com/simonwinther/codeforces-cp/blob/HEAD"
CF_PROBLEMS_API_URL = "https://codeforces.com/api/problemset.problems"
CF_API_ATTEMPTS = 5
CF_API_TIMEOUT_SECONDS = 20
CF_API_HEADERS = {
    "User-Agent": (
        "codeforces-cp-metadata-updater/1.0 "
        "(+https://github.com/simonwinther/codeforces-cp)"
    )
}

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


def encode_path(path: str) -> str:
    return quote(path, safe="/")


# ---------- Solution discovery ----------

def iter_solution_files(solution_dir: str = SOLUTIONS_DIR):
    """
    Yield supported source files that count as solved problems.

    Draft files in the repository root are intentionally ignored; moving a file
    into solutions/ is the publishing step for README and docs generation.
    """
    if not os.path.isdir(solution_dir):
        return

    for file in sorted(os.listdir(solution_dir)):
        file_path = os.path.join(solution_dir, file)

        if not os.path.isfile(file_path):
            continue

        ext = file.rsplit(".", 1)[-1] if "." in file else ""
        if ext not in image_mapper:
            continue

        pid = file.rsplit(".", 1)[0]
        markdown_path = encode_path(file_path)
        repo_url = f"{REPO_BLOB_URL}/{markdown_path}"

        yield {
            "file": file,
            "file_path": file_path,
            "markdown_path": markdown_path,
            "pid": pid,
            "ext": ext,
            "repo_url": repo_url,
        }

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
        f.write("\n")


def prune_cached_difficulties(cache: dict, active_pids) -> None:
    active_pids = set(active_pids)
    for pid in list(cache):
        if pid not in active_pids:
            del cache[pid]

# ---------- Codeforces helpers ----------

_CF_PROBLEMS_BY_INDEX_AND_NAME = None  # (INDEX, norm_name) -> problem dict
_CF_PROBLEMS_LOAD_ERROR = None


def _normalize_name(name: str) -> str:
    """Lowercase, remove non-alphanumerics, collapse whitespace."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", " ", name)
    return " ".join(name.split())


def _parse_pid(pid: str):
    """
    From filename base like 'a_beautiful_matrix' or 'A. Beautiful Matrix' return:
      index = 'A'
      raw_name = 'beautiful matrix'
    If it doesn't match expected pattern, return (None, None).
    """
    base = pid.strip()  # pid is already without extension
    match = re.match(r"^([A-Za-z][A-Za-z0-9]{0,2})[\s._-]+(.+)$", base)
    if not match:
        return None, None

    index = match.group(1).upper()  # 'A'
    raw_name = re.sub(r"[\s._-]+", " ", match.group(2)).strip()
    return index, raw_name


def _load_codeforces_index_map():
    """
    Load Codeforces problems once and build a map:
      key: "INDEX::normalized_name"
      val: problem dict
    """
    global _CF_PROBLEMS_BY_INDEX_AND_NAME
    global _CF_PROBLEMS_LOAD_ERROR
    if _CF_PROBLEMS_BY_INDEX_AND_NAME is not None:
        return _CF_PROBLEMS_BY_INDEX_AND_NAME

    last_error = None
    for attempt in range(1, CF_API_ATTEMPTS + 1):
        try:
            resp = requests.get(
                CF_PROBLEMS_API_URL,
                headers=CF_API_HEADERS,
                timeout=CF_API_TIMEOUT_SECONDS,
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get("status") != "OK":
                raise RuntimeError("Codeforces API returned non-OK status.")

            break
        except Exception as e:
            last_error = e
            if attempt < CF_API_ATTEMPTS:
                time.sleep(min(2 ** (attempt - 1), 8))
    else:
        print(
            "Error fetching Codeforces problems after "
            f"{CF_API_ATTEMPTS} attempts: {last_error}"
        )
        _CF_PROBLEMS_BY_INDEX_AND_NAME = {}
        _CF_PROBLEMS_LOAD_ERROR = str(last_error)
        return _CF_PROBLEMS_BY_INDEX_AND_NAME

    _CF_PROBLEMS_LOAD_ERROR = None

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


def _get_fresh_cache_entry(pid: str, cache: dict) -> dict:
    entry = cache.get(pid)
    if not entry:
        return {}

    last_updated = entry.get("last_updated")
    if not last_updated:
        return {}

    try:
        last_updated_date = datetime.strptime(last_updated, "%Y-%m-%d")
    except ValueError:
        return {}

    if (datetime.now() - last_updated_date).days > CACHE_EXPIRY_DAYS:
        return {}

    return entry


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
    cached = cache.get(pid) or {}
    fresh_cached = _get_fresh_cache_entry(pid, cache)
    cached_difficulty = fresh_cached.get("difficulty")
    if cached_difficulty == "N/A":
        cached_difficulty = None

    problem, display_name, search_query = _find_problem_for_pid(pid)
    metadata_unavailable = _CF_PROBLEMS_LOAD_ERROR is not None
    should_update_cache = True

    if problem is not None:
        contest_id = problem.get("contestId")
        index = problem.get("index")
        rating = problem.get("rating")

        difficulty = str(rating) if rating is not None else cached_difficulty or "N/A"

        if contest_id is not None and index is not None:
            url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
            code = f"{contest_id}{index}"
        else:
            url = (
                cached.get("url")
                or f"https://codeforces.com/problemset?search={search_query}"
            )
            code = cached.get("code") or pid
    elif metadata_unavailable and all(cached.get(k) for k in ("name", "url", "code")):
        difficulty = cached_difficulty or cached.get("difficulty") or "N/A"
        display_name = cached["name"]
        url = cached["url"]
        code = cached["code"]
        should_update_cache = False
    else:
        if metadata_unavailable:
            raise RuntimeError(
                "Codeforces API is unavailable and no complete cached metadata "
                f"exists for {pid}; refusing to generate a fallback search URL."
            )

        difficulty = cached_difficulty or "N/A"
        url = f"https://codeforces.com/problemset?search={search_query or pid}"
        code = pid
        if display_name is None:
            # Fallback if parsing failed totally
            display_name = pid.replace("_", " ").title()

    # Update cache with complete metadata so future API outages do not rewrite
    # direct links back to search URLs.
    if should_update_cache:
        cache[pid] = {
            "difficulty": difficulty,
            "name": display_name,
            "url": url,
            "code": code,
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
