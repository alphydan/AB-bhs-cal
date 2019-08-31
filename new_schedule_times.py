#!/usr/bin/env python

import csv
# definition of when the class periods begin and end
from datetime import timedelta as td

reg = td(hours=8, minutes=20)  # registration
l1 = td(hours=8, minutes=40)   # 1st period
l2 = td(hours=10, minutes=5)  # 2nd period
l3 = td(hours=11, minutes=15)  # 3rd period
l4 = td(hours=13, minutes=15)  # 4th period
l5 = td(hours=14, minutes=20)  # 5th period
lunch = td(hours=12, minutes=20)  # lunch

plus_a_registration = td(hours=0, minutes=20)
plus_half_an_hour = td(hours=0, minutes=30)
plus_a_lunch = td(hours=0, minutes=50)
plus_an_hour = td(hours=1, minutes=0)
plus_a_lesson = td(hours=1, minutes=5)
plus_half_a_day = td(hours=4, minutes=0)
plus_a_working_day = td(hours=7, minutes=0)

# timetable_name = raw_input("What is the username of the teacher? (without .csv ): ")
timetable_name = 'afeito'
timetable_path_n_file = './timetable_files/' + str(timetable_name) + '_TT_2019_2020.csv'
# timetable_file = open(path_n_file, 'r',)

###########################
# Read Timetable CSV file #
timetable = open(timetable_path_n_file, 'r')
tt_reader = csv.reader(timetable)
tt_headers = next(tt_reader)


# correspondance:
# MoA: 0, TueA: 1, ... MoB: 5, etc
week_dic = {'Monday A': 0, 'Tuesday A': 1, 'Wednesday A': 2,
            'Thursday A': 3, 'Friday A': 4, 'Monday B': 5,
            'Tuesday B': 6, 'Wednesday B': 7,
            'Thursday B': 8, 'Friday B': 9}

timetable_dict = {}
for i, row in enumerate(tt_reader):
    week = [x.replace("\xc2\xa0", "") for x in row[1:]]
    week = [x.replace("\xa0", "") for x in week]
    if i < 4: # skip name, date, blanks
        continue
    if i % 2 == 0: # even rows
        # this is hackish, quick and dirty ...
        # but no more time for feeding pandas today :-/
        if row[0] == 'Wednesday' and i < 10:
            timetable_dict[2] = week
            last_day = 2
        elif row[0] == 'Wednesday' and i > 12:
            timetable_dict[7] = week
            last_day = 7
        else:
            timetable_dict[week_dic[row[0]]] = week
            last_day = week_dic[row[0]]
        continue
    if i % 2 == 1: #even rows
        # add the rooms corresponding to the class to the dictionary
        timetable_dict[last_day] = (timetable_dict[last_day], week)


## Combine the information about which lesson: timtable_dict[key][0]
## with the information about where it takes place:  timtable_dict[key][1]

for i in range(0,10):
    tt_n_room = zip(timetable_dict[i][0], timetable_dict[i][1])
    combined = []
    for x in tt_n_room:
        if x[0]: # is there a class that period?
            # yes, then make a string with class + @location
            combined.append(x[0] + ' @' + x[1])
        else:
            combined.append('')
    timetable_dict[i] = combined

print(timetable_dict)
