from requests_html import HTMLSession

baseUrl = "https://www.mojposao.ba/#!searchjobs;keyword=;page=1;title=all;range=today;location=all;i=32_31_47;lk=Sarajevo;state=all"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

session = HTMLSession()
r = session.get(baseUrl, headers=headers)
r.html.render()
print(r.html.search("upravljanje"))
print(r.html.text)