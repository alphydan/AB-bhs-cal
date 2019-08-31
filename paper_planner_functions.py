from datetime import datetime as dt
from datetime import timedelta as td

from generate_ical_file import all_dates_list, bhs_calendar, current_yr, timetable_dict
from import_fun_and_stats import get_list_of_unique_lessons
from new_schedule_times import timetable_path_n_file



def add_lesson_to_wld(lesson_attribute, weekly_lesson_dictionary):
    '''
    add lesson to weekly lesson dictionary
    increments counter of lessons if the lesson is in the dictionary
    or creates a new entry to count this lesson
    '''
    lesson = lesson_attribute.split('@')[0].rstrip()
    # removes the location: 'Y11 Phys @PL' --> 'Y11 Phys'

    if (lesson in weekly_lesson_dictionary) and (len(lesson) > 1):
        weekly_lesson_dictionary[lesson] += 1
    elif len(lesson) > 1:  # don't count empy lesson
        weekly_lesson_dictionary[lesson] = 1

    return None

def total_weekly_lessons(weekly_lesson_dictionary):
    ''' returns an integer
        which is the total number of lessons that week.
        typically 15 - 20
    '''
    return sum(weekly_lesson_dictionary.values())

def when_is_this_lesson(year_lesson_substring, day_data):
    '''
    `input`:
    - string like 'Y8', 'Y8A', 'Y10C', 'IB1' or 'Y10'
    - day_data, an item from cal_list= sorted(bhs_calendar.items())
    `outpt`: Lesson number when it's taught or False
    '''
    clean_lessons_that_day = [x.split(' ')[0].rstrip() for x in day_data.all_lessons]
    clean_lessons_that_day = day_data.all_lessons
    is_lesson_taught = [L for L in clean_lessons_that_day
                        if year_lesson_substring in L]
    if len(is_lesson_taught) == 0:
        return False
    else:
        indx = [i+1 for i, L in enumerate(day_data.all_lessons)
                if year_lesson_substring in L][0]
        lesson = is_lesson_taught[0]
        return indx, lesson


# def generate_weekly_calendar(full_calendar, monday, friday):
#     this_week = []
#     for x in full_calendar:
#         if (x[0] >= monday) and (x[0] <= friday):
#             this_week.append(x)
#     return this_week

# def what_week_are_we(someday=None):
#   '''
#   When today() is called, it returns the date of Monday
#   this week and the day of Friday this week.
#   Output: datetime of Monday, datetime of Friday
#   '''
#   if someday:
#     weekday_today = someday.weekday()
#     monday = someday - td((weekday_today), 0, 0)
#     friday = monday+  td(4,0,0)
#     return monday, friday
#   else:
#     weekday_today = dt.today().weekday()
#     monday = dt.today() - td((weekday_today), 0, 0)
#     friday = monday + td(4,0,0)
#     return monday, friday



cal_list = sorted(bhs_calendar.items()) # calendar list


##########################################
#  Make dict with the weeks of the year  #
##########################################

weeks_dict = {0: (dt(2019, 8, 26), dt(2019, 8, 30))}
week_counter = 1
for i in cal_list:
    if i[0] > 1:
        # skip the first week (as it's already item zero above)
        if i[1].date.weekday() == 0:
            monday = i[1].date
        elif i[1].date.weekday() == 4:
            friday = i[1].date
            weeks_dict[week_counter] = (monday, friday)
            week_counter += 1

print( "There are %s weeks in the %s-%s year" % \
      (len(weeks_dict), current_yr, current_yr+1))



#############################################################
# Make list with a dict of how many lessons of each class   #
#                     are given each week                   #
#############################################################
# Example, weekly_lesson_dictionary[1] =
# [datetime.datetime(2018, 9, 3, 0, 0),
# {'Y10BC Phy 2': 2, 'Y8B Sc': 2,
#  'Y11 Phy': 2, 'Y10A Phy 1': 1,
# 'IB1': 2, 'IB2': 2}
# ]

