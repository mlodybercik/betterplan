from bs4 import BeautifulSoup
import requests

main_site = """naaah"""
plan_site = """i wont give it to ya"""
proxy = """"""


def parsePlan(url):
    get = requests.get(main_site + url, proxies=proxy)
    if get.ok:
        site = BeautifulSoup(get.text.encode("latin1").decode("utf-8"), "html5lib")
        return Plan(site)
    else:
        raise Exception("Couldn't download site " + url)


class Entry:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text


class Plan:
    plan = []

    def __init__(self, site):
        if type(site) is not BeautifulSoup:
            print(type(site))
            raise Exception("Couldn't decode, given object isn't a bs4.BS")
        self.plan = self.__parsePlan(site)

    def __parsePlan(self, site):
        plan = [[], [], [], [], []]
        for single_line in site.body.div.table.tbody.tr.td.find_all("tr"):
            td = single_line.find_all("td")
            if(len(td) == 0):
                continue
            for i in range(2, 7):
                plan[i-2].append(Entry(td[i].text))

        print(plan)
        for i in range(0, 5):
            plan[i].remove(plan[i][0])
        return plan


def __main__():
    Plan("nope")


if __name__ == "__main__":
    __main__()
