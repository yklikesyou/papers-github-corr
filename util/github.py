import re

def valid_github_url_check(url: str):
    # example: https://github.com/pswkiki/SphereGAN
    return bool(re.match(r"^https://github.com/([^ \t\r\n\v\f]+)/([^ \t\r\n\v\f]+)", url))

def get_github_api_url(username: str, repo: str):
    return f"https://api.github.com/repos/{username}/{repo}"