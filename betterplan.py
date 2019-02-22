from bs4 import BeautifulSoup
import requests

main_site = """ricardo milos is my"""
plan_site = """hero"""
proxy = """"""
LOG_LEVEL = 1


def log(text):
    if LOG_LEVEL > 0:
        print(text)


def _getSite(url):
    get = requests.get(url, proxies=proxy)
    if get.ok:
        log("[_getSite] Site {} ok".format(url))
        return get.text.encode("latin1").decode("utf-8")
    else:
        raise Exception("Couldn't download site {} error: {}".format(url))


def parsePlan(url):
    log("[parsePlan] Parsing: {}".format(url))
    site = BeautifulSoup(_getSite(url), "html5lib")
    return Plan(site)


def getList():
    list = []
    classlist = BeautifulSoup(_getSite(main_site + plan_site), "html5lib")
    for ul in classlist.find_all("ul"):
        dict = {}
        for li in ul.find_all("li"):
            dict[li.text] = li.a.get("href")
        list.append(dict)
    return list


class Entry:

    def __init__(self, text, type="class"):
        self.text = text
        self.type = type

    def __repr__(self):
        return self.text


class AdvEntry(Entry):
    pass


class Plan:
    plan = []

    def __init__(self, site):
        if type(site) is not BeautifulSoup:
            print(type(site))
            raise Exception("Couldn't decode, given object isn't a bs4.BS")
        self.plan = self.__parsePlan(site)

    def __decode(self, text):
        try:
            # return AdvEntry
            raise Exception("not implemented lmao")
        except Exception:
            log("[__decode] Couldn't decode: {}".format(text))
            return Entry(text)

    def __parsePlan(self, site):
        plan = [[], [], [], [], []]
        log("[__parsePlan] Parsing plan")
        for single_line in site.body.div.table.tbody.tr.td.find_all("tr"):
            td = single_line.find_all("td")
            if(len(td) == 0):
                continue
            for i in range(2, 7):
                plan[i-2].append(self.__decode(td[i].text))

        print(plan)
        for i in range(0, 5):
            plan[i].remove(plan[i][0])
        return plan


def __main__():
    pass


if __name__ == "__main__":
    __main__()
