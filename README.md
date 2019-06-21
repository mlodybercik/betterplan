# betterplan
Webscraper for lesson plan scheduler made by Vulcan. `Plan lekcji Optivum`

## Usage:
First make an array of all plans, using `betterplan.parsePlan()`.
```python
import betterplan
import json

plans = []
for i in range(amount):
	plans.append(betterplan.parsePlan("url to page"))
```
`parsePlan` returns array which is made out of `AdvEntry`'ies and `Entry`'ies. Advanced (this is what Adv stands for lol) contains one more array with information about `classroom`, `classname` and `teacher` for group halves of subgroups. If parser couldn't read it it'll make it a normal `Entry` containing only inner text. So for eg.

`x = betterplan.parsePlan("url")`\
`x[0]` whole first day.\
`x[0][1]` second entry of first day.\
`x[0][1][2]` third subgroup in second entry on first day.\
^ that one, contains `[classname, teachername, classroom]` sooo,\
`x[0][1][2][0]` class name of third subgroup in second entry on first day.\
`x.plan[0][0].plan[0][0]` == `x[0][0][0][0]`.\
btw, `x.no` contains name of parsed plan.

Then, pass that list to `betterplan.generatePlan()` with corresponding type.
```python
plan = betterplan.generatePlan(plans, "type")
```
Possible types are:
 - `classroom` returning plans for every unique classroom.
 - `class` returning plans for every unique group.
 - `teacher` returning plans for every unique teacher.

Now, do whatever you want, for eg. you could put it inside JSON for website development or exporting.

```python
betterplan.generatePlanJSON(plan)
```

I hate explaining my *spaghetti* code, better if you try it for yourself. Type `wygenerowano ? za pomocą programu Plan lekcji Optivum` in google, then look for iframe url of plan.

## TODO:
- fix *spaghetti*
- add comments
- add in-code documentation
