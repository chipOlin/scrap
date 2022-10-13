import requests
from bs4 import BeautifulSoup
import json


def get_html_notik(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "accept": "* / *"
    }

    r = requests.get(url, timeout=5)

    notebooks = []
    # soup = BeautifulSoup(html_content, "lxml")
    soup = BeautifulSoup(r.content, "lxml")
    goods = soup.find_all("tr", class_="hide-mob")
    for item in goods:
        # print(item.td.div["title"] != "Нет в наличии")
        # if (not item.td.find("div", class_="instock") is None):
        if (item.td.div["title"] != "Нет в наличии"):
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
                    "Price": int(price)
                }
            )
    
    # def sortByPrice(e):
    #     return e['Price']
    # notebooks.sort(key=sortByPrice)
    
    return notebooks


def get_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def save_json(data):
    with open("notik.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def update_list_goods(fn):
    list_notebooks = get_json(fn)
    notik_data = get_html_notik("https://www.notik.ru/search_catalog/filter/sales.htm")  # - all models

    ln_vendCode = [x["Vendor code"] for x in list_notebooks]
    i = 0
    for ndata in notik_data:
        if not ndata["Vendor code"] in ln_vendCode:
            i += 1
            list_notebooks.append(ndata)
    save_json(list_notebooks)
    print(f"add {i} position")

    nd_vendCode = [x["Vendor code"] for x in notik_data]
    i, j = (0, 0)
    for lndata in list_notebooks:
        if not lndata["Vendor code"] in nd_vendCode:
            d = list_notebooks.pop(i)
            j += 1
            print(f"remove \"{d['Title']}\" position: {d['Link']}")
        i += 1
    save_json(list_notebooks)
    print(f"remove {j} position")


def show_goods(fn):
    data = get_json(fn)
    print(json.dumps(data, indent=2, sort_keys=True))


def main():
    # sites scraping:
    # https://www.notik.ru/
    # https://www.alt-del.ru/
    
    # """
    # active steps
    # """
    fileGoods = "notik.json"
    update_list_goods(fileGoods)
    show_goods(fileGoods)


if __name__ == '__main__':
    main()
