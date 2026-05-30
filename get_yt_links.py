import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

queries = [
    "Beirut explosion CCTV",
    "Sri Lanka protesters storm president house",
    "Assam floods drone footage",
    "France riots fire street",
    "Turkey earthquake building collapse live",
    "Pakistan police clash protesters Lahore",
    "Myanmar military crackdown",
    "Delhi communal violence 2020",
    "Indonesia tsunami 2018 caught on camera",
    "Morocco earthquake panic"
]

for q in queries:
    url = "https://www.youtube.com/results?search_query=" + q.replace(" ", "+")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        if video_ids:
            print(f"{q}: https://www.youtube.com/watch?v={video_ids[0]}")
        else:
            print(f"{q}: No results")
    except Exception as e:
        print(f"{q}: Error {e}")
