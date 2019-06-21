import json
import betterplan

plans = []
for i in range(1,997):
	plans.append(betterplan.parsePlan("dont think about it lmao"))

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
