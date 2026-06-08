local function to_solution_slug(problem_name)
  local slug = problem_name:lower()
  slug = slug:gsub("[^%w]+", "_")
  slug = slug:gsub("^_+", ""):gsub("_+$", "")
  return slug
end

local function received_problem_path(task, file_extension)
  local uv = vim.uv or vim.loop
  return string.format("%s/%s.%s", uv.cwd(), to_solution_slug(task.name), file_extension)
end

local function received_contest_problem_path(task, file_extension)
  return string.format("%s.%s", to_solution_slug(task.name), file_extension)
end

return {
  testcases_directory = ".testcases",
  testcases_input_file_format = "$(FNOEXT)_input$(TCNUM).txt",
  testcases_output_file_format = "$(FNOEXT)_output$(TCNUM).txt",
  testcases_single_file_format = "$(FNOEXT).testcases",
  received_files_extension = "cpp",
  received_problems_path = received_problem_path,
  received_problems_prompt_path = false,
  received_contests_directory = "$(CWD)",
  received_contests_problems_path = received_contest_problem_path,
  received_contests_prompt_directory = false,
  received_contests_prompt_extension = false,
}
