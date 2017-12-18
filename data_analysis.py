from bs4 import BeautifulSoup
import os
import json
import matplotlib

conversations = os.listdir('messages/')

month_dict = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6,
                'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12,
                'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5,
                'June' : 6, 'July' : 7, 'August' : 8, 'September' : 9, 'October' : 10,
                'November' : 11, 'December' : 12}
people = {}

def does_file_exist_in_dir(filename):
    directory = os.listdir('.')
    for i in range(0, len(directory)):
        if directory[i] == filename:
            return True
    return False



if not does_file_exist_in_dir('people.json'):
    for i in range(0, len(conversations)):
        f = open('{0}/{1}'.format('messages', conversations[i]))
        soup = BeautifulSoup(f, 'html5lib')
        person = soup.find('title').text.split("with ")[1].replace(' ', '')
        if(len(person.split(',')) == 1):
            people[person] = {}
            people[person]['num_messages'] = len(soup.find_all('p'))
            people[person]['message_years'] = {}

            # index all messages of a person based on year/month/day
            for timestamp in soup.findAll(attrs={'class': 'meta'}):
                msg_year = int(timestamp.text.split(',')[2].split('at')[0].replace(' ', ''))
                msg_month = month_dict[timestamp.text.split(',')[1].split(' ')[1].replace(' ', '')]
                msg_day = int(timestamp.text.split(',')[1].split(' ')[2].replace(' ', ''))

                if msg_year not in people[person]['message_years']:
                    people[person]['message_years'][msg_year] = { msg_month : { msg_day : 1 }}
                else:
                    if msg_month not in people[person]['message_years'][msg_year]:
                        people[person]['message_years'][msg_year][msg_month] = {msg_day : 1}
                    else:
                        if msg_day not in people[person]['message_years'][msg_year][msg_month]:
                            people[person]['message_years'][msg_year][msg_month][msg_day] = 1
                        else:
                            people[person]['message_years'][msg_year][msg_month][msg_day] += 1

        f.close()
        print('{0}/{1} finished'.format(i, len(conversations)))

    with open('people.json', 'w') as fp:
        json.dump(people, fp)
else:
    people = json.load(open('people.json'))

# print list of people sorted by num messages
sorted_people = sorted(people.items(), key=lambda x:x[1], reverse = True)


# Number of people you have exchanged at least 2 messages with
min_messages = 2
count = 0
for i in range(0, len(sorted_people)):
    if(sorted_people[i][1] < min_messages):
        count += 1
        break
    count = i



# get list of when added/dropped
f = open('html/friends.htm')
soup = BeautifulSoup(f, 'html5lib')
friend_list = soup.find_all('ul')[1]
friend_list_pending = soup.find_all('ul')[2]
friend_list_request = soup.find_all('ul')[3]
friend_list_removed = soup.find_all('ul')[4]


friend_array = []
for name in friend_list.children:
    name_str = name.text

    str_array = name_str.split('[')
    if(len(str_array) != 1):
        real_str = str_array[0] + str_array[1].split(']')[1]
        name = str_array[0].replace(' ', '')
        date_added = str_array[1].split(']')[1].split('(')[1].split(')')[0]
    else:
        real_str = str_array[0]
        name = str_array[0].split('(')[0].replace(' ', '')
        date_added = str_array[0].split('(')[1].split(')')[0]

    date_arr = date_added.split(',')
    month = month_dict[date_arr[0].split(' ')[0]]
    day = int(date_arr[0].split(' ')[1])
    if(len(date_arr) == 1):
        year = 2017
    else:
        year = int(date_arr[1].replace(' ', ''))

    if name not in people:
        people[name] = {}
        people[name]['num_messages'] = 0

    people[name]['date_added'] = {}
    people[name]['date_added']['day'] = day
    people[name]['date_added']['month'] = month
    people[name]['date_added']['year'] = year

for name in friend_list_removed.children:
    name_str = name.text

    str_array = name_str.split('[')
    if(len(str_array) != 1):
        real_str = str_array[0] + str_array[1].split(']')[1]
        name = str_array[0].replace(' ', '')
        date_added = str_array[1].split(']')[1].split('(')[1].split(')')[0]
    else:
        real_str = str_array[0]
        if(len(str_array[0].split('(')) != 1):
            name = str_array[0].split('(')[0].replace(' ', '')
            date_added = str_array[0].split('(')[1].split(')')[0]
        else: # no date
            name = str_array[0].replace(' ', '')
            if name not in people:
                people[name] = {}
                people[name]['num_messages'] = 0

            continue

    date_arr = date_added.split(',')
    month = month_dict[date_arr[0].split(' ')[0]]
    day = int(date_arr[0].split(' ')[1])
    if(len(date_arr) == 1):
        year = 2017
    else:
        year = int(date_arr[1].replace(' ', ''))

    if name not in people:
        people[name] = {}
        people[name]['num_messages'] = 0

    people[name]['date_removed'] = {}
    people[name]['date_removed']['day'] = day
    people[name]['date_removed']['month'] = month
    people[name]['date_removed']['year'] = year


#print(people)
add_friend_years = {}
total = 0
for name in people:
    if 'date_added' in people[name]:
        if people[name]['date_added']['year'] not in add_friend_years:
            add_friend_years[people[name]['date_added']['year']] = 1
        else:
            add_friend_years[people[name]['date_added']['year']] += 1
        total += 1

removed_friend_years = {}
for name in people:
    if 'date_removed' in people[name]:
        if people[name]['date_removed']['year'] not in removed_friend_years:
            removed_friend_years[people[name]['date_removed']['year']] = 1
        else:
            removed_friend_years[people[name]['date_removed']['year']] += 1
        total += 1


with open('people.json', 'w') as fp:
    json.dump(people, fp)


top = 300
# print top 5 people
#print('Top {0} communicators'.format(top))
#for i in range(0, top):
#    print('{0}: {1}'.format(sorted_people[i][0].encode('utf-8'), sorted_people[i][1]))

#print("Number of people you have exchanged at least {0} messages with: {1}".format(min_messages, count))
