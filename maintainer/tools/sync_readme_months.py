import argparse
import os
import re
import sys

MONTHS_BLOCK_RE = re.compile(
    r"(<!-- months -->\s*).*?(\s*<!-- /months -->)",
    re.DOTALL,
)

# Matches keys from month(...) in course_data.py, excluding buy, uses, builds, and stock
COLUMNS = [
    "n",
    "title",
    "theme",
    "host",
    "samples",
    "learn",
    "projects",
    "status",
]

UPPERCASE_COLS = {"host", "samples"}


def _find_month_folder(repo_root, n):
  prefix = f"month-{n:02d}-"
  for entry in sorted(os.listdir(repo_root)):
    full = os.path.join(repo_root, entry)
    if os.path.isdir(full) and entry.startswith(prefix):
      return entry
  return None


def _escape_cell(value):
  return str(value).replace("|", "\\|").replace("\n", " ").strip()


def _format_header(col):
  if not col:
    return ""
  return col[0].upper() + col[1:]


def _format_cell(item, col, repo_root):
  val = item.get(col)

  if col == "title":
    title = _escape_cell(val or "")
    n = item.get("n")
    if isinstance(n, int):
      folder = _find_month_folder(repo_root, n)
      if folder and os.path.isfile(
          os.path.join(repo_root, folder, "README.md")
      ):
        return f"[{title}]({folder}/README.md)"
    return title

  if isinstance(val, list):
    text = ", ".join(str(x) for x in val) if val else "—"
  elif val is None or val == "":
    text = "—"
  else:
    text = str(val)

  if col in UPPERCASE_COLS and text != "—":
    text = text.upper()

  return _escape_cell(text)


def render_plan_table(plan, repo_root, columns=COLUMNS):
  headers = [_format_header(col) for col in columns]
  header = "| " + " | ".join(headers) + " |"
  align = "| " + " | ".join("---" for _ in columns) + " |"
  rows = [header, align]

  for item in plan:
    cells = [_format_cell(item, col, repo_root) for col in columns]
    rows.append("| " + " | ".join(cells) + " |")

  return "\n".join(rows)


def sync_readme_from_plan(
    readme_path, plan, repo_root, check_only=False, columns=COLUMNS
):
  with open(readme_path, "r", encoding="utf-8", newline="") as f:
    raw = f.read()

  if not MONTHS_BLOCK_RE.search(raw):
    raise ValueError(
        f"Missing <!-- months --> ... <!-- /months --> markers in {readme_path}"
    )

  normalized = raw.replace("\r\n", "\n")
  table_md = render_plan_table(plan, repo_root, columns=columns)
  updated = MONTHS_BLOCK_RE.sub(
      lambda m: f"{m.group(1)}{table_md}{m.group(2)}",
      normalized,
      count=1,
  )
  changed = updated != normalized

  if changed and not check_only:
    with open(readme_path, "w", encoding="utf-8", newline="\n") as f:
      f.write(updated)

  return changed
  

def main():
  parser = argparse.ArgumentParser(
      description=(
          "Sync the course table in root README.md from course_data.PLAN."
      )
  )
  parser.add_argument(
      "--check",
      action="store_true",
      help="Check whether README.md is out of sync without writing changes.",
  )
  args = parser.parse_args()

  tools_dir = os.path.dirname(os.path.abspath(__file__))
  repo_root = os.path.abspath(os.path.join(tools_dir, "..", ".."))
  if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

  from course_data import PLAN

  readme_path = os.path.join(repo_root, "README.md")
  changed = sync_readme_from_plan(
      readme_path, PLAN, repo_root, check_only=args.check
  )

  if args.check:
    if changed:
      print(f"FAIL {readme_path} months table is out of sync with course_data.PLAN.")
      sys.exit(1)
    print(f"OK {readme_path} months table is in sync.")
    sys.exit(0)

  if changed:
    print(f"Updated {readme_path} ({len(PLAN)} months from PLAN).")
  else:
    print(f"No changes needed in {readme_path}.")


if __name__ == "__main__":
  main()
