import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import collections

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
        months_years.append('{0}/{1}'.format(str(months[j]), str(years[i])))
        month_year_map[years[i]][months[j]] = len(msgs_per_month_year) - 1

people = json.load(open('people.json'))

friend = sys.argv[1]


if int(people[friend]['num_messages']) != 0:
    for year in people[friend]['message_years']:
        for month in people[friend]['message_years'][year]:
            for day in people[friend]['message_years'][year][month]:
                msgs_per_month_year[month_year_map[int(year)][int(month)]] += people[friend]['message_years'][year][month][day]

    plt.figure()
    if 'date_added' in people[friend]:
        friend_add_month = int(people[friend]['date_added']['month'])
        friend_add_year = int(people[friend]['date_added']['year'])
        plt.axvline(month_year_map[friend_add_year][friend_add_month], color = 'r')

        truncated_msgs = msgs_per_month_year[month_year_map[friend_add_year][friend_add_month]:-1]
        months_as_friends = months_years[month_year_map[friend_add_year][friend_add_month]:-1]



    x = np.arange(len(msgs_per_month_year))
    plt.bar(x, height = msgs_per_month_year)

    plt.xticks([6, 18, 30, 42, 54, 66, 78, 90, 102], [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017])
    plt.xlabel('Year')
    plt.ylabel('Number of messages exchanged')
    plt.title('High School & College Friend')
    plt.show()
else:
    print('No messages shared.')

# bar chart of people added per year
num_friends_per_year = {}
for person in people:
    if 'date_added' in people[person]:
        if people[person]['date_added']['year'] not in num_friends_per_year:
            num_friends_per_year[people[person]['date_added']['year']] = 1
        else:
            num_friends_per_year[people[person]['date_added']['year']] += 1

sorted_dictionary = collections.OrderedDict(sorted(num_friends_per_year.items()))
years_arr = sorted_dictionary.keys()
friends_per_year_arr = sorted_dictionary.values()

x = np.arange(len(years_arr))
plt.figure()
plt.bar(x, friends_per_year_arr)
plt.xticks(x, years_arr)
plt.xlabel('Year')
plt.ylabel('Number of Added Friends')
plt.title('Number of added friends per year')
plt.show()
