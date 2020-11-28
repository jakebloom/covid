import json
import os
from matplotlib import pyplot
from datetime import datetime
from urllib import request

PATH = './out'
URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'

GRAPHS = [
  ['San Francisco'],
  ['San Francisco', 'San Mateo', 'Santa Clara'],
  ['San Francisco', 'San Mateo', 'Santa Clara', 'Los Angeles']
]
res = request.urlopen(URL)
california = [r.decode('utf-8').strip().split(',') for r in res if 'California' in r.decode('utf-8')]
files = []

data = {}
for row in california:
  county = row[1]
  if county not in data:
    data[county] = []
  date = row[0]
  cases = row[4]
  data[county].append((date, cases))

try:
  os.mkdir(PATH)
except FileExistsError:
  pass
except e:
  raise e

for graphCounties in GRAPHS:
  pyplot.clf()

  for county in data:
    if county in graphCounties:
      s = sorted(data[county], key=lambda day: datetime.strptime(day[0], "%Y-%m-%d").timestamp())
      days = [x[0] for x in s]
      totalCases = [int(x[1]) for x in s]
      cases = [totalCases[0]]
      for i in range(1, len(totalCases)):
        cases.append(totalCases[i] - totalCases[i - 1])

      averageCases = []
      for i in range(7, len(cases)):
        averageCases.append(sum(cases[i - 7:i]) / 7)

      pyplot.plot(days[7:], averageCases, label=county + " {:.2f}".format(averageCases[-1]))

  pyplot.legend()
  locs, _ = pyplot.xticks()
  xticks = [locs[0], locs[len(locs) // 4], locs[len(locs) // 2], locs[len(locs) * 3 // 4], locs[-1]]
  pyplot.xticks(xticks)
  pyplot.xlabel('Date')
  pyplot.ylabel('7 Day Average New Cases')
  pyplot.grid(axis='y')

  filename = PATH + '/' + '_'.join(graphCounties).lower().replace(' ', '_') + '.png'
  pyplot.savefig(filename)
  files.append(filename[2:])

with open(PATH + '/files.json', 'w') as f:
  f.write(json.dumps(files))