weekly_lesson_configurations = []
for i in range(len(weeks_dict)):  # loop over all weeks
    monday = weeks_dict[i][0]
    friday = weeks_dict[i][1]

    wld = {}  # weekly lesson dictionary
    for x in cal_list:

        if (x[1].date >= monday) and (x[1].date <= friday) \
            and (not x[1].half_day) and (not x[1].special_day):
            add_lesson_to_wld(x[1].L1, wld)
            add_lesson_to_wld(x[1].L2, wld)
            add_lesson_to_wld(x[1].L3, wld)
            add_lesson_to_wld(x[1].L4, wld)
            add_lesson_to_wld(x[1].L5, wld)
    weekly_lesson_configurations.append([monday, wld])




    #############################################
    # Create an empty list of weeks and lessons #
    #############################################
all_weeks = sorted(weeks_dict.items())
cal_list = sorted(bhs_calendar.items()) # calendar list

# the unwieldy animal of dict of dicts with lists of lists:
full_schedule_by_year = {}
list_unique_classes = get_list_of_unique_lessons(timetable_dict)
clean_list_u_classes = [x.split('@')[0].rstrip() for x in list_unique_classes]

# dict structure to fill with lesson info:
# get_list_of_unique_lessons(timetable_path_n_file)
# ->  ['Y10BC Phy 2', 'Y8B Sc', 'Y11 Phy', 'Y10A Phy 1', 'IB1', 'IB2']
how_many_different_classes = \
len(list_unique_classes)


print( clean_list_u_classes, how_many_different_classes )


empty_lessons_dict = {}
for i in range(how_many_different_classes):
    empty_lessons_dict[int(i)] = []


# empty_lessons_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

xxx =   {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

for aweek in all_weeks:
  # Create a list of tuples with (Monday, empty dict of lesson)
  # For example, on the second week, the third item of the list is:
  # (datetime.datetime(2018, 9, 10, 0, 0),
  #  {0: [], 1: [], 2: [], 3: [], 4: [], 5: []})
  # The actual lessons will be filled in in the next loop

  full_schedule_by_year[aweek[1][0]] = \
  {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []} # for skelly
  # {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
  # {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
  # empty_lessons_dict
  # A REALLY WEIRD BUG IS HIDING HERE!
  # if I hand code the dict as above it works
  # if I use empty_lessons_dict it breaks:
  # add many more dates inside each week??


#-------------------------------

for aweek in sorted(full_schedule_by_year):
    monday = aweek
    friday = aweek + td(days=4)

    # which days from the full list of teaching days
    # are inside of this week?
    dates_in_week = [x[1] for x in cal_list if \
                    (x[1].date >= monday and x[1].date <= friday)]
    # x[1] selects the newcal.SchoolDay object from the tuple


    # strategy:
    # 1. get list of classes (Y8, Y10B, etc)
    #    list_unique_classes
    # 2. create an entry for each


    for adate in dates_in_week:
        for class_index, a_class in enumerate(clean_list_u_classes):
            # assumption: a given lesson only happens once a day
            whe = when_is_this_lesson(a_class, adate)
            if whe:
                full_schedule_by_year[monday][class_index].append(\
                                             [adate.date, whe[0], whe[1]])

#-----------------------


# for x in full_schedule_by_year[dt(2018,9,10)][0]:
#     print x

# for x in full_schedule_by_year[dt(2018,9,10)][1]:
#     print x


# --> Now use this full_schedule_by_year object to make the layout
# and use the usual cal_list to make the calendar on the right page

## full_schedule_by_year produces tuple items in a dict of the form:
# THE WEEK: (datetime.datetime(2018, 9, 3, 0, 0),
# THE LESSONS ASSOCIATED:
# {
# Y8 lessons -> 0: [[datetime.datetime(2018, 9, 5, 0, 0), 3, 'Y8B Sc @PL'],
# [datetime.datetime(2018, 9, 7, 0, 0), 4, 'Y8B Sc @PL']],
# Y10 lessons -> 1: [[datetime.datetime(2018, 9, 6, 0, 0), 1, 'Y10A Phy 1
# @PL'], [datetime.datetime(2018, 9, 7, 0, 0), 3, 'Y10BC Phy 2 @PL']],
# 2: [], 3: [], 4: [[datetime.datetime
# (2018, 9, 6, 0, 0), 4, 'IB1 @3'], [datetime.datetime(2018, 9, 7, 0, 0), 2, 'IB1 @PL']], 5: [[datetime.date
# time(2018, 9, 5, 0, 0), 4, 'IB2 @26'], [datetime.datetime(2018, 9, 6, 0, 0), 3, 'IB2 @8']]})
