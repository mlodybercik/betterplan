from bs4 import BeautifulSoup
import requests
import copy as cp

proxy = """"""
LOG_LEVEL = 1


def divideList(list_, divider = "<br/>"):
	divided = []
	new = []
	for i in list_:
		if str(i) != divider:
			try:
				new.append(i.text)
			except:
				new.append(str(i))
		else:
			divided.append(new)
			new = []
			continue
	divided.append(new)
	return divided

def log(text, FG = 97, BG = 30):
	if LOG_LEVEL > 0:
		print("\033[{};{}m".format(FG,BG+10) + str(text) + "\033[0m")

def _getSite(url):
	get = requests.get(url, proxies=proxy)
	if get.ok:
		log("[_getSite] Site {} ok".format(url), 36)
		return get.text.encode("latin1").decode("utf-8")
	else:
		raise Exception("Couldn't download site {} error: {}".format(url))

def parsePlan(url):
	log("[parsePlan] Parsing: {}".format(url))
	site = BeautifulSoup(_getSite(url), "html5lib")
	return Plan(site)

class Entry:

	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return str(self.text)

class AdvEntry(Entry):
	def __init__(self, text):
		self.text = text.text
		self.plan = self.__parse(text)

	def __getitem__(self, a):
		return self.plan[a]

	def __iter__(self):
		return self.plan.__iter__()

	def __parse(self, text):
		spans = len(text.find_all("br")) + 1
		currPlan = []
		copy = cp.copy(text)

		def __extractSpan(atext):
			length = len(atext.text.split(" "))
			if length == 3:
				if atext.text.startswith("CKZ"):
					currPlan.append(["CKZ", "CKZ", "CKZ"])
					return
				p, n, s = atext.text.split(" ")
				currPlan.append([p, n, s])
				return
			elif length % 3 == 0:
				longtext = atext.text.split(" ")
				longtext.reverse()
				while len(longtext) > 0:
					s, n, p = longtext.pop(), longtext.pop(), longtext.pop()
					currPlan.append([s,n,p])
			else:
				log("[__extractSpan] length % 3 != 0")
				log("[__extractSpan] {}".format(atext))
				if atext.text.startswith("CKZ"):
					currPlan.append(["CKZ", "CKZ", "CKZ"])
			
			try:
				p = atext.find("span", "p").text
				n = atext.find("span", "n").text
				s = atext.find("span", "s").text
				# log("[__extractSpan] Adding {}, {}, {}".format(p, n, s))
				currPlan.append([p,n,s])
				return
			except AttributeError:
				p = atext.text
				currPlan.append([p, p, p])
				return
			except Exception:
				for i in divideList(copy):
					*p, n, s = "".join(i).split()
					if type(p) is list:
						p = "".join(p)
					if [p,n,s] not in currPlan:
						currPlan.append([p, n, s])
					# log("[afterException] Adding {}, {}, {}".format(p, n, s))
					copy.extract()
				return

		if text.text != "\xa0":
			if spans > 1:
				try:
					for _ in range(spans):
						asd = text.find_all("span")[0]
						if len(asd.text.split(" ")) == 1:
							asd = text.find_all("span")
						else:
							asd = text.find_all("span")[0].extract()
						__extractSpan(asd)
				except AttributeError:
					try:
						for i in divideList(copy):
							try:
								ddd = "".join(i).split(" ")
								if len(ddd) == 3:
									p, n, s = ddd
									currPlan.append([p,n,s])
								else:
									raise Exception
							except Exception:
								p, _, s = "".join(i).split(" ")
								currPlan.append([p,"?",s])
								log(text.text, 35)
					except Exception as e:
						log("[AdvEntry.__parse] Something went wrong... {}".format(e), 31)
						return currPlan
			else:
				__extractSpan(text)

			return currPlan
		else:
			return []

class Plan:
	plan = []
	no = ""
	def __init__(self, site):
		if type(site) is not BeautifulSoup:
			print(type(site))
			raise Exception("Couldn't decode, given object isn't a bs4.BS")
		self.plan = self.__parsePlan(site)
		self.no = site.find_all("span", "tytulnapis")[0].text
		if "#" in self.no:
			self.no = self.no.replace("#", "")

	def __len__(self):
		return len(self.plan)

	def __iter__(self):
		return self.plan.__iter__()

	def __getitem__(self, n):
		return self.plan[n]


	def __decode(self, text):
		try:
			return AdvEntry(text)
		except NotImplemented:
			return Entry(text)

	def __parsePlan(self, site):
		plan = [[], [], [], [], []]
		for single_line in site.body.div.table.tbody.tr.td.tbody.find_all("tr"):
			td = single_line.find_all("td", "l")
			if(len(td) == 0):
				continue
			for dzien in range(0, 5):
				try:
					plan[dzien].append(self.__decode(td[dzien]))
				except Exception as e:
					print(td[dzien])
					raise(Exception("chuj"))

		return plan

def generatePlanJSON(plan, removeAdditional = True):
	temp = [[], [], [], [], []]
	import json
	if removeAdditional:
		for day in range(len(plan)):
			for lesson in range(len(plan[day])):
				if plan[day][-1].text == "\xa0":
					del plan[day][-1]
					continue
				break

	for day in zip(plan, range(0,len(plan))):
		for lesson in zip(day[0], range(0, len(day[0]))):
			temp[day[1]].append(lesson[0].plan)

	return json.dumps(temp)

def __main__():
	print("Go. Away.")

def generatePlan(listOfPlans, typeOfPlan="teacher"):
	def checkMax():
		_list = []
		for i in zip(listOfPlans, range(len(listOfPlans))):
			_list.append(len(i[0][0]))
		return max(_list)

	maxDay = checkMax()

	def createPlan():
		planA = [[], [], [], [], []]
		for day in range(0,5):
			for _ in range(0,maxDay):
				planA[day].append([])
		return planA

	plans = {}
	if typeOfPlan == "teacher":
		# JSON generation for teacher plans
		for plan in listOfPlans:
			plan.no.replace("#", "H")
			for day in zip(plan, range(0, len(plan))):
				for lesson in zip(day[0], range(0, len(day[0]))):
					for group in lesson[0]:
						if group[1] in plans.keys():
							plans[group[1]][day[1]][lesson[1]].append([group[0], group[2], plan.no])
						else:
							plans[group[1]] = createPlan()
							plans[group[1]][day[1]][lesson[1]].append([group[0], group[2], plan.no])

	elif typeOfPlan == "classroom":
		# JSON generation for classroom plans
		for plan in listOfPlans:
			plan.no.replace("#", "H")
			for day in zip(plan, range(0, len(plan))):
				for lesson in zip(day[0], range(0, len(day[0]))):
					for group in lesson[0]:
						if group[2] in plans.keys():
							plans[group[2]][day[1]][lesson[1]].append([group[0], group[1], plan.no])
						else:
							plans[group[2]] = createPlan()
							plans[group[2]][day[1]][lesson[1]].append([group[0], group[1], plan.no])

	elif typeOfPlan == "class":
		for plan in listOfPlans:
			plan.no.replace("#", "H")
			for day in zip(plan, range(0, len(plan))):
				for lesson in zip(day[0], range(0, len(day[0]))):
					for group in lesson[0]:
						if plan.no in plans.keys():
							plans[plan.no][day[1]][lesson[1]].append([group[0], group[1], group[2]])
						else:
							plans[plan.no] = createPlan()
							plans[plan.no][day[1]][lesson[1]].append([group[0], group[1], group[2]])
	return plans


if __name__ == "__main__":
	__main__()

class NotImplemented(Exception):
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)
