# 📘 Repository Manual

> **This file is manually maintained.** `README.md` is auto-generated: never edit it directly.
> Source of truth for the README: **`.github/readme/scripts/readme_template.md`**
> Source of truth for the data/settings: **`.github/readme/scripts/config.json`**

---

## Table of Contents

1. [What this repository does](#1-what-this-repository-does)
2. [Repository map](#2-repository-map)
3. [Using this repo on a new device](#3-using-this-repo-on-a-new-device)
4. [Daily workflow](#4-daily-workflow)
5. [How the automation works](#5-how-the-automation-works)
6. [Changing the README](#6-changing-the-readme)
7. [Changing the visual assets](#7-changing-the-visual-assets)
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
  - a Striver A2Z step tracker based on topic coverage
  - problem, streak, and skill milestones
  - an eight-week activity log from git history
  - a live repo tree
  - an optional contest log from `.github/readme/scripts/contests.json`
- Automation commits are excluded from streaks, heatmaps, and the weekly log, so the numbers reflect your work and not the bot.
- The script regenerates:
  - `README.md`
  - `.github/readme/assets/hero.svg`
  - `.github/readme/assets/dashboard.svg`
  - `.github/readme/assets/activity.svg`
  - `.github/readme/assets/divider.svg`
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
├── .github/
│   ├── readme/                      ← all tooling, hidden inside .github
│   │   ├── MANUAL.md                ← this manual
│   │   ├── assets/
│   │   │   ├── hero.svg             ← AUTO-GENERATED header banner
│   │   │   ├── dashboard.svg        ← AUTO-GENERATED dashboard
│   │   │   ├── activity.svg         ← AUTO-GENERATED heatmap
│   │   │   ├── divider.svg          ← AUTO-GENERATED Pac-Man divider
│   │   │   └── grind.gif            ← the one pop culture GIF in the README
│   │   ├── scripts/
│   │   │   ├── config.json          ← targets, topics, steps, timezone
│   │   │   ├── contests.example.json ← copy to contests.json for the log
│   │   │   ├── readme_template.md   ← edit this to change the README
│   │   │   └── update_readme.py     ← generator (no external dependencies)
│   │   └── templates/
│   │       └── solution.cpp         ← copy-paste solution template
│   └── workflows/
│       ├── update-readme.yml        ← rebuilds README and assets
│       └── snake.yml                ← generates snake SVGs on the output branch
└── .gitignore
```

The root is intentionally clean. `README.md`, `DSA/`, and `CPP/` are the only
visible content. All tooling lives inside `.github/readme/`, which is GitHub's
standard infrastructure folder and does not clutter the profile.

Unused GIFs and the original Claude draft are archived outside the repository on
your computer:

```text
~/Practice/Dsa-cpp-archive/
├── alternates/                      ← GIFs not used by the README
└── reference/claude-readme.md       ← original draft
```

They are not tracked, not downloaded, and never affect the repo size.

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
2. `README.md` and every file under `.github/readme/assets/` are committed by the bot.
3. `Generate Snake` refreshes the `output` branch.

> Pull before starting work. The bot commits to `README.md` and `.github/readme/assets/`, so a
> `git pull --rebase` avoids unnecessary conflicts.

---

## 5. How the automation works

### 5.1 `Update README`

File: `.github/workflows/update-readme.yml`

Triggers:

- push to `main` (except changes only under `README.md`, `.github/readme/assets/**`, `.github/readme/MANUAL.md`, `output/**`)
- daily at `18:45 UTC` = `00:15 IST`
- manual `workflow_dispatch`

Steps:

1. Check out with `fetch-depth: 0` (full history is needed for streak/heatmap data).
2. Install Python 3.12.
3. Run `python .github/readme/scripts/update_readme.py`.
4. Commit `README.md` and `.github/readme/assets/` with `[skip ci]`.
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

### 5.3 What the generator computes

`.github/readme/scripts/update_readme.py` builds every dynamic part of the README:

| Section | Source |
| :--- | :--- |
| Hero banner | `.github/readme/assets/hero.svg` |
| Goal table | First commit date and `config.json` |
| Overall progress | Solution count and `target_problems` |
| Stats at a glance | Solution files and difficulty metadata |
| Dashboard | Topic counts, streaks, active days |
| Striver A2Z tracker | `striver_steps` in `config.json` plus topic counts |
| Milestones | Problem count, best streak, topic counts, contest data |
| Recent work | Newest solution files and metadata |
| Weekly log | Git history, last eight weeks |
| Heatmap | Git history, last 365 days |
| Repo tree | Real top-level folders and solution counts |
| Contest log | Optional `.github/readme/scripts/contests.json` |

### 5.4 Why bot commits are excluded

The daily README rebuild commits to `main` with `[skip ci]`. The snake workflow
also writes to the `output` branch. If those commits were counted, the streak
and heatmap would always look active even when you did not solve anything.

The generator now:

- reads history from `HEAD` only, so the `output` branch is ignored
- skips commits authored by `github-actions[bot]`
- skips the bot email `41898282+github-actions[bot]@users.noreply.github.com`

The result is a streak and heatmap that reflect your work.

---

## 6. Changing the README

### 6.1 The golden rule

**Edit `.github/readme/scripts/readme_template.md`, not `README.md`.**

`README.md` is overwritten on every push. Changes made directly to it will be
lost the next time the workflow runs.

### 6.2 Change text, headings, quotes, or links

Edit `.github/readme/scripts/readme_template.md` directly. The template is the
source of truth for every static word in the README.

Then either run the generator and commit:

```bash
python3 .github/readme/scripts/update_readme.py
git add README.md .github/readme/assets/ .github/readme/scripts/readme_template.md
git commit -m "docs: update README copy"
git push
```

or push the template change and let the Action regenerate it.

### 6.3 Add a new static section

Add normal Markdown to `.github/readme/scripts/readme_template.md`:

```markdown
## 🎧 What I'm Listening To

Lo-fi beats and compiler errors.
```

No Python changes are needed for static content.

### 6.4 Add a dynamic section

Use a placeholder in the template:

```markdown
## Progress

{{STATS_TABLE}}
```

Then add the value to the `replacements` dictionary in `build_readme()`:

```python
"{{STATS_TABLE}}": build_stats_table(stats),
```

The script exits with an error if a placeholder is left unresolved, so a broken
README is never committed.

### 6.5 Available placeholders

| Placeholder | Value |
| :--- | :--- |
| `{{USERNAME}}` | GitHub username from `config.json` |
| `{{REPO}}` | Repository name |
| `{{REPO_URL}}` | Full repository URL |
| `{{LAST_UPDATED}}` | Generator timestamp |
| `{{STATS_TABLE}}` | Total, difficulty split, current and best streak |
| `{{STRIVER_TABLE}}` | Striver A2Z step tracker |
| `{{MILESTONES}}` | Auto-checked problem, streak, and skill milestones |
| `{{RECENT_TABLE}}` | Five most recent solutions |
| `{{WEEKLY_LOG}}` | Last eight weeks of topics, solutions, and commits |
| `{{REPO_TREE}}` | Real top-level folders and solution counts |
| `{{CONTEST_SECTION}}` | Optional contest log from `contests.json` |
| `{{TOTAL_SOLUTIONS}}` | Total tracked code files |
| `{{TARGET_PROBLEMS}}` | Overall target |
| `{{PROGRESS_PCT}}` | Overall percentage |

### 6.6 Change the hero banner

The header is a local SVG, not an external service. Edit `render_hero()` in
`.github/readme/scripts/update_readme.py`. See section 7.3 for the layout table.

The hero is generated on every run, so change the function rather than the SVG.

### 6.7 Change the GIF

The README uses one local GIF:

```html
<img src=".github/readme/assets/grind.gif" alt="I'm ready to slay" width="620" />
```

To swap it:

1. Put the new file in `.github/readme/assets/`.
2. Update the `src` in `.github/readme/scripts/readme_template.md`.
3. Update the `alt` text.
4. Keep the file under about 5 MB and around 500 to 700 pixels wide.
5. Change the `width` if the new image is a different shape.

The other GIFs are archived outside the repo at
`~/Practice/Dsa-cpp-archive/alternates/`. They are not tracked and do not affect
rendering speed or repository size.

### 6.8 Change the Striver A2Z tracker

The tracker reads `striver_steps` from `.github/readme/scripts/config.json`:

```json
{
  "name": "Arrays",
  "topics": ["Arrays", "Two Pointers", "Sliding Window"]
}
```

The `topics` names must match the `topics` list in the same file. Each step
shows:

- **Solved**: total solutions in the mapped topics
- **Coverage**: how many mapped topics have at least one solution
- **Status**: ⬜ none, 🟨 some, 🟩 all mapped topics started

Add, remove, or reorder steps by editing the array. The table updates on the
next run.

> Coverage is about topics started, not every problem in the sheet. If you want
> strict sheet completion, add a `target` per step and compare `solved` to it.

### 6.9 Change milestones

Problem milestones live in `PROBLEM_MILESTONES`:

```python
PROBLEM_MILESTONES = [
    (10, ""),
    (50, ""),
    (100, ""),
    (250, ""),
    (455, "A2Z sheet complete"),
    (600, ""),
    (800, ""),
]
```

Streak milestones live in `STREAK_MILESTONES`:

```python
STREAK_MILESTONES = [7, 30, 50, 100, 200, 365]
```

Skill milestones are in `build_milestones()`. They use topic counts and
difficulty counts, so they stay automatic. Contest skill milestones use the
number of entries in `contests.json`.

### 6.10 Change the weekly log, heatmap, and snake

- Weekly log: `build_weekly_log(stats)` uses git history and the last eight
  weeks. The current week is partial.
- Heatmap: `render_activity(stats)` draws the last 365 days.
- Snake: generated by `.github/workflows/snake.yml` on the `output` branch.
  The template embeds the dark and light SVGs with a `<picture>` element.

The snake is the only remote image in the README. It comes from the same
repository, so it does not depend on a third-party image host. If it is missing,
run **Actions → Generate Snake → Run workflow** once.

### 6.11 Add or change the contest log

The contest section is optional. It stays hidden until you create:

```text
.github/readme/scripts/contests.json
```

Start from `contests.example.json`:

```bash
cp .github/readme/scripts/contests.example.json .github/readme/scripts/contests.json
```

Schema:

```json
{
  "profiles": {
    "LeetCode": {
      "handle": "your_handle",
      "rating": "1850",
      "url": "https://leetcode.com/u/your_handle"
    }
  },
  "contests": [
    {
      "date": "2026-11-15",
      "platform": "LeetCode",
      "contest": "Weekly Contest 400",
      "solved": 3,
      "rank": 1200,
      "rating": "+25",
      "takeaway": "Need faster implementation on the third problem."
    }
  ]
}
```

If both `profiles` and `contests` are empty, the whole section is omitted. If
the file is invalid JSON, the section is also omitted, so the README cannot
break because of it.

### 6.12 Remove or reorder sections

Delete a section from `.github/readme/scripts/readme_template.md`. If it uses a
placeholder, remove the placeholder too, or keep the entry in `replacements`.
Order is controlled only by the template.

### 6.13 Unbreakable images policy

The README is designed to survive broken links:

- The hero, dashboard, heatmap, divider, and GIF are local files.
- The snake comes from this repository's own `output` branch.
- External services such as capsule-render, typing-svg, shields.io, and
  github-readme-stats are not used.
- Tables and milestone lists are plain Markdown, so they render even if every
  image fails.
- The contest section is hidden when its data file is missing or invalid.

If you add a new external image, expect it to break eventually. Download it or
generate it locally when the image matters.

---

## 7. Changing the visual assets

These are generated by `.github/readme/scripts/update_readme.py`. The
`.github/readme/assets/` folder holds four files:

| Asset | Function | Purpose |
| :--- | :--- | :--- |
| `hero.svg` | `render_hero(stats)` | Header banner with Matrix-style code rain |
| `dashboard.svg` | `render_dashboard(stats)` | Progress cards and topic coverage |
| `activity.svg` | `render_activity(stats)` | 365-day commit heatmap |
| `divider.svg` | `render_divider()` | Pac-Man divider before the closing section |

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

### 7.3 Hero banner

Function: `render_hero(stats)`

- Canvas: `1200 × 340`
- Matrix-style code rain behind the text
- Title, subtitle, and a mono command line
- A glowing binary tree on the right
- Colors: cyan `#22d3ee`, teal `#2dd4bf`, violet `#a78bfa`, green `#4ade80`

Common edits:

| Change | Where |
| :--- | :--- |
| Title | `svg_text(64, 140, "DSA in C++", 62, ...)` |
| Subtitle | The `Notes and solutions from my DSA practice.` line |
| Command line | The `$ g++ -std=c++17 solution.cpp -o solution` line |
| Rain density | `for column in range(18, width, 30)` |
| Rain colors | `color = "#4ade80" if ... else "#22d3ee"` |
| Tree nodes | The `nodes = [...]` list |
| Title gradient | `<linearGradient id="heroTitle">` |

### 7.4 Pac-Man divider

Function: `render_divider()`

- Canvas: `1200 × 96`
- Transparent background, so it works in light and dark mode
- Pac-Man, four ghosts, and a pellet trail
- A nod to BFS and graph traversal

Common edits:

| Change | Where |
| :--- | :--- |
| Ghost colors | `ghosts = [(620, "#ef4444"), ...]` |
| Ghost positions | First value in each `ghosts` tuple |
| Divider text | `"chasing better solutions"` |
| Line style | `stroke-width`, `stroke-dasharray` |

### 7.5 Change where assets are written

In `main()`:

```python
(ASSETS_DIR / "hero.svg").write_text(...)
(ASSETS_DIR / "dashboard.svg").write_text(...)
(ASSETS_DIR / "activity.svg").write_text(...)
(ASSETS_DIR / "divider.svg").write_text(...)
```

If you rename them, update the template image paths and the workflow's
`git add README.md .github/readme/assets/`.

### 7.6 Add a completely new generated asset

1. Write a `render_*.svg` function.
2. Call it in `main()` and write the file under `.github/readme/assets/`.
3. Embed it in `.github/readme/scripts/readme_template.md`.
4. Ensure the workflow commits it (`git add README.md .github/readme/assets/` already covers `.github/readme/assets/`).
5. Run locally to verify.

### 7.7 Pop culture in this README

The default design uses three pop culture pieces:

| Piece | Where | Format |
| :--- | :--- | :--- |
| Matrix code rain | Hero banner | Local SVG |
| Pac-Man and ghosts | Divider before Connect | Local SVG |
| "I'm ready to slay" knight | Under the hero | Local GIF |

The chosen GIF is `.github/readme/assets/grind.gif`. It is a short, readable loop
with the message built into the frame, so it works even without the caption.
The other GIFs and the Claude draft are archived outside the repo at
`~/Practice/Dsa-cpp-archive/`.

Other themes that fit a DSA and C++ repository:

| Theme | Best placement | Why it fits |
| :--- | :--- | :--- |
| **The Matrix** | Hero background | Green code rain and the "there is no spoon" energy |
| **Pac-Man** | Divider or Graphs section | BFS and graph traversal, chasing the next pellet |
| **Tetris** | Stack and Queue section | Falling blocks are stacks, clears are queues |
| **Chess** | Dynamic Programming section | Minimax, evaluation, and planning ahead |
| **Pokemon** | Progress section | "Gotta solve 'em all" works for problem counts |
| **One Piece** | Roadmap | The Grand Line is a natural phase map |
| **Inception** | Recursion section | A dream inside a dream is recursion |
| **Interstellar** | Complexity section | Time dilation is a fun way to explain Big O |
| **Dragon Ball** | Difficulty section | Power levels as time complexity |
| **Minecraft** | Data structures section | Crafting recipes as building blocks |
| **Star Wars** | Footer | "May the force be with you" |
| **Among Us** | Bug fixing section | Finding the impostor in the code |

### 7.8 Adding images safely

The README intentionally uses almost no external images. If you add one, follow
these rules:

- Prefer SVG or PNG over GIF when you can. They load faster and look sharper.
- Hotlinked GIFs can disappear. If the image matters, download it, place it in
  `.github/readme/assets/`, and reference the local path.
- Fan art and screenshots may be copyrighted. Use official press kits, creative
  commons assets, or draw your own SVG.
- Add a short `alt` text so the README still reads well if the image fails.
- Keep the hero under about `1200 × 400` so it does not dominate the page.
- Keep a README GIF under about 5 MB. The current `grind.gif` is about 3 MB.

---

## 8. Adding and organizing solutions

### 8.1 Create a solution file

```bash
mkdir -p DSA/Arrays
cp .github/readme/templates/solution.cpp DSA/Arrays/0001-two-sum.cpp
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

- put them under `.github/readme/` or another excluded folder such as `docs/`, or
- use a non-code extension such as `.md`, or
- add the folder to `exclude_dirs` in `.github/readme/scripts/config.json`.

### 8.6 Adding another language

Add the extension to `code_extensions`:

```json
"code_extensions": [".cpp", ".py", ".java", ".go", ".rs"]
```

The dashboard counts it as a solution. The language badge is not displayed by
default; add one in the template if desired.

### 8.7 Excluding folders

In `.github/readme/scripts/config.json`:

```json
"exclude_dirs": [".git", ".github", ".vscode", ".idea", "scripts", "templates", "assets", "docs", "build", "bin", "node_modules"]
```

This matches **any path segment** with that exact name. It is not a glob.

> There is no per-file exclusion yet. To skip files starting with `_`, add a
> condition in `iter_code_files()`.

---

## 9. Adding or changing topics

### 9.1 Add a new topic

In `.github/readme/scripts/config.json`, add an object to `topics`:

```json
{
  "name": "Union Find",
  "icon": "🔗",
  "match": ["unionfind", "disjointset", "dsu"]
}
```

Then add it to a Striver step if it belongs to the A2Z tracker:

```json
{
  "name": "Graphs",
  "topics": ["Graphs", "Union Find"]
}
```

Run:

```bash
python3 .github/readme/scripts/update_readme.py
```

The dashboard and the Striver A2Z tracker pick it up automatically.

### 9.2 Rename a topic

1. Change `name` in `config.json`.
2. Update the same name wherever it appears in `striver_steps`.
3. Keep the old keyword in `match` if you want existing folders to keep working,
   or rename the folder too.

### 9.3 Remove a topic

1. Remove it from `topics`.
2. Remove it from `striver_steps`.
3. Existing files fall back to `Misc` unless their folder/metadata matches
   another topic.

### 9.4 Change per-topic goal

```json
"topic_target": 25
```

This controls the per-topic bars in the dashboard. It does not cap the count.

### 9.5 Change overall target

```json
"target_problems": 455
```

This controls the overall progress bar in the dashboard and the A2Z completion
milestone.

### 9.6 Change timezone

```json
"timezone": "Asia/Kolkata"
```

This affects “today” for streaks and the timestamps in the generated SVGs.
Use any IANA timezone name.

### 9.7 Change the Striver A2Z tracker

Edit the `striver_steps` array. Topic names must match `topics[].name` exactly.
The tracker shows solved counts and topic coverage for each step, and
auto-checks a step when all mapped topics have at least one solution.

---

## 10. Running the generator locally

```bash
python3 .github/readme/scripts/update_readme.py
```

It prints something like:

```text
Rebuilt README.md, .github/readme/assets/hero.svg, .github/readme/assets/dashboard.svg,
.github/readme/assets/activity.svg and .github/readme/assets/divider.svg
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
magick .github/readme/assets/dashboard.svg /tmp/dashboard.png
magick .github/readme/assets/activity.svg /tmp/activity.png
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
`.github/readme/assets/**`, and `output/**` ignored to prevent loops.

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
`.github/readme/scripts/readme_template.md`, then run:

```bash
python3 .github/readme/scripts/update_readme.py
git add README.md .github/readme/assets/ .github/readme/scripts/readme_template.md
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

### 12.8 A remote image does not load

The default README only uses one remote image: the contribution snake from this
repository's own `output` branch. If it breaks, see 12.7.

If you added a third-party image such as a stats card or trophy, expect it to be
rate-limited or temporarily down. Replace it with a local asset under
`.github/readme/assets/`, or remove it from the template. A fully self-hosted
README is the reliable option.

### 12.9 Stats are zero even though files exist

Check:

- File extension is in `code_extensions`.
- Folder is not in `exclude_dirs`.
- The file is inside the repo, not a submodule.
- Run locally and read the printed count:

```bash
python3 .github/readme/scripts/update_readme.py
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

Streaks are based on commit dates from `HEAD` in the configured timezone.
Commits authored by `github-actions[bot]` are filtered out before streaks,
active days, the heatmap, and the weekly log are computed.

The current streak allows today or yesterday as the starting point, so it does
not break before you commit for the day. The longest streak is computed only
from your own commit days.

> Bot commits can still appear in GitHub's own contribution graph because that
> graph is controlled by GitHub, not by this script. The README dashboard and
> heatmap deliberately exclude them.

### 12.13 The bot commit conflicts with my local changes

Pull with rebase before pushing:

```bash
git pull --rebase
git push
```

If there is a conflict in `README.md` or `.github/readme/assets/`, discard your local generated
files and regenerate:

```bash
git checkout --theirs README.md .github/readme/assets/
# or
git restore --source=origin/main README.md .github/readme/assets/
python3 .github/readme/scripts/update_readme.py
```

For template conflicts, resolve `.github/readme/scripts/readme_template.md` manually.

### 12.14 The generator fails with unresolved placeholders

You used a `{{PLACEHOLDER}}` in the template without adding it to
`build_readme()` in `.github/readme/scripts/update_readme.py`.

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
git checkout <COMMIT> -- README.md .github/readme/assets/
git commit -m "docs: restore previous README"
git push
```

### 13.4 Start over

```bash
git checkout <COMMIT> -- .github/readme/scripts/ .github/readme/assets/ README.md
python3 .github/readme/scripts/update_readme.py
git add README.md .github/readme/assets/ .github/readme/scripts/
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
- External README images are limited to the contribution snake, which comes from
  this repository's own `output` branch. The rest of the visuals are local. Keep
  it that way if you care about reliability and privacy.

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
python3 .github/readme/scripts/update_readme.py

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
| Change README text/design | `.github/readme/scripts/readme_template.md` |
| Change targets/topics/steps/timezone | `.github/readme/scripts/config.json` |
| Change banner/dashboard/heatmap/divider visuals | `.github/readme/scripts/update_readme.py` |
| Swap the README GIF | `.github/readme/assets/grind.gif` and the template |
| Add contest data | `.github/readme/scripts/contests.json` |
| Add a solution | `DSA/<Topic>/...` |
| Change automation schedule | `.github/workflows/update-readme.yml` |
| Change snake settings | `.github/workflows/snake.yml` |
| Document a new workflow | `.github/readme/MANUAL.md` (this file) |

### Files you should not edit

| File | Why |
| :--- | :--- |
| `README.md` | Regenerated on every push |
| `.github/readme/assets/hero.svg` | Regenerated by the script |
| `.github/readme/assets/dashboard.svg` | Regenerated by the script |
| `.github/readme/assets/activity.svg` | Regenerated by the script |
| `.github/readme/assets/divider.svg` | Regenerated by the script |

---

<div align="center">

**Keep the streak alive. 🚀**

</div>
