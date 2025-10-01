import requests
import os

USERNAME = "RudrasenaReddy87"
README_FILE = "README.md"
TOKEN = os.getenv("GH_PAT")
HEADERS = {'Authorization': f'token {TOKEN}'} if TOKEN else {}

def get_languages(username):
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos = requests.get(repos_url, headers=HEADERS).json()
    language_stats = {}
    for repo in repos:
        if not repo.get("fork"):
            langs = requests.get(repo["languages_url"], headers=HEADERS).json()
            for lang, count in langs.items():
                language_stats[lang] = language_stats.get(lang, 0) + count
    return language_stats

def calculate_percentages(language_stats):
    total = sum(language_stats.values())
    percentages = {lang: round((count / total) * 100) for lang, count in language_stats.items()}
    return dict(sorted(percentages.items(), key=lambda x: x[1], reverse=True))

def generate_table(percentages):
    table = """
## 🛠 Skills Overview (Auto Updated)

<table style="border-collapse: collapse; border-radius: 10px; overflow: hidden; width: 100%;">
  <tr>
    <th>Language / Tool</th>
    <th>Proficiency</th>
  </tr>
"""
    colors = ["#3776AB", "#E34F26", "#61DAFB", "#F7DF1E", "#4DB33D", "#764ABC", "#FF9800"]
    for i, (lang, percent) in enumerate(percentages.items()):
        color = colors[i % len(colors)]
        table += f"""
  <tr>
    <td><b>{lang}</b></td>
    <td>
      <div style="background:#ddd; border-radius:8px; width:100%;">
        <div style="width:{percent}%; background:{color}; padding:5px 0; border-radius:8px; color:white; text-align:center;">{percent}%</div>
      </div>
    </td>
  </tr>
"""
    table += "</table>\n"
    return table

def update_readme(new_table):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    start_marker = "## 🛠 Skills Overview"
    if start_marker in content:
        before = content.split(start_marker)[0]
        updated_content = before + new_table + "\n\n"
    else:
        updated_content = content + "\n" + new_table + "\n"
    # Add GitHub Stats
    github_stats = f"""
## 📊 GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username={USERNAME}&show_icons=true&theme=radical)

## 🔥 GitHub Streaks

![GitHub Streaks](https://github-readme-streak-stats.herokuapp.com/?user={USERNAME}&theme=radical)
"""
    updated_content += github_stats
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("✅ README updated successfully!")

if __name__ == "__main__":
    stats = get_languages(USERNAME)
    percentages = calculate_percentages(stats)
    table = generate_table(percentages)
    update_readme(table)
