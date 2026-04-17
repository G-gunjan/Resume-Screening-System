import re

def extract_github_links(text):

    if not text:
        return []

    text_lower = text.lower()

    # ✅ FIXED PATTERN (handles with or without https)
    url_pattern = r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)*"

    links = re.findall(url_pattern, text_lower)

    # Normalize links (add https if missing)
    links = [
        link if link.startswith("http") else "https://" + link
        for link in links
    ]

    # Fallback: Github: username
    if not links:
        username_pattern = r"github:?\s*([A-Za-z0-9_-]+)"
        usernames = re.findall(username_pattern, text_lower)
        links = [f"https://github.com/{u}" for u in usernames]

    return list(set(links))


def extract_usernames(github_links):

    if not github_links:
        return []

    usernames = []

    for link in github_links:
        parts = link.rstrip("/").split("/")
        if len(parts) >= 4:
            usernames.append(parts[3])

    return list(set(usernames))
