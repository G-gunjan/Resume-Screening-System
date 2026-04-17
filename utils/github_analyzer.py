import requests

def github_score(username):
    if not username:
        return 0

    try:
        user = requests.get(f"https://api.github.com/users/{username}").json()
        repos = requests.get(f"https://api.github.com/users/{username}/repos").json()

        followers = user.get("followers", 0)

        stars = sum(r.get("stargazers_count", 0) for r in repos)
        forks = sum(r.get("forks_count", 0) for r in repos)
        langs = len(set(r.get("language") for r in repos if r.get("language")))

        score = (
            0.3 * min(followers / 100, 1) +
            0.3 * min(stars / 200, 1) +
            0.2 * min(forks / 100, 1) +
            0.2 * min(langs / 10, 1)
        )

        return min(score, 1)

    except:
        return 0