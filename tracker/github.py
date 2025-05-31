import requests
import datetime
import os
from dotenv import load_dotenv

def track_commits(username, token):
    today = datetime.datetime.now().date().isoformat()
    url = f"https://api.github.com/search/commits?q=author:{username}+committer-date:{today}"
    headers = {"Accept": "application/vnd.github.cloak-preview", "Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json().get("items", [])
        print(f"Commits for {today}:")
        if not commits:
            print("No commits found.")
        for commit in commits:
            message = commit['commit']['message']
            commit_time_utc = commit['commit']['committer']['date']
            # Parse ISO time and convert to local time
            try:
                dt_utc = datetime.datetime.fromisoformat(commit_time_utc.replace('Z', '+00:00'))
                dt_local = dt_utc.astimezone()
                time_str = dt_local.strftime('%d-%m-%Y %H:%M:%S')
            except Exception:
                time_str = commit_time_utc
            print(f"- {message} (at {time_str})")
    else:
        print("Failed to fetch commits:", response.text)

def get_commit_count(username, token):
    today = datetime.datetime.now().date().isoformat()
    url = f"https://api.github.com/search/commits?q=author:{username}+committer-date:{today}"
    headers = {"Accept": "application/vnd.github.cloak-preview", "Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json().get("items", [])
        return len(commits)
    return 0