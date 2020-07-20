import csv
from matplotlib import pyplot
from datetime import datetime

with open('./cali.csv') as f:
  reader = csv.reader(f)
  data = {}
  for row in reader:
    county = row[1]
    if county not in data:
      data[county] = []
    date = row[0]
    cases = row[4]
    data[county].append((date, cases))

  for county in data:
    if county in ['San Francisco', 'San Mateo', 'Santa Clara']:
      s = sorted(data[county], key=lambda day: datetime.strptime(day[0], "%Y-%m-%d").timestamp())
      days = [x[0] for x in s]
      totalCases = [int(x[1]) for x in s]
      cases = [totalCases[0]]
      for i in range(1, len(totalCases)):
        cases.append(totalCases[i] - totalCases[i - 1])
      # pyplot.plot(days, cases)
      averageCases = []
      for i in range(7, len(cases)):
        averageCases.append(sum(cases[i - 7:i]) / 7)
      pyplot.plot(days[7:], averageCases, label=county)
  pyplot.legend()
  locs, _ = pyplot.xticks()
  xticks = [locs[0], locs[len(locs) // 2], locs[-1]]
  pyplot.xticks(xticks)
  pyplot.xlabel('Date')
  pyplot.ylabel('7 Day Average New Cases')
  pyplot.show()
  


