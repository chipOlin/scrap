import requests
from bs4 import BeautifulSoup
import json


def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "accept": "* / *"
    }

    r = requests.get(url, timeout=5)
    # with open("sale_notebook.html", "wb") as f:
    #     f.write(r.content)

    # with open("sale_notebook.html", "rb") as f:
    #     html_content = f.read()

    notebooks = []
    # soup = BeautifulSoup(html_content, "lxml")
    soup = BeautifulSoup(r.content, "lxml")
    goods = soup.find_all("tr", class_="hide-mob")
    for item in goods:
        if (not item.td.find("div", class_="instock") is None):
            title = item.td.a.string.replace("восстановленный ", "")
            link = "https://www.notik.ru" + item.td.a["href"]
            series = item.td.find("b", class_="wordwrap").string
            vendor_code = item.td.find("div", class_="artikul").string

            characteristics = item.findNext("tr")
            price = characteristics.find("a", class_="tocart")["ecprice"]
            description = characteristics.find("a", class_="tocart")["ecname"]

            notebooks.append(
                {
                    "Title": title,
                    "Description": description,
                    "Link": link,
                    "Series": series,
                    "Vendor code": vendor_code,
                    "Price": price
                }
            )
    with open("notebooks.json", "w", encoding="utf-8") as file:
        json.dump(notebooks, file, indent=4, ensure_ascii=False)
    print("scraping finished")


def get_json(filename):
    with open(filename) as f:
        data = json.load(f)
    for x in data:
        if "92050" in x["Vendor code"]:
            print("Y")


def main():
    # sites scraping:
    # https://www.notik.ru/
    # https://www.alt-del.ru/
    # get_html("https://www.notik.ru/search_catalog/filter/sales.htm?source=menu&sortby=price")  # - all models
    get_json("notebooks.json")


if __name__ == '__main__':
    main()
