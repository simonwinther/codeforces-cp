# utilities/scripts/build_docs.py

from util import (
    get_image,
    load_cached_difficulties,
    save_cached_difficulties,
    prune_cached_difficulties,
    get_problem_info,
    iter_solution_files,
)

file_whitelist = {"bnn_accuracy.py", "testing_tool.py", "unununion_find.py"}


def build_problem_table():
    difficulty_cache = load_cached_difficulties()
    problem_rows = []
    active_pids = []

    for solution in iter_solution_files():
        file = solution["file"]
        ext = solution["ext"]
        pid = solution["pid"]
        repo_url = solution["repo_url"]

        info = get_problem_info(pid, difficulty_cache)
        difficulty = info["difficulty"]
        url = info["url"]
        name = info["name"]
        code = info["code"]

        active_pids.append(pid)

        # language icon
        lang_icon = ""
        if file not in file_whitelist:
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
        </tr>
"""
        problem_rows.append(row)

    prune_cached_difficulties(difficulty_cache, active_pids)
    save_cached_difficulties(difficulty_cache)
    return problem_rows


def insert_problems_into_html():
    with open("docs/index.html", "r", encoding="utf8") as f:
        html = f.read()

    start_marker = "<!-- START_PROBLEM -->"
    end_marker = "<!-- END_PROBLEM -->"

    if start_marker in html and end_marker in html:
        before_start, after_start = html.split(start_marker, 1)
        _, after_end = after_start.split(end_marker, 1)

        problem_rows = build_problem_table()
        html = (
            before_start
            + start_marker
            + "\n"
            + "".join(problem_rows)
            + "      "
            + end_marker
            + after_end
        )

    with open("docs/index.html", "w", encoding="utf8") as f:
        f.write(html)


if __name__ == "__main__":
    insert_problems_into_html()
