import re


def check_url(url: str) -> str | None:
    regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return url if len(re.findall(regex, url)) == 1 else None
