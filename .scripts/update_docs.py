# utilities/scripts/build_docs.py

import os

from util import (
    get_image,
    image_mapper,
    load_cached_difficulties,
    save_cached_difficulties,
    get_problem_info,
)

file_whitelist = {"bnn_accuracy.py", "testing_tool.py", "unununion_find.py"}


def build_problem_table():
    difficulty_cache = load_cached_difficulties()
    problem_rows = []

    # Iterate through files in the 'solutions' directory
    for file in sorted(os.listdir("solutions")):
        file_path = os.path.join("solutions", file)

        if not os.path.isfile(file_path):
            continue

        ext = file.split(".")[-1]
        if ext not in image_mapper:
            continue

        pid = file.rsplit(".", 1)[0]  # 'a_beautiful_matrix'

        info = get_problem_info(pid, difficulty_cache)
        difficulty = info["difficulty"]
        url = info["url"]
        name = info["name"]
        code = info["code"]

        # language icon
        lang_icon = ""
        if file not in file_whitelist:
            repo_url = (
                "https://github.com/simonwinther/codeforces-cp/tree/main/solutions/"
                f"{file}"
            )
            lang_icon = (
                f'<a href="{repo_url}" target="_blank">'
                f'<img alt="{ext}" src="{get_image(ext)}" /></a>'
            )


        row = f"""
        <tr>
            <td><a href="{url}">{name}</a></td>
            <td>{code}</td>
            <td>{difficulty}</td>
            <td class="language-icon">{lang_icon}</td>
        </tr>"""
        problem_rows.append(row)

    save_cached_difficulties(difficulty_cache)
    return problem_rows


def insert_problems_into_html():
    with open("docs/index.html", "r", encoding="utf8") as f:
        lines = f.readlines()

    start_marker = "<!-- START_PROBLEM -->"
    end_marker = "<!-- END_PROBLEM -->"

    start_index, end_index = None, None
    for i, line in enumerate(lines):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i
            break

    if start_index is not None and end_index is not None:
        problem_rows = build_problem_table()
        lines = lines[: start_index + 1] + problem_rows + lines[end_index:]

    with open("docs/index.html", "w", encoding="utf8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    insert_problems_into_html()

