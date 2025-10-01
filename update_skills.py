import requests
import os

USERNAME = "RudrasenaReddy87"  # your GitHub username
README_FILE = "README.md"

# Get token from environment
TOKEN = os.getenv("GH_PAT")
HEADERS = {'Authorization': f'token {TOKEN}'} if TOKEN else {}

# Function to get languages used across all repos
def get_languages(username):
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos = requests.get(repos_url, headers=HEADERS).json()

    language_stats = {}
    for repo in repos:
        if not repo.get("fork"):  # ignore forks
            lang_url = repo["languages_url"]
            langs = requests.get(lang_url, headers=HEADERS).json()
            for lang, count in langs.items():
                language_stats[lang] = language_stats.get(lang, 0) + count

    return language_stats


# Convert to percentages
def calculate_percentages(language_stats):
    total = sum(language_stats.values())
    percentages = {lang: round((count / total) * 100, 2) for lang, count in language_stats.items()}
    return dict(sorted(percentages.items(), key=lambda x: x[1], reverse=True))


# Generate progress bar HTML
def generate_table(percentages):
    table = """
## 🛠 Skills Overview (Auto Updated)

<table style="border-collapse: collapse; border-radius: 10px; overflow: hidden; width: 100%;">
  <tr>
    <th>Language/Tool</th>
    <th>Proficiency</th>
  </tr>
"""
    colors = ["#3776AB", "#E34F26", "#61DAFB", "#F7DF1E", "#4DB33D", "#764ABC", "#FF9800"]

    i = 0
    for lang, percent in percentages.items():
        color = colors[i % len(colors)]
        table += f"""
  <tr>
    <td><b>{lang}</b></td>
    <td>
      <div style="background:#ddd; border-radius:8px; width:100%;">
        <div style="width:{percent}%; background:{color}; padding:4px; border-radius:8px; color:white; text-align:center;">{percent}%</div>
      </div>
    </td>
  </tr>
"""
        i += 1

    table += "</table>\n"
    return table


# Update README.md
def update_readme(new_table):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "## 🛠 Skills Overview"
    if start_marker in content:
        before = content.split(start_marker)[0]
        updated_content = before + new_table
    else:
        updated_content = content + "\n" + new_table

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)


if __name__ == "__main__":
    stats = get_languages(USERNAME)
    percentages = calculate_percentages(stats)
    new_table = generate_table(percentages)

    # Add GitHub stats section
    github_stats = """
## 📊 GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=RudrasenaReddy87&show_icons=true&theme=radical)

## 🔥 GitHub Streaks

![GitHub Streaks](https://github-readme-streak-stats.herokuapp.com/?user=RudrasenaReddy87&theme=radical)
"""

    full_content = new_table + "\n" + github_stats
    update_readme(full_content)
    print("✅ README updated with latest skills table and GitHub stats.")
