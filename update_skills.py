import requests
import os
import json

USERNAME = "RudrasenaReddy87"
README_FILE = "README.md"
TOKEN = os.getenv("GH_PAT")
HEADERS = {'Authorization': f'token {TOKEN}'} if TOKEN else {}

def get_languages(username):
    repos = requests.get(f"https://api.github.com/users/{username}/repos", headers=HEADERS).json()
    stats = {}
    for repo in repos:
        if not repo.get("fork"):
            langs = requests.get(repo["languages_url"], headers=HEADERS).json()
            for lang, count in langs.items():
                stats[lang] = stats.get(lang, 0) + count
    return stats

def generate_table(stats):
    total = sum(stats.values())
    percentages = {lang: round(count / total * 100) for lang, count in stats.items()}
    table = "<table style='border-collapse: collapse; border-radius: 10px; overflow: hidden; width: 100%;'>"
    table += "<tr><th>Language/Tool</th><th>Proficiency</th><th>Hours Spent</th></tr>"
    colors = ["#3776AB","#E34F26","#61DAFB","#F7DF1E","#4DB33D","#764ABC","#FF9800"]
    for i, (lang, perc) in enumerate(sorted(percentages.items(), key=lambda x: x[1], reverse=True)):
        color = colors[i % len(colors)]
        table += f"<tr><td><b>{lang}</b></td>"
        table += f"<td><div style='background:#ddd;border-radius:8px;width:100%;overflow:hidden;'>"
        table += f"<div style='width:{perc}%;background:{color};padding:5px 0;border-radius:8px;color:white;text-align:center;'>{perc}%</div></div></td>"
        table += f"<td>{perc*10}+ hrs</td></tr>"
    table += "</table>"
    return table

def update_readme(table_html):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    start = "<!-- SKILLS_TABLE_START -->"
    end = "<!-- SKILLS_TABLE_END -->"
    new_content = content.split(start)[0] + start + "\n" + table_html + "\n" + end + content.split(end)[1]
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    stats = get_languages(USERNAME)
    table_html = generate_table(stats)
    update_readme(table_html)
    print("✅ README updated!")
