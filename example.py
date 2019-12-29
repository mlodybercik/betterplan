import json
import betterplan
import threading
import time

plans = []
todo = []

class Collector(threading.Thread):
	def run(self):
		global plans
		global todo
		while len(todo) > 0:
			plans.append(betterplan.parsePlan("".format(todo.pop())))

todo = list(range(1, 26))
threads = []

for i in range(5):
	threads.append(Collector())

for i in range(5):
	threads[i].start()

for i in threads:
	i.join()

tp = betterplan.generatePlan(plans, "classroom")
for i in tp.keys():
	with open("nau/s/" + i + ".json", "w") as fil3:
		fil3.write(json.dumps(tp[i]))

tp = betterplan.generatePlan(plans, "class")
for i in tp.keys():
	with open("nau/c/" + i + ".json", "w") as fil3:
		fil3.write(json.dumps(tp[i]))

tp = betterplan.generatePlan(plans, "teacher")
for i in tp.keys():
	with open("nau/n/" + i + ".json", "w") as fil3:
		fil3.write(json.dumps(tp[i]))
