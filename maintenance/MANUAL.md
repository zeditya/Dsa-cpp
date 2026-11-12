# 📘 Repository Manual

> **This file is manually maintained.** `README.md` is auto-generated: never edit it directly.
> Source of truth for the README: **`maintenance/scripts/readme_template.md`**
> Source of truth for the data/settings: **`maintenance/scripts/config.json`**

---

## Table of Contents

1. [What this repository does](#1-what-this-repository-does)
2. [Repository map](#2-repository-map)
3. [Using this repo on a new device](#3-using-this-repo-on-a-new-device)
4. [Daily workflow](#4-daily-workflow)
5. [How the automation works](#5-how-the-automation-works)
6. [Changing the README](#6-changing-the-readme)
7. [Changing the dashboard and heatmap](#7-changing-the-dashboard-and-heatmap)
8. [Adding and organizing solutions](#8-adding-and-organizing-solutions)
9. [Adding or changing topics](#9-adding-or-changing-topics)
10. [Running the generator locally](#10-running-the-generator-locally)
11. [Workflow controls](#11-workflow-controls)
12. [Troubleshooting](#12-troubleshooting)
13. [Disabling or rolling back automation](#13-disabling-or-rolling-back-automation)
14. [Security notes](#14-security-notes)
15. [Quick reference](#15-quick-reference)

---

## 1. What this repository does

This repo is a **living DSA + C++ practice journal**:

- Every solution is stored as a normal source file.
- A Python script scans the repo, reads optional metadata headers, and computes:
  - total solutions
  - per-topic progress
  - difficulty counts
  - current and longest commit streak
  - active days
  - recent solutions
  - a 365-day commit heatmap
- The script regenerates:
  - `README.md`
  - `maintenance/assets/dashboard.svg`
  - `maintenance/assets/activity.svg`
- GitHub Actions runs the script:
  - on every push to `main`
  - daily at **00:15 IST** (`18:45 UTC`)
  - manually, from the Actions tab
- A second workflow generates the contribution-snake animation and publishes it to the `output` branch.

Push code, and the showcase updates itself.

---

## 2. Repository map

```text
Dsa-cpp/
├── README.md                        ← AUTO-GENERATED, do not edit
├── DSA/                             ← your data structures and algorithms work
├── CPP/                             ← your C++ notes and practice
├── maintenance/                     ← everything used to maintain the repo
│   ├── MANUAL.md                    ← this manual
│   ├── assets/
│   │   ├── dashboard.svg            ← AUTO-GENERATED dashboard
│   │   └── activity.svg             ← AUTO-GENERATED heatmap
│   ├── scripts/
│   │   ├── config.json              ← targets, topics, phases, timezone
│   │   ├── readme_template.md       ← edit this to change the README
│   │   └── update_readme.py         ← generator (no external dependencies)
│   └── templates/
│       └── solution.cpp             ← copy-paste solution template
├── .github/
│   └── workflows/
│       ├── update-readme.yml        ← rebuilds README and assets
│       └── snake.yml                ← generates snake SVGs on the output branch
└── .gitignore
```

The `maintenance/` folder is the only non-code folder at the root. Your own code
can live in `DSA/`, `CPP/`, or any folder structure you prefer.

Your actual solutions can live anywhere. Recommended:

```text
DSA/
├── Arrays/
├── Strings/
├── LinkedList/
├── StackQueue/
├── Trees/
├── Graphs/
├── DynamicProgramming/
├── Greedy/
├── Backtracking/
├── BinarySearch/
├── Hashing/
├── Heaps/
├── Tries/
├── Recursion/
├── BitManipulation/
├── Math/
├── Sorting/
├── SegmentTrees/
└── Misc/
CPP/
├── Basics/
├── OOP/
└── STL/
```

> The **folder name decides the topic** when no `Topic:` metadata is present.
> Recommended paths make classification effortless.

---

## 3. Using this repo on a new device

You need **Git**, **Python 3.9+**, and **GitHub CLI (`gh`)**.

### 3.1 Linux

```bash
sudo apt update
sudo apt install -y git python3 gh
```

If `gh` is not available in your distro's package manager, install the binary from
<https://github.com/cli/cli/releases>.

### 3.2 macOS

```bash
brew install git python gh
```

### 3.3 Windows

```powershell
winget install --id Git.Git -e
winget install --id GitHub.cli -e
winget install --id Python.Python.3.12 -e
```

Then use **Git Bash** or **PowerShell** for the commands below.

### 3.4 Clone the repo

```bash
git clone https://github.com/zeditya/Dsa-cpp.git
cd Dsa-cpp
```

### 3.5 Authenticate once

```bash
gh auth login
```

Choose:

- **GitHub.com**
- **HTTPS**
- **Login with a web browser**
- Authorize GitHub CLI

Then connect Git to the stored credential:

```bash
gh auth setup-git
```

Verify:

```bash
gh auth status
git push
```

> The credential is stored in your OS keyring after this. Future `git push`
> commands should not ask for a username or password.

### 3.6 If you plan to edit workflow files

Pushing changes to `.github/workflows/*` requires the **`workflow`** scope.
Grant it once:

```bash
gh auth refresh --hostname github.com --scopes workflow
```

Complete the browser/device authorization. Verify:

```bash
gh auth status
```

You should see `workflow` in the token scopes.

### 3.7 Alternative: SSH

If you prefer SSH:

```bash
ssh-keygen -t ed25519 -C "adityabahuguna098@gmail.com"
cat ~/.ssh/id_ed25519.pub
```

Add the public key to **GitHub → Settings → SSH and GPG keys → New SSH key**.
Then:

```bash
git remote set-url origin git@github.com:zeditya/Dsa-cpp.git
ssh -T git@github.com
git push
```

### 3.8 Alternative: Personal Access Token

Use this only if you do not want to use GitHub CLI.

1. GitHub → **Settings → Developer settings → Personal access tokens**
2. Create a token:
   - **Fine-grained token**: repository access `Dsa-cpp`, permissions **Contents: Read and write** and **Workflows: Read and write**.
   - **Classic token**: scopes `repo` and `workflow`.
3. Store it with a credential helper:

```bash
git config --global credential.helper store
git push
# Username: zeditya
# Password: <paste token>
```

`credential.helper store` saves the token in plain text at `~/.git-credentials`.
For better security, use `gh` or your OS keyring instead.

---

## 4. Daily workflow

```bash
cd ~/Practice/Dsa-cpp
git pull --rebase
# add or edit solutions
git add .
git commit -m "solve: two sum"
git push
```

That's it. On push:

1. `Update README` recalculates every statistic.
2. `README.md`, `maintenance/assets/dashboard.svg`, and `maintenance/assets/activity.svg` are committed by the bot.
3. `Generate Snake` refreshes the `output` branch.

> Pull before starting work. The bot commits to `README.md` and `maintenance/assets/`, so a
> `git pull --rebase` avoids unnecessary conflicts.

---

## 5. How the automation works

### 5.1 `Update README`

File: `.github/workflows/update-readme.yml`

Triggers:

- push to `main` (except changes only under `README.md`, `maintenance/assets/**`, `output/**`)
- daily at `18:45 UTC` = `00:15 IST`
- manual `workflow_dispatch`

Steps:

1. Check out with `fetch-depth: 0` (full history is needed for streak/heatmap data).
2. Install Python 3.12.
3. Run `python maintenance/scripts/update_readme.py`.
4. Commit `README.md` and `maintenance/assets/` with `[skip ci]`.
5. Push using the workflow's `GITHUB_TOKEN`.

The `paths-ignore` and `[skip ci]` prevent an infinite workflow loop.

### 5.2 `Generate Snake`

File: `.github/workflows/snake.yml`

Triggers:

- daily at `00:00 UTC`
- push to `main`
- manual `workflow_dispatch`

It uses `platane/snk/svg-only@v3` to build:

```text
output/github-contribution-grid-snake.svg
output/github-contribution-grid-snake-dark.svg
```

and publishes them to the `output` branch with `crazy-max/ghaction-github-pages@v4`.

The README embeds those files from:

```text
https://raw.githubusercontent.com/zeditya/Dsa-cpp/output/github-contribution-grid-snake.svg
https://raw.githubusercontent.com/zeditya/Dsa-cpp/output/github-contribution-grid-snake-dark.svg
```

> The first snake appears after the workflow finishes. If the image is broken
> immediately after setup, run **Actions → Generate Snake → Run workflow** once.

---

## 6. Changing the README

### 6.1 The golden rule

**Edit `maintenance/scripts/readme_template.md`, not `README.md`.**

`README.md` is overwritten on every push. Changes made directly to it will be
lost the next time the workflow runs.

### 6.2 Change text, headings, quotes, or links

Edit `maintenance/scripts/readme_template.md` directly. Examples:

- intro paragraph
- “Hey, I'm Aditya” section
- mission table
- “The Long Game” section
- footer quote
- social links
- badges
- section order

Then either:

```bash
python3 maintenance/scripts/update_readme.py
git add README.md maintenance/assets/ maintenance/scripts/readme_template.md
git commit -m "docs: update README copy"
git push
```

or just push the template change and let the Action regenerate it.

### 6.3 Add a new static section

Add normal Markdown to `maintenance/scripts/readme_template.md`:

```markdown
## 🎧 What I'm Listening To

Lo-fi beats and compiler errors.
```

No Python changes are needed for static content.

### 6.4 Add a dynamic section

Use a placeholder in the template:

```markdown
## 📌 Current Focus

{{CURRENT_FOCUS}}
```

Then add the value to the `replacements` dictionary in
`maintenance/scripts/update_readme.py` inside `build_readme()`:

```python
"{{CURRENT_FOCUS}}": build_current_focus(stats),
```

If the placeholder is not replaced, the script exits with:

```text
Unresolved template placeholders: {{YOUR_PLACEHOLDER}}
```

That safety check prevents a broken README from being committed.

### 6.5 Available placeholders

| Placeholder | Value |
| :--- | :--- |
| `{{USERNAME}}` | GitHub username from `config.json` |
| `{{REPO}}` | Repository name |
| `{{REPO_URL}}` | Full repository URL |
| `{{LAST_UPDATED}}` | Generator timestamp |
| `{{CURRENT_FOCUS}}` | Topic of the most recently added solution |
| `{{STAT_BADGES}}` | Generated shields.io stat badges |
| `{{TOPIC_TARGET}}` | Soft goal per topic |
| `{{TOPIC_TABLE}}` | Topic progress table |
| `{{NEXT_MILESTONE}}` | Next 50-solution milestone |
| `{{TOTAL_SOLUTIONS}}` | Total tracked code files |
| `{{TARGET_PROBLEMS}}` | Overall target |
| `{{PROGRESS_PCT}}` | Overall percentage |
| `{{RECENT_TABLE}}` | Last 8 solutions |
| `{{ROADMAP}}` | Auto-checked phase checklist |
| `{{LEETCODE_SECTION}}` | Optional LeetCode card |

> The default README is intentionally concise for recruiters. The topic table,
> roadmap, and long automation explainer are available as placeholders, but the
> default template keeps them out and lets the dashboard carry that information.
> Add them back if you want a more detailed profile.

### 6.6 Change the header banner

The banner uses `capsule-render`:

```html
<img src="https://capsule-render.vercel.app/api?type=waving&color=...&text=DSA%20%C3%97%20C%2B%2B..." />
```

Edit the query string in `maintenance/scripts/readme_template.md`.

Useful parameters:

| Parameter | Meaning |
| :--- | :--- |
| `type=waving` | Waving banner |
| `color=0:hex,100:hex` | Gradient stops |
| `height=240` | Banner height |
| `text=...` | Main text (URL-encoded) |
| `fontSize=72` | Text size |
| `animation=fadeIn` | Animation |
| `desc=...` | Subtitle |
| `descAlignY=56` | Subtitle position |

### 6.7 Change the typing animation

Edit the `readme-typing-svg` URL in the template:

```text
https://readme-typing-svg.demolab.com?font=JetBrains+Mono&...
```

Separate lines with `;` and URL-encode spaces as `+` or `%20`.

### 6.8 Change badges

Add or edit shields.io images in the template:

```markdown
![Label](https://img.shields.io/badge/Label-Value-COLOR?style=for-the-badge&logo=LOGO)
```

The generated stat badges come from `build_stat_badges()` in
`maintenance/scripts/update_readme.py` if you want to change their colors or labels.

### 6.9 Change the GitHub stats cards

The default template uses these external images:

- `github-readme-stats.vercel.app` for the main stats card
- `github-readme-stats.vercel.app` for top languages
- `skillicons.dev` for the tech stack

Change the query parameters (`theme=tokyonight`, `hide_border=true`, etc.) or
remove the sections entirely.

The streak and trophy cards are not part of the default design, which keeps the
profile focused. You can add them back from `streak-stats.demolab.com` or
`github-profile-trophy.vercel.app` if you want them.

> If one of these services is rate-limited or down, the image may fail to load.
> The custom `maintenance/assets/dashboard.svg` and `maintenance/assets/activity.svg` do not depend on
> them.

### 6.10 Change the snake section

The snake is embedded from the `output` branch. If you rename the repo or
username, update `maintenance/scripts/config.json`; the template uses
`{{USERNAME}}` and `{{REPO}}`.

To change colors, edit the `outputs` line in `.github/workflows/snake.yml`:

```yaml
output/github-contribution-grid-snake-dark.svg?palette=github-dark
```

Available palettes are documented by `platane/snk`.

### 6.11 Remove a section

Delete it from `maintenance/scripts/readme_template.md`. If it was a dynamic section, you can
also remove its placeholder and the corresponding entry in `build_readme()`.

### 6.12 Reorder sections

Cut and paste sections in `maintenance/scripts/readme_template.md`. Keep the
`<!-- AUTO-GENERATED -->` comment at the top.

---

## 7. Changing the dashboard and heatmap

These are generated by `maintenance/scripts/update_readme.py`.

### 7.1 Dashboard layout

Function: `render_dashboard(stats)`

- Canvas: `1200 × 780`
- Header pill + title
- Four stat cards: solutions, current streak, topics, active days
- Overall progress bar
- Two-column topic coverage grid
- Footer with last-updated timestamp and repo URL

Common edits:

| Change | Where |
| :--- | :--- |
| Title text | `"DSA Progress, Visualized."` |
| Subtitle | `f"Auto-generated from commits  ·  github.com/..."` |
| Card labels | `cards = [...]` |
| Card colors | Last value of each `cards` tuple |
| Overall bar gradient | `<linearGradient id="bar">` |
| Background gradient | `<linearGradient id="bg">` |
| Accent line | `<rect ... fill="url(#accent)">` |
| Topic bar colors | `["#22d3ee", "#2dd4bf", "#a78bfa", "#4ade80"]` |
| Topic grid columns | `per_column = math.ceil(len(topics) / 2)` |
| Footer text | Bottom `svg_text(...)` calls |

### 7.2 Heatmap layout

Function: `render_activity(stats)`

- Canvas: `1200 × 340`
- Last 365 days
- 53-week grid, Sunday-first
- Month labels, weekday labels, legend
- Commit counts per day

Common edits:

| Change | Where |
| :--- | :--- |
| Title | `"A year of consistent practice."` |
| Cell size / gap | `cell, gap = 13, 4` |
| Grid position | `grid_x, grid_y = 120, 160` |
| Heatmap colors | `level_colors = [...]` |
| Legend position | `legend_x`, `legend_y` |
| Footer text | Bottom `svg_text(...)` calls |

> Keep the SVG free of JavaScript and `<foreignObject>` if you want GitHub to
> render it reliably. Plain shapes, text, gradients, and filters are safe.

### 7.3 Change where assets are written

In `main()`:

```python
(ASSETS_DIR / "dashboard.svg").write_text(...)
(ASSETS_DIR / "activity.svg").write_text(...)
```

If you rename them, update the template image paths and the workflow's
`git add README.md maintenance/assets/`.

### 7.4 Add a completely new generated asset

1. Write a `render_*.svg` function.
2. Call it in `main()` and write the file under `maintenance/assets/`.
3. Embed it in `maintenance/scripts/readme_template.md`.
4. Ensure the workflow commits it (`git add README.md maintenance/assets/` already covers `maintenance/assets/`).
5. Run locally to verify.

---

## 8. Adding and organizing solutions

### 8.1 Create a solution file

```bash
mkdir -p DSA/Arrays
cp maintenance/templates/solution.cpp DSA/Arrays/0001-two-sum.cpp
```

Use any of these naming styles:

```text
0001-two-sum.cpp
two-sum.cpp
TwoSum.cpp
```

Numbers sort nicely. The script strips leading numbers for display titles.

### 8.2 Recommended metadata header

```cpp
/*
 * Problem   : 0001. Two Sum
 * Topic     : Arrays
 * Difficulty: Easy        // Easy | Medium | Hard
 * Link      : https://leetcode.com/problems/two-sum/
 * Time      : O(n)
 * Space     : O(n)
 *
 * Approach:
 *   Store each number's complement in a hash map while scanning.
 */
```

The parser accepts these keys:

| Key | Aliases | Example |
| :--- | :--- | :--- |
| Problem | Title, Question | `0001. Two Sum` |
| Topic | Category, Tags | `Arrays` |
| Difficulty | Level | `Easy` |
| Link | URL, Problem Link | `https://...` |
| Time | Time Complexity | `O(n)` |
| Space | Space Complexity | `O(n)` |

It reads the first **80 lines** and supports `//`, `#`, `/* ... */`, `*`, and
`<!-- ... -->` comment styles.

### 8.3 How topic detection works

Priority order:

1. **Metadata `Topic:`**: exact match to a topic name or keyword.
2. **Folder name**: exact match to a topic name or keyword.
3. **Keyword search**: longest matching keyword across the path and filename.
4. **Fallback**: `Misc`.

Examples:

| Path | Topic |
| :--- | :--- |
| `DSA/Arrays/0001-two-sum.cpp` | Arrays |
| `DSA/DP/knapsack.cpp` | Dynamic Programming |
| `DSA/SegmentTrees/range-sum.cpp` | Segment Trees |
| `DSA/Trees/bst.cpp` | Trees & BST |
| `CPP/STL/vector.cpp` | C++ & STL |
| `random.cpp` | Misc |

If a file is misclassified, add an explicit `Topic:` header or move it into the
right folder.

### 8.4 Multiple topics in one file

Only the **first** recognised topic is counted:

```cpp
// Topic: Arrays, Two Pointers
```

This file is counted under **Arrays** only. This keeps total counts accurate.

### 8.5 Adding notes or non-solution files

The script counts every file with an allowed extension. To keep notes out of the
stats:

- put them under `maintenance/` or another excluded folder such as `docs/`, or
- use a non-code extension such as `.md`, or
- add the folder to `exclude_dirs` in `maintenance/scripts/config.json`.

### 8.6 Adding another language

Add the extension to `code_extensions`:

```json
"code_extensions": [".cpp", ".py", ".java", ".go", ".rs"]
```

The dashboard counts it as a solution. The language badge is not displayed by
default; add one in the template if desired.

### 8.7 Excluding folders

In `maintenance/scripts/config.json`:

```json
"exclude_dirs": [".git", ".github", ".vscode", ".idea", "maintenance", "scripts", "templates", "assets", "docs", "build", "bin", "node_modules"]
```

This matches **any path segment** with that exact name. It is not a glob.

> There is no per-file exclusion yet. To skip files starting with `_`, add a
> condition in `iter_code_files()`.

---

## 9. Adding or changing topics

### 9.1 Add a new topic

In `maintenance/scripts/config.json`, add an object to `topics`:

```json
{
  "name": "Union Find",
  "icon": "🔗",
  "match": ["unionfind", "disjointset", "dsu"]
}
```

Then add it to a phase if you want it on the roadmap:

```json
{
  "name": "Phase 3 · Algorithms",
  "topics": ["Recursion", "Backtracking", "Greedy", "Graphs", "Dynamic Programming", "Union Find"]
}
```

Run:

```bash
python3 maintenance/scripts/update_readme.py
```

The dashboard, topic table, and roadmap pick it up automatically.

### 9.2 Rename a topic

1. Change `name` in `config.json`.
2. Update its entry in `phases`.
3. Keep the old keyword in `match` if you want existing folders to keep working,
   or rename the folder too.

### 9.3 Remove a topic

1. Remove it from `topics`.
2. Remove it from `phases`.
3. Existing files fall back to `Misc` unless their folder/metadata matches
   another topic.

### 9.4 Change per-topic goal

```json
"topic_target": 25
```

This controls the progress bars in the topic table and dashboard. It does not
cap the count.

### 9.5 Change overall target

```json
"target_problems": 500
```

This controls the overall progress bar and next milestone.

### 9.6 Change timezone

```json
"timezone": "Asia/Kolkata"
```

This affects “today” for streaks and the timestamps in the generated SVGs.
Use any IANA timezone name.

### 9.7 Enable the LeetCode card

```json
"leetcode_username": "your-leetcode-username",
"show_leetcode_card": true
```

The card comes from `leetcard.jacoblin.cool`. If that service is unavailable,
set `show_leetcode_card` back to `false`.

### 9.8 Change phases

Edit the `phases` array. Topic names must match `topics[].name` exactly.
The roadmap shows one checkbox per topic and auto-checks it when the topic has
at least one solution.

---

## 10. Running the generator locally

```bash
python3 maintenance/scripts/update_readme.py
```

It prints something like:

```text
Rebuilt README.md, maintenance/assets/dashboard.svg and maintenance/assets/activity.svg
(14 solutions, 10/22 topics, 3d streak).
```

The script uses only the Python standard library. No `pip install` is needed.

Requirements:

- Python 3.9+
- a Git repository with history (full clone is best)
- `git` on PATH

> If you run it in a shallow clone, streak/heatmap history may be incomplete.
> GitHub Actions uses `fetch-depth: 0` for this reason.

Preview the SVGs:

```bash
# Linux, if ImageMagick is installed
magick maintenance/assets/dashboard.svg /tmp/dashboard.png
magick maintenance/assets/activity.svg /tmp/activity.png
```

Or open them directly in a browser.

---

## 11. Workflow controls

### 11.1 Run manually

GitHub → **Actions** → **Update README** → **Run workflow**.

For the snake:

GitHub → **Actions** → **Generate Snake** → **Run workflow**.

### 11.2 View status from the terminal

```bash
gh run list --repo zeditya/Dsa-cpp --limit 10
gh run view <RUN_ID> --repo zeditya/Dsa-cpp --log
```

### 11.3 Change the daily schedule

Cron is in **UTC**.

```yaml
schedule:
  - cron: "45 18 * * *"
```

`18:45 UTC` = `00:15 IST` next day.

Examples:

| IST time | UTC cron |
| :--- | :--- |
| 00:15 | `45 18 * * *` |
| 06:00 | `30 0 * * *` |
| 12:00 | `30 6 * * *` |
| 21:00 | `30 15 * * *` |

Use <https://crontab.guru> for other times.

### 11.4 Change when the README workflow runs

In `.github/workflows/update-readme.yml`:

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: "45 18 * * *"
  workflow_dispatch:
```

You can add `paths` / `paths-ignore` filters, but keep `README.md`,
`maintenance/assets/**`, and `output/**` ignored to prevent loops.

### 11.5 Disable the daily refresh but keep push refresh

Remove the `schedule:` block from `update-readme.yml`.

### 11.6 Stop bot commits from creating noise

Options:

1. Remove the `schedule:` block (push-only updates).
2. Remove `{{LAST_UPDATED}}` from the template so identical runs produce no diff.
3. Run weekly instead of daily.

If you remove `[skip ci]` or the `paths-ignore` filters, the bot commit will
trigger the workflow again and create a loop. Do not remove them casually.

### 11.7 Change the snake palette

Edit `.github/workflows/snake.yml`:

```yaml
output/github-contribution-grid-snake-dark.svg?palette=github-dark
```

Other palettes are supported by `platane/snk`.

---

## 12. Troubleshooting

### 12.1 `Invalid username or token. Password authentication is not supported`

GitHub no longer accepts account passwords for Git.

Fix:

```bash
gh auth login
gh auth setup-git
```

Or use a PAT as the password. Never use your GitHub account password.

### 12.2 `refusing to allow an OAuth App to create or update workflow ... without workflow scope`

Your token lacks the `workflow` scope.

Fix:

```bash
gh auth refresh --hostname github.com --scopes workflow
```

Complete the authorization, then push again.

### 12.3 `git push` keeps asking for credentials

Check:

```bash
gh auth status
git config --global --get-regexp credential
```

You should see:

```text
credential.https://github.com.helper !/home/aditya/.local/bin/gh auth git-credential
```

If not:

```bash
gh auth setup-git
```

### 12.4 The Actions tab shows no runs

- Check **Settings → Actions → General → Allow all actions and reusable workflows**.
- Check the workflow file is on the default branch (`main`).
- Check the YAML is valid.
- Push a commit that changes a non-ignored path.

### 12.5 The workflow runs but cannot push

- **Settings → Actions → General → Workflow permissions** → **Read and write permissions**.
- Ensure `.github/workflows/update-readme.yml` has `permissions: contents: write`.
- Check branch protection rules.

### 12.6 The README was overwritten

That is expected if you edited `README.md` directly. Restore your changes into
`maintenance/scripts/readme_template.md`, then run:

```bash
python3 maintenance/scripts/update_readme.py
git add README.md maintenance/assets/ maintenance/scripts/readme_template.md
git commit -m "docs: restore README design"
git push
```

### 12.7 The snake image is broken

1. Run **Actions → Generate Snake → Run workflow**.
2. Check the `output` branch exists.
3. Verify these URLs return 200:

```text
https://raw.githubusercontent.com/zeditya/Dsa-cpp/output/github-contribution-grid-snake.svg
https://raw.githubusercontent.com/zeditya/Dsa-cpp/output/github-contribution-grid-snake-dark.svg
```

4. Ensure `permissions: contents: write` is present in `snake.yml`.

### 12.8 External GitHub cards do not load

Services like `github-readme-stats`, `streak-stats`, and `github-profile-trophy`
can be rate-limited or temporarily down. The custom dashboard and heatmap still
work. You can remove those sections from the template if you want a fully
self-hosted README.

### 12.9 Stats are zero even though files exist

Check:

- File extension is in `code_extensions`.
- Folder is not in `exclude_dirs`.
- The file is inside the repo, not a submodule.
- Run locally and read the printed count:

```bash
python3 maintenance/scripts/update_readme.py
```

### 12.10 A solution is in the wrong topic

Add an explicit header:

```cpp
// Topic: Graphs
```

or move it into the matching folder. Exact folder names win. Keyword matching
uses the longest match, so `SegmentTrees` beats `Trees`.

### 12.11 Recent solutions order looks wrong

The order comes from the commit that **added** the file, not the file's modified
time. Uncommitted files use filesystem mtime as a fallback. Commit files to get
stable dates.

### 12.12 Streak is wrong

Streaks are based on commit dates in the configured timezone. The current streak
allows “today or yesterday” so the streak does not break before you commit.
Longest streak is computed from all commit days.

> The bot's own README commits are authored by `github-actions[bot]`, so they
> should not inflate your personal contribution graph. They may still appear in
> the repository's commit history and heatmap.

### 12.13 The bot commit conflicts with my local changes

Pull with rebase before pushing:

```bash
git pull --rebase
git push
```

If there is a conflict in `README.md` or `maintenance/assets/`, discard your local generated
files and regenerate:

```bash
git checkout --theirs README.md maintenance/assets/
# or
git restore --source=origin/main README.md maintenance/assets/
python3 maintenance/scripts/update_readme.py
```

For template conflicts, resolve `maintenance/scripts/readme_template.md` manually.

### 12.14 The generator fails with unresolved placeholders

You used a `{{PLACEHOLDER}}` in the template without adding it to
`build_readme()` in `maintenance/scripts/update_readme.py`.

Either add the replacement or remove the placeholder.

### 12.15 The generator fails in Actions but works locally

- Ensure the action checks out with `fetch-depth: 0`.
- Ensure Python 3.12 is installed by `actions/setup-python`.
- Check the workflow log:

```bash
gh run view <RUN_ID> --repo zeditya/Dsa-cpp --log
```

### 12.16 Unicode / emoji looks broken in the SVG

Use a font stack that exists on GitHub's image renderer. The script uses:

```text
Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif
```

If you add new symbols, test the rendered SVG in a browser.

---

## 13. Disabling or rolling back automation

### 13.1 Temporarily disable a workflow

GitHub → **Actions** → select workflow → **⋯** → **Disable workflow**.

### 13.2 Delete the automation entirely

```bash
git rm .github/workflows/update-readme.yml .github/workflows/snake.yml
git commit -m "chore: remove README automation"
git push
```

You can keep the generated README and assets; they are normal files.

### 13.3 Revert to a previous README

```bash
git log --oneline -- README.md
git checkout <COMMIT> -- README.md maintenance/assets/
git commit -m "docs: restore previous README"
git push
```

### 13.4 Start over

```bash
git checkout <COMMIT> -- maintenance/scripts/ maintenance/assets/ README.md
python3 maintenance/scripts/update_readme.py
git add README.md maintenance/assets/ maintenance/scripts/
git commit -m "docs: rebuild README system"
git push
```

---

## 14. Security notes

- Never commit a Personal Access Token, `~/.git-credentials`, or `GH_TOKEN`.
- Prefer `gh auth login` with the OS keyring.
- If a token leaks, revoke it immediately:
  **GitHub → Settings → Developer settings → Personal access tokens**.
- The workflow uses the ephemeral `GITHUB_TOKEN`, not your personal token.
- The `workflow` scope is powerful: it allows changing Actions files. Grant it
  only when needed.
- External README images (stats cards, trophies) are third-party requests. If you
  care about privacy, remove those sections and keep only the self-generated SVGs.

---

## 15. Quick reference

### Most-used commands

```bash
# daily
git pull --rebase
git add .
git commit -m "solve: problem name"
git push

# run generator locally
python3 maintenance/scripts/update_readme.py

# verify auth
gh auth status

# add workflow permission
gh auth refresh --hostname github.com --scopes workflow

# list workflow runs
gh run list --repo zeditya/Dsa-cpp --limit 10

# trigger manually
gh workflow run update-readme.yml --repo zeditya/Dsa-cpp
gh workflow run snake.yml --repo zeditya/Dsa-cpp
```

### Files you should edit

| Goal | File |
| :--- | :--- |
| Change README text/design | `maintenance/scripts/readme_template.md` |
| Change targets/topics/phases/timezone | `maintenance/scripts/config.json` |
| Change dashboard/heatmap visuals | `maintenance/scripts/update_readme.py` |
| Add a solution | `DSA/<Topic>/...` |
| Change automation schedule | `.github/workflows/update-readme.yml` |
| Change snake settings | `.github/workflows/snake.yml` |
| Document a new workflow | `maintenance/MANUAL.md` (this file) |

### Files you should not edit

| File | Why |
| :--- | :--- |
| `README.md` | Regenerated on every push |
| `maintenance/assets/dashboard.svg` | Regenerated by the script |
| `maintenance/assets/activity.svg` | Regenerated by the script |

---

<div align="center">

**Keep the streak alive. 🚀**

</div>
