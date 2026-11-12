#!/usr/bin/env python3
"""
Rebuild README.md, assets/dashboard.svg and assets/activity.svg from the repo.

The script is intentionally dependency-free (Python standard library only) so
GitHub Actions can run it without installing anything.

Run locally:
    python3 scripts/update_readme.py
"""

from __future__ import annotations

import html
import json
import math
import re
import subprocess
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "scripts" / "config.json"
TEMPLATE_PATH = ROOT / "scripts" / "readme_template.md"
README_PATH = ROOT / "README.md"
ASSETS_DIR = ROOT / "assets"

SANS = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SFMono-Regular', Consolas, monospace"

DIFFICULTY_COLORS = {
    "Easy": "00B8A3",
    "Medium": "FFB020",
    "Hard": "EF4444",
    "Unknown": "64748B",
}


# --------------------------------------------------------------------------- #
# Small utilities
# --------------------------------------------------------------------------- #
def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


CONFIG = load_json(CONFIG_PATH)


def resolve_timezone(name: str):
    try:
        return ZoneInfo(name)
    except Exception:
        return timezone.utc


TZ = resolve_timezone(CONFIG.get("timezone", "UTC"))


def git(*args: str) -> str:
    """Run a git command, returning stdout (empty string on failure)."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        return result.stdout if result.returncode == 0 else ""
    except Exception:
        return ""


def norm_token(value: str) -> str:
    """Normalise a topic/path token for matching: 'Two Pointers' -> 'twopointers'."""
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def shields_escape(value: object) -> str:
    """Escape a value for the path portion of a shields.io badge."""
    text = str(value)
    text = text.replace("%", "%25")
    text = text.replace("-", "--")
    text = text.replace("_", "__")
    text = text.replace(" ", "%20")
    text = text.replace("/", "%2F")
    text = text.replace("&", "%26")
    text = text.replace("#", "%23")
    text = text.replace("?", "%3F")
    return text


def svg_text(
    x: float,
    y: float,
    text: object,
    size: float = 14,
    fill: str = "#e2e8f0",
    weight: int = 400,
    anchor: str = "start",
    family: str = SANS,
    opacity: float = 1,
    letter_spacing: float | None = None,
) -> str:
    attrs = (
        f'x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
    )
    if opacity != 1:
        attrs += f' opacity="{opacity}"'
    if letter_spacing is not None:
        attrs += f' letter-spacing="{letter_spacing}"'
    return f"<text {attrs}>{html.escape(str(text))}</text>"


# --------------------------------------------------------------------------- #
# Repo scanning
# --------------------------------------------------------------------------- #
def iter_code_files() -> list[Path]:
    excluded = {d.strip("/") for d in CONFIG.get("exclude_dirs", [])}
    extensions = {e.lower() for e in CONFIG.get("code_extensions", [])}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(ROOT).parts
        if any(part in excluded for part in rel_parts[:-1]):
            continue
        if path.suffix.lower() not in extensions:
            continue
        files.append(path)
    return sorted(files)


def clean_comment_line(line: str) -> str:
    line = line.strip()
    line = re.sub(r"^(?://+|#+|/\*+|\*+|<!--)\s*", "", line)
    line = re.sub(r"\*/\s*$", "", line)
    return line.strip()


META_PATTERNS = {
    "problem": re.compile(r"^@?(?:problem(?:\s*name)?|title|question)\s*[:\-]\s*(.+)$", re.I),
    "topic": re.compile(r"^@?(?:topic|category|tags?)\s*[:\-]\s*(.+)$", re.I),
    "difficulty": re.compile(r"^@?(?:difficulty|level)\s*[:\-]\s*(.+)$", re.I),
    "link": re.compile(r"^@?(?:link|url|problem\s*link)\s*[:\-]\s*(https?://\S+)", re.I),
    "time": re.compile(r"^@?(?:time(?:\s*complexity)?)\s*[:\-]\s*(.+)$", re.I),
    "space": re.compile(r"^@?(?:space(?:\s*complexity)?)\s*[:\-]\s*(.+)$", re.I),
}
NUMBERED_TITLE = re.compile(r"^(?:\d+[\.\)\-:]\s*)(.+)$")


def parse_metadata(path: Path) -> dict[str, str]:
    meta: dict[str, str] = {}
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for _ in range(80):
                raw = fh.readline()
                if not raw:
                    break
                line = clean_comment_line(raw)
                if not line:
                    continue
                for key, pattern in META_PATTERNS.items():
                    match = pattern.match(line)
                    if match and key not in meta:
                        meta[key] = match.group(1).strip().rstrip("*/").strip()
                if "problem" not in meta:
                    numbered = NUMBERED_TITLE.match(line)
                    if numbered and not line.lower().startswith(("time", "space", "link", "topic", "difficulty")):
                        meta["problem"] = numbered.group(1).strip()
    except OSError:
        pass
    return meta


def clean_title(raw: str) -> str:
    title = re.sub(r"^(?:\d+[\.\)\-:]\s*)", "", raw.strip())
    title = re.sub(r"\s+", " ", title).strip(" */")
    return title[:120]


def title_from_filename(path: Path) -> str:
    stem = re.sub(r"^\d+[-_.\s]+", "", path.stem)
    stem = re.sub(r"[-_]+", " ", stem).strip()
    if not stem:
        return "Untitled"
    return stem.title()[:120]


def normalize_difficulty(raw: str | None) -> str:
    if not raw:
        return "Unknown"
    lowered = raw.lower()
    for difficulty in ("easy", "medium", "hard"):
        if difficulty in lowered:
            return difficulty.capitalize()
    return "Unknown"


def build_topic_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for topic in CONFIG["topics"]:
        for value in [topic["name"], *topic.get("match", [])]:
            token = norm_token(value)
            if token:
                lookup.setdefault(token, topic["name"])
    return lookup


TOPIC_LOOKUP = build_topic_lookup()
TOPIC_ICONS = {topic["name"]: topic.get("icon", "•") for topic in CONFIG["topics"]}


def classify_topic(rel_path: str, meta_topic: str | None) -> str:
    """Classify a solution by metadata topic, exact folder name, then keywords."""
    if meta_topic:
        for part in re.split(r"[,/|;]+", meta_topic):
            token = norm_token(part)
            if token in TOPIC_LOOKUP:
                return TOPIC_LOOKUP[token]

    pure = PurePosixPath(rel_path)
    directories = list(pure.parts[:-1])
    for part in reversed(directories):
        token = norm_token(part)
        if token in TOPIC_LOOKUP:
            return TOPIC_LOOKUP[token]

    haystack = norm_token(" ".join([*directories, pure.stem, meta_topic or ""]))
    best_name = "Misc"
    best_length = 0
    for topic in CONFIG["topics"]:
        for value in [topic["name"], *topic.get("match", [])]:
            token = norm_token(value)
            if token and token in haystack and len(token) > best_length:
                best_name = topic["name"]
                best_length = len(token)
    return best_name


# --------------------------------------------------------------------------- #
# Git history
# --------------------------------------------------------------------------- #
def collect_git_data() -> tuple[set[date], int, dict[str, datetime]]:
    commit_days: set[date] = set()
    commit_count = 0

    raw_dates = git("log", "--all", "--format=%aI")
    for line in raw_dates.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            moment = datetime.fromisoformat(line)
        except ValueError:
            continue
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        commit_days.add(moment.astimezone(TZ).date())
        commit_count += 1

    added: dict[str, datetime] = {}
    raw_added = git("log", "--all", "--diff-filter=A", "--name-only", "--format=COMMIT|%aI")
    current: datetime | None = None
    for line in raw_added.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("COMMIT|"):
            try:
                current = datetime.fromisoformat(line.split("|", 1)[1])
            except (ValueError, IndexError):
                current = None
        elif current is not None:
            # Newest commit is read first, so setdefault keeps the latest add.
            added.setdefault(line, current)

    if not commit_days:
        for moment in added.values():
            commit_days.add(moment.astimezone(TZ).date())

    return commit_days, commit_count, added


def calculate_streaks(active_days: set[date], today: date) -> tuple[int, int]:
    if not active_days:
        return 0, 0

    current = 0
    cursor = today if today in active_days else today - timedelta(days=1)
    while cursor in active_days:
        current += 1
        cursor -= timedelta(days=1)

    longest = 1
    run = 1
    ordered = sorted(active_days)
    for previous, current_day in zip(ordered, ordered[1:]):
        if current_day - previous == timedelta(days=1):
            run += 1
            longest = max(longest, run)
        else:
            run = 1
    return current, longest


# --------------------------------------------------------------------------- #
# Aggregate stats
# --------------------------------------------------------------------------- #
def collect_solutions() -> list[dict]:
    commit_days, commit_count, added_map = collect_git_data()
    solutions: list[dict] = []

    for path in iter_code_files():
        rel = path.relative_to(ROOT).as_posix()
        meta = parse_metadata(path)
        raw_title = meta.get("problem") or title_from_filename(path)
        title = clean_title(raw_title)
        if not title:
            title = title_from_filename(path)

        topic = classify_topic(rel, meta.get("topic"))
        difficulty = normalize_difficulty(meta.get("difficulty"))
        added_at = added_map.get(rel)
        if added_at is None:
            added_at = datetime.fromtimestamp(path.stat().st_mtime, tz=TZ)
        else:
            added_at = added_at.astimezone(TZ)

        solutions.append(
            {
                "path": rel,
                "title": title,
                "topic": topic,
                "difficulty": difficulty,
                "added_at": added_at,
                "link": meta.get("link", ""),
                "time": meta.get("time", ""),
                "space": meta.get("space", ""),
                "language": path.suffix.lower().lstrip("."),
            }
        )

    solutions.sort(key=lambda item: (item["added_at"], item["path"]), reverse=True)

    today = datetime.now(TZ).date()
    current_streak, longest_streak = calculate_streaks(commit_days, today)
    topic_counts = Counter(item["topic"] for item in solutions)
    covered = sum(1 for topic in CONFIG["topics"] if topic_counts.get(topic["name"], 0) > 0)
    difficulty_counts = Counter(item["difficulty"] for item in solutions)
    cpp_extensions = {".cpp", ".cc", ".cxx", ".c", ".h", ".hpp"}
    cpp_files = sum(1 for item in solutions if f".{item['language']}" in cpp_extensions)

    return {
        "solutions": solutions,
        "total": len(solutions),
        "cpp_files": cpp_files,
        "topics": topic_counts,
        "covered": covered,
        "total_topics": len(CONFIG["topics"]),
        "easy": difficulty_counts.get("Easy", 0),
        "medium": difficulty_counts.get("Medium", 0),
        "hard": difficulty_counts.get("Hard", 0),
        "unknown": difficulty_counts.get("Unknown", 0),
        "commit_days": commit_days,
        "commit_count": commit_count,
        "active_days": len(commit_days),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "today": today,
        "last_updated": datetime.now(TZ),
    }


# --------------------------------------------------------------------------- #
# Markdown fragments
# --------------------------------------------------------------------------- #
def build_stat_badges(stats: dict) -> str:
    username = CONFIG["username"]
    repo = CONFIG["repo"]
    total = stats["total"]
    streak = stats["current_streak"]
    covered = stats["covered"]
    total_topics = stats["total_topics"]
    active_days = stats["active_days"]

    streak_label = f"{streak} day" + ("" if streak == 1 else "s")
    badges = [
        (
            f"https://img.shields.io/badge/Solutions-{shields_escape(total)}-22D3EE"
            "?style=for-the-badge&logo=leetcode&logoColor=white",
            "Solutions",
        ),
        (
            f"https://img.shields.io/badge/Streak-{shields_escape(streak_label)}-FB923C"
            "?style=for-the-badge&logo=git&logoColor=white",
            "Current streak",
        ),
        (
            f"https://img.shields.io/badge/Topics-{shields_escape(str(covered) + '/' + str(total_topics))}-A78BFA"
            "?style=for-the-badge&logo=bookstack&logoColor=white",
            "Topics covered",
        ),
        (
            f"https://img.shields.io/badge/Active%20Days-{shields_escape(active_days)}-4ADE80"
            "?style=for-the-badge&logo=googlecalendar&logoColor=white",
            "Active days",
        ),
        (
            f"https://img.shields.io/github/last-commit/{username}/{repo}"
            "?label=Last%20Commit&style=for-the-badge&color=64748B&logo=git&logoColor=white",
            "Last commit",
        ),
    ]
    return "\n".join(f'  <img src="{src}" alt="{alt}" />' for src, alt in badges)


def build_topic_table(stats: dict) -> str:
    goal = int(CONFIG.get("topic_target", 25))
    rows: list[str] = []
    for topic in CONFIG["topics"]:
        name = topic["name"]
        icon = topic.get("icon", "•")
        count = stats["topics"].get(name, 0)
        percentage = 0 if count == 0 else min(100, round(count / goal * 100))
        filled = round(percentage / 100 * 16)
        if count > 0:
            filled = max(1, filled)
        bar = "█" * filled + "░" * (16 - filled)
        rows.append(f"| {icon} **{name}** | `{count:>3} / {goal}` | `{bar}` **{percentage}%** |")
    return "\n".join(rows)


def build_recent_table(stats: dict) -> str:
    solutions = stats["solutions"]
    if not solutions:
        return (
            "> 🚀 **No solutions tracked yet.** Add your first file under `DSA/Arrays/` "
            "and this table will populate itself on the next push."
        )

    rows = [
        "| Problem | Topic | Difficulty | Added | Code |",
        "| :--- | :--- | :---: | :---: | :---: |",
    ]
    for item in solutions[:8]:
        title = item["title"].replace("|", "\\|")
        if item["link"]:
            problem_cell = f"[**{title}**]({item['link']})"
        else:
            problem_cell = f"**{title}**"
        icon = TOPIC_ICONS.get(item["topic"], "•")
        difficulty = item["difficulty"]
        color = DIFFICULTY_COLORS.get(difficulty, DIFFICULTY_COLORS["Unknown"])
        difficulty_badge = (
            f"![{difficulty}](https://img.shields.io/badge/"
            f"{shields_escape(difficulty)}-{color}?style=flat-square)"
        )
        code_link = quote(item["path"], safe="/")
        rows.append(
            f"| {problem_cell} | {icon} {item['topic']} | {difficulty_badge} | "
            f"{item['added_at'].strftime('%d %b %Y')} | [View]({code_link}) |"
        )

    table = "\n".join(rows)
    if len(solutions) > 8:
        table += f"\n\n<sub>Showing the 8 most recent of **{len(solutions)}** tracked files.</sub>"
    return table


def build_roadmap(stats: dict) -> str:
    lines: list[str] = []
    for phase in CONFIG.get("phases", []):
        names = phase["topics"]
        started = sum(1 for name in names if stats["topics"].get(name, 0) > 0)
        lines.append(f"### {phase['name']}")
        lines.append(f"`{started} / {len(names)} topics started`")
        lines.append("")
        for name in names:
            count = stats["topics"].get(name, 0)
            icon = TOPIC_ICONS.get(name, "•")
            if count:
                plural = "s" if count != 1 else ""
                lines.append(f"- [x] {icon} **{name}** — {count} solution{plural}")
            else:
                lines.append(f"- [ ] {icon} **{name}**")
        lines.append("")
    return "\n".join(lines).strip()


def build_leetcode_section() -> str:
    if not CONFIG.get("show_leetcode_card"):
        return ""
    username = CONFIG.get("leetcode_username", "").strip()
    if not username:
        return ""
    return (
        "## 🧪 LeetCode Profile\n\n"
        '<div align="center">\n'
        f'  <img src="https://leetcard.jacoblin.cool/{quote(username)}'
        '?theme=dark&font=JetBrains%20Mono&ext=heatmap" alt="LeetCode stats" />\n'
        "</div>"
    )


def build_current_focus(stats: dict) -> str:
    if stats["solutions"]:
        return f"**{stats['solutions'][0]['topic']}**"
    return "the fundamentals — first solution loading…"


def build_next_milestone(stats: dict) -> str:
    target = int(CONFIG.get("target_problems", 500))
    total = stats["total"]
    if total >= target:
        return f"**{target} reached** 🎉"
    step = 50
    next_milestone = min(target, ((total // step) + 1) * step)
    return f"**{next_milestone} solutions**"


# --------------------------------------------------------------------------- #
# SVG: dashboard
# --------------------------------------------------------------------------- #
def render_dashboard(stats: dict) -> str:
    width, height = 1200, 780
    username = CONFIG["username"]
    repo = CONFIG["repo"]
    target = int(CONFIG.get("target_problems", 500))
    total = stats["total"]
    percentage = 0 if target <= 0 else min(100, round(total / target * 100))

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Live DSA progress dashboard for {html.escape(username)}">',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#080f1c" />',
        '<stop offset="55%" stop-color="#0b1526" />',
        '<stop offset="100%" stop-color="#0a1a22" />',
        "</linearGradient>",
        '<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">',
        '<stop offset="0%" stop-color="#22d3ee" />',
        '<stop offset="55%" stop-color="#2dd4bf" />',
        '<stop offset="100%" stop-color="#a78bfa" />',
        "</linearGradient>",
        '<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">',
        '<stop offset="0%" stop-color="#06b6d4" />',
        '<stop offset="50%" stop-color="#14b8a6" />',
        '<stop offset="100%" stop-color="#8b5cf6" />',
        "</linearGradient>",
        '<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">',
        '<path d="M 32 0 L 0 0 0 32" fill="none" stroke="#38bdf8" stroke-width="0.5" />',
        "</pattern>",
        '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%">',
        '<feGaussianBlur stdDeviation="70" />',
        "</filter>",
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="26" fill="url(#bg)" />',
        f'<rect width="{width}" height="{height}" rx="26" fill="url(#grid)" opacity="0.035" />',
        '<rect x="0" y="0" width="1200" height="4" fill="url(#accent)" />',
        '<circle cx="1080" cy="90" r="190" fill="#06b6d4" opacity="0.10" filter="url(#blur)" />',
        '<circle cx="120" cy="700" r="180" fill="#8b5cf6" opacity="0.08" filter="url(#blur)" />',
        '<rect x="60" y="42" width="168" height="28" rx="14" fill="#0b2838" stroke="#155e75" />',
        '<circle cx="78" cy="56" r="4.5" fill="#22d3ee" />',
        svg_text(92, 60, "LIVE DSA DASHBOARD", 10.5, "#67e8f9", 700, letter_spacing=1.4),
        svg_text(60, 118, "The Grind, Visualized.", 36, "#f8fafc", 700),
        svg_text(
            60,
            144,
            f"Auto-generated from commits  ·  github.com/{username}/{repo}",
            12,
            "#94a3b8",
        ),
    ]

    cards = [
        ("SOLUTIONS", str(total), "code files tracked", "#22d3ee"),
        ("CURRENT STREAK", f"{stats['current_streak']}d", "keep the chain alive", "#fb923c"),
        ("TOPICS", f"{stats['covered']}/{stats['total_topics']}", "coverage unlocked", "#a78bfa"),
        ("ACTIVE DAYS", str(stats["active_days"]), "days with commits", "#4ade80"),
    ]
    card_y = 166
    for index, (label, value, subtitle, color) in enumerate(cards):
        x = 60 + index * 275
        parts.extend(
            [
                f'<rect x="{x}" y="{card_y}" width="255" height="104" rx="16" '
                'fill="#101c2e" stroke="#1e3a5f" stroke-width="1" />',
                f'<rect x="{x}" y="{card_y}" width="4" height="104" rx="2" fill="{color}" />',
                svg_text(x + 24, card_y + 30, label, 10.5, "#7dd3fc", 700, letter_spacing=1.2),
                svg_text(x + 24, card_y + 70, value, 32, "#f8fafc", 700, family=MONO),
                svg_text(x + 24, card_y + 90, subtitle, 10.5, "#94a3b8"),
            ]
        )

    parts.extend(
        [
            svg_text(60, 312, "OVERALL PROGRESS", 11.5, "#94a3b8", 700, letter_spacing=1.4),
            svg_text(
                1140,
                312,
                f"{total} / {target}  ·  {percentage}%",
                13,
                "#e2e8f0",
                700,
                anchor="end",
                family=MONO,
            ),
            '<rect x="60" y="328" width="1080" height="16" rx="8" fill="#1e293b" />',
        ]
    )
    if percentage > 0:
        fill_width = max(18.0, 1080 * percentage / 100)
        parts.append(
            f'<rect x="60" y="328" width="{fill_width:.1f}" height="16" rx="8" fill="url(#bar)" />'
        )
    parts.extend(
        [
            svg_text(60, 390, "TOPIC COVERAGE", 11.5, "#94a3b8", 700, letter_spacing=1.4),
            svg_text(
                1140,
                390,
                f"{stats['covered']} of {stats['total_topics']} topics started",
                11.5,
                "#64748b",
                anchor="end",
            ),
        ]
    )

    topics = CONFIG["topics"]
    per_column = math.ceil(len(topics) / 2)
    topic_goal = int(CONFIG.get("topic_target", 25))
    for index, topic in enumerate(topics):
        column = index // per_column
        row = index % per_column
        x = 60 + column * 555
        y = 420 + row * 27
        count = stats["topics"].get(topic["name"], 0)
        topic_percentage = 0 if count == 0 else min(100, count / topic_goal * 100)
        bar_width = 155
        filled_width = bar_width * topic_percentage / 100
        parts.extend(
            [
                svg_text(x, y, topic["name"], 12.5, "#cbd5e1" if count else "#64748b", 500),
                f'<rect x="{x + 190}" y="{y - 9}" width="{bar_width}" height="8" rx="4" fill="#1e293b" />',
            ]
        )
        if filled_width > 0:
            parts.append(
                f'<rect x="{x + 190}" y="{y - 9}" width="{max(6.0, filled_width):.1f}" '
                f'height="8" rx="4" fill="{["#22d3ee", "#2dd4bf", "#a78bfa", "#4ade80"][index % 4]}" />'
            )
        parts.append(
            svg_text(
                x + 390,
                y,
                str(count),
                11.5,
                "#94a3b8" if count else "#475569",
                700,
                anchor="end",
                family=MONO,
            )
        )

    parts.extend(
        [
            '<line x1="60" y1="720" x2="1140" y2="720" stroke="#1e293b" stroke-width="1" />',
            svg_text(
                60,
                748,
                f"Last updated {stats['last_updated'].strftime('%d %b %Y, %I:%M %p %Z')}",
                11,
                "#64748b",
            ),
            svg_text(
                1140,
                748,
                f"github.com/{username}/{repo}",
                11,
                "#64748b",
                anchor="end",
                family=MONO,
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# SVG: consistency heatmap
# --------------------------------------------------------------------------- #
def render_activity(stats: dict) -> str:
    width, height = 1200, 340
    today = stats["today"]
    username = CONFIG["username"]
    repo = CONFIG["repo"]

    counts: Counter[date] = Counter()
    for day in stats["commit_days"]:
        counts[day] += 1

    start = today - timedelta(days=364)
    # GitHub heatmaps start weeks on Sunday.
    start -= timedelta(days=(start.weekday() + 1) % 7)
    weeks = ((today - start).days // 7) + 1
    cell, gap = 13, 4
    step = cell + gap
    grid_x, grid_y = 120, 160
    level_colors = ["#172033", "#0e4429", "#006d32", "#26a641", "#39d353"]

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Commit consistency heatmap for the last 365 days">',
        "<defs>",
        '<linearGradient id="abg" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#080f1c" />',
        '<stop offset="100%" stop-color="#0a1a22" />',
        "</linearGradient>",
        '<filter id="aglow" x="-50%" y="-50%" width="200%" height="200%">',
        '<feGaussianBlur stdDeviation="60" />',
        "</filter>",
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="24" fill="url(#abg)" />',
        '<rect x="0" y="0" width="1200" height="4" fill="#22c55e" />',
        '<circle cx="1070" cy="70" r="150" fill="#22c55e" opacity="0.08" filter="url(#aglow)" />',
        '<rect x="60" y="36" width="180" height="26" rx="13" fill="#0b2a1a" stroke="#166534" />',
        '<circle cx="78" cy="49" r="4.5" fill="#4ade80" />',
        svg_text(92, 53, "CONSISTENCY MAP", 10, "#86efac", 700, letter_spacing=1.3),
        svg_text(60, 106, "Every square is a day you showed up.", 26, "#f8fafc", 700),
        svg_text(
            60,
            128,
            f"Last 365 days  ·  {stats['active_days']} active days  ·  "
            f"{stats['current_streak']}d current streak  ·  {stats['longest_streak']}d best",
            11.5,
            "#94a3b8",
        ),
    ]

    # Month labels.
    last_month = None
    for week in range(weeks):
        week_start = start + timedelta(days=week * 7)
        if week_start > today:
            break
        if week_start.day <= 7 and week_start.month != last_month:
            parts.append(
                svg_text(grid_x + week * step, grid_y - 14, week_start.strftime("%b"), 10.5, "#64748b")
            )
            last_month = week_start.month

    # Weekday labels (Monday, Wednesday, Friday).
    weekday_labels = {1: "Mon", 3: "Wed", 5: "Fri"}
    for day_index, label in weekday_labels.items():
        parts.append(
            svg_text(
                grid_x - 12,
                grid_y + day_index * step + 10,
                label,
                10,
                "#475569",
                anchor="end",
            )
        )

    # Cells.
    for week in range(weeks):
        for day_index in range(7):
            current = start + timedelta(days=week * 7 + day_index)
            if current > today:
                continue
            count = counts.get(current, 0)
            level = 0 if count == 0 else 1 if count == 1 else 2 if count == 2 else 3 if count == 3 else 4
            parts.append(
                f'<rect x="{grid_x + week * step}" y="{grid_y + day_index * step}" '
                f'width="{cell}" height="{cell}" rx="3" fill="{level_colors[level]}">'
                f"<title>{current.isoformat()}: {count} commit{'s' if count != 1 else ''}</title></rect>"
            )

    # Legend.
    legend_x = 880
    legend_y = 302
    parts.append(svg_text(legend_x, legend_y, "Less", 10.5, "#64748b"))
    for level, color in enumerate(level_colors):
        parts.append(
            f'<rect x="{legend_x + 38 + level * (cell + 4)}" y="{legend_y - 11}" '
            f'width="{cell}" height="{cell}" rx="3" fill="{color}" />'
        )
    parts.append(svg_text(legend_x + 38 + 5 * (cell + 4) + 4, legend_y, "More", 10.5, "#64748b"))

    parts.extend(
        [
            '<line x1="60" y1="316" x2="1140" y2="316" stroke="#1e293b" stroke-width="1" />',
            svg_text(
                60,
                334,
                f"Updated {stats['last_updated'].strftime('%d %b %Y, %I:%M %p %Z')}  ·  "
                f"{stats['commit_count']} commits in history",
                10.5,
                "#64748b",
            ),
            svg_text(
                1140,
                334,
                f"github.com/{username}/{repo}",
                10.5,
                "#64748b",
                anchor="end",
                family=MONO,
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Build everything
# --------------------------------------------------------------------------- #
def build_readme(stats: dict) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    target = int(CONFIG.get("target_problems", 500))
    percentage = 0 if target <= 0 else min(100, round(stats["total"] / target * 100))

    replacements = {
        "{{USERNAME}}": CONFIG["username"],
        "{{REPO}}": CONFIG["repo"],
        "{{REPO_URL}}": f"https://github.com/{CONFIG['username']}/{CONFIG['repo']}",
        "{{LAST_UPDATED}}": stats["last_updated"].strftime("%d %b %Y, %I:%M %p %Z"),
        "{{CURRENT_FOCUS}}": build_current_focus(stats),
        "{{STAT_BADGES}}": build_stat_badges(stats),
        "{{TOPIC_TARGET}}": str(CONFIG.get("topic_target", 25)),
        "{{TOPIC_TABLE}}": build_topic_table(stats),
        "{{NEXT_MILESTONE}}": build_next_milestone(stats),
        "{{TOTAL_SOLUTIONS}}": str(stats["total"]),
        "{{TARGET_PROBLEMS}}": str(target),
        "{{PROGRESS_PCT}}": str(percentage),
        "{{RECENT_TABLE}}": build_recent_table(stats),
        "{{ROADMAP}}": build_roadmap(stats),
        "{{LEETCODE_SECTION}}": build_leetcode_section(),
    }

    readme = template
    for placeholder, value in replacements.items():
        readme = readme.replace(placeholder, value)

    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", readme)))
    if unresolved:
        raise SystemExit(f"Unresolved template placeholders: {', '.join(unresolved)}")

    return readme.rstrip() + "\n"


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    stats = collect_solutions()

    README_PATH.write_text(build_readme(stats), encoding="utf-8")
    (ASSETS_DIR / "dashboard.svg").write_text(render_dashboard(stats), encoding="utf-8")
    (ASSETS_DIR / "activity.svg").write_text(render_activity(stats), encoding="utf-8")

    print(
        f"Rebuilt README.md, assets/dashboard.svg and assets/activity.svg "
        f"({stats['total']} solutions, {stats['covered']}/{stats['total_topics']} topics, "
        f"{stats['current_streak']}d streak)."
    )


if __name__ == "__main__":
    main()
