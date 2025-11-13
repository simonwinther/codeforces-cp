# utilities/scripts/update_readme.py

import os

from util import (
    get_image,
    image_mapper,
    load_cached_difficulties,
    save_cached_difficulties,
    get_problem_info,
    generate_table_of_contents,
)

file_whitelist = {"bnn_accuracy.py", "testing_tool.py", "unununion_find.py"}

difficulty_cache = load_cached_difficulties()
contents = []

# Iterate through files in the 'solutions' directory
for file in sorted(os.listdir("solutions")):
    file_path = os.path.join("solutions", file)

    if not os.path.isfile(file_path):
        continue

    ext = file.split(".")[-1]
    if ext not in image_mapper:
        continue

    pid = file.rsplit(".", 1)[0]  # 'a_beautiful_matrix'
    repo_url = (
        "https://github.com/simonsejse/competitive-programming/tree/main/"
        f"solutions/{file}"
    )

    info = get_problem_info(pid, difficulty_cache)
    difficulty = info["difficulty"]
    codeforces_url = info["url"]
    cf_code = info["code"]   # e.g. "263A" or pid
    cf_title = info["name"]  # "A. Beautiful Matrix"

    image_icon = (
        f"[![{ext}]({get_image(ext)})]({file_path})"
        if file not in file_whitelist
        else ""
    )

    # pid used as sort key, row is markdown
    row = (
        f"|[{file}]({repo_url})| "
        f"[{cf_title}]({codeforces_url}) | "
        f"{difficulty} | "
        f"{image_icon}|\n"
    )
    contents.append([pid, row])

# Save the updated difficulties cache
save_cached_difficulties(difficulty_cache)

# ---------- Update the solved stats section ----------

with open("README.md", "r", encoding="utf8") as f:
    lines = f.readlines()

start_marker = "<!-- START_SOLVED_STATS -->"
end_marker = "<!-- END_SOLVED_STATS -->"

start_index = None
end_index = None
for i, line in enumerate(lines):
    if start_marker in line:
        start_index = i
    if end_marker in line:
        end_index = i
        break

if start_index is not None and end_index is not None:
    solved_section = [
        f"## Total problems solved: {len(contents)}\n\n",
        "Note that the table below is auto-generated. There might be slight inaccuracies.\n\n",
        "|Problem Name|Problem ID|Difficulty|Languages|\n",
        "|:---|:---|:---|:---|\n",
    ]

    # Sort by pid for stable ordering
    solved_section.extend([row for _, row in sorted(contents, key=lambda x: x[0])])

    lines = lines[: start_index + 1] + solved_section + lines[end_index:]

with open("README.md", "w", encoding="utf8") as f:
    f.writelines(lines)

# ---------- Update the Table of Contents ----------

with open("README.md", "r", encoding="utf8") as f:
    lines = f.readlines()

toc_start_marker = "<!-- START_TABLE_OF_CONTENTS -->"
toc_end_marker = "<!-- END_TABLE_OF_CONTENTS -->"

toc_start_index = None
toc_end_index = None
for i, line in enumerate(lines):
    if toc_start_marker in line:
        toc_start_index = i
    if toc_end_marker in line:
        toc_end_index = i
        break

table_of_contents = generate_table_of_contents(lines)

if toc_start_index is not None and toc_end_index is not None:
    lines = (
        lines[: toc_start_index + 1]
        + table_of_contents
        + lines[toc_end_index:]
    )

with open("README.md", "w", encoding="utf8") as f:
    f.writelines(lines)

