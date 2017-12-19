import json
import matplotlib.pyplot as plt
import sys

months = [1,2,3,4,5,6,7,8,9,10,11,12]
years = [2009,2010,2011,2012,2013,2014,2015,2016,2017]
month_year_map = {}
for i in range(0, len(years)):
    month_year_map[years[i]] = {}

msgs_per_month_year = []
months_years = []
for i in range(0, len(years)):
    for j in range(0, len(months)):
        msgs_per_month_year.append(0)
        months_years.append((years[i], months[j]))
        month_year_map[years[i]][months[j]] = len(msgs_per_month_year) - 1

people = json.load(open('people.json'))

friend = sys.argv[1]

friend_add_month = int(people[friend]['date_added']['month'])
friend_add_year = int(people[friend]['date_added']['year'])

if int(people[friend]['num_messages']) != 0:
    for year in people[friend]['message_years']:
        for month in people[friend]['message_years'][year]:
            for day in people[friend]['message_years'][year][month]:
                msgs_per_month_year[month_year_map[int(year)][int(month)]] += people[friend]['message_years'][year][month][day]

    truncated_msgs = msgs_per_month_year[month_year_map[friend_add_year][friend_add_month]:-1]
    months_as_friends = months_years[month_year_map[friend_add_year][friend_add_month]:-1]

    plt.plot(msgs_per_month_year)
    plt.show()
else:
    print('No messages shared.')
