#!/usr/bin/env python
# Class Based implementation of the BHS calendar
from datetime import datetime as dt
from datetime import timedelta as td
import csv, re

from icalendar import Calendar, Event

# What period is at what time? eg. period 1 from 8:40 - 9:45
from new_schedule_times import reg, l1, l2, l3, l4, l5, lunch, \
                               plus_a_registration, plus_a_lunch, \
                               plus_an_hour, plus_half_an_hour, \
                               plus_a_lesson, plus_half_a_day, \
                               plus_a_working_day, timetable_path_n_file




def add_half_a_day(ical, a_day):
    ''' Create icalendar entry for half a day
    '''
    day_data = a_day[1]
    event = Event()
    event.add('summary', 'Half Day')
    event['location'] = 'BHS'
    event.add('dtstart', day_data.date + reg)
    event.add('dtend', day_data.date + reg + plus_half_a_day)
    event['uid'] = 'Half' + str(a_day[0]) + str(day_data.date).replace(" ","-")
    ical.add_component(event)
    return ical

def add_special_day(ical, a_day):
    ''' Create icalendar entry for half a day
    '''
    day_data = a_day[1]
    event = Event()
    event.add('summary', day_data.special_day)
    event['location'] = 'BHS'
    event.add('dtstart', day_data.date + reg)
    event.add('dtend', day_data.date + reg + plus_a_working_day)
    event['uid'] = 'Special' + str(a_day[0]) + \
                   str(day_data.date).replace(" ", "-") + day_data.special_day
    ical.add_component(event)
    return ical

def add_PD_day(ical, a_day):
    ''' Create icalendar entry for half a day
    '''
    day_data = a_day[1]
    event = Event()
    event.add('summary', 'Professional Development')
    event['location'] = 'BHS'
    event.add('dtstart', day_data.date + l1)
    event.add('dtend', day_data.date + l1 + plus_a_working_day)
    event['uid'] = 'PD' + str(a_day[0]) + str(day_data.date).replace(" ", "-")
    ical.add_component(event)
    return ical


def add_statistics_string(day_data, timetable_dict):
    all_classes = get_list_of_unique_lessons(timetable_dict)
    dd = day_data

    full_string = 'These are the lessons you will \
teach minus half-days, study leave, sports/art/steam days and most exams: \n\n'

    for class_name in all_classes:
        sub_string = '_' + class_name + '_' + ' :   %s taught     ||     %s left \n' % \
        (day_data.stats[class_name+'-done'], day_data.stats[class_name+'-left'])
        full_string = full_string + sub_string


    teaching_days ='\n %d days of teaching left, %d days of teaching done \n ' % \
                    (dd.stats['days_left_teaching'], dd.stats['days_taught'])
    just_days = "%d days left 'til the summer! \n\n" % \
                    dd.stats['days_to_summer']

    disclaimer = '''DISCLAIMER: You will have fewer lessons than
                    indicated due to the usual suspects:
                    Torch Day, Days out, trips, Y7 endeavour, etc.'''
    full_string = full_string + teaching_days + just_days + disclaimer

    return full_string

def short_statistics(day_data, timetable_dict):
    '''
    A quick overview of statistics.
    Called by PDF generator sandbox.py
    '''
    all_classes = get_list_of_unique_lessons(timetable_dict)
    dd = day_data
    list_of_short_stats = []
    for class_name in all_classes:
        # if len(class_name.split(' ')) > 2:
        #     # if it is of the form 'Y11 Phy 6'
        #     sub_string = class_name.split(' ')[0] + \
        #     ' : %s / %s' %  \
        #    (day_data.stats[class_name+'-done'], day_data.stats[class_name+'-left'])
        # else:
        # if it is of the form 'IB1'
        sub_string = class_name.split(' ')[0]+ \
            ' : %s / %s' % \
        (day_data.stats[class_name+'-done'], day_data.stats[class_name+'-left'])
        list_of_short_stats.append(sub_string)

    return list_of_short_stats


def add_teaching_day(ical, a_day, timetable_dict):
    ''' Create icalendar entry for a normal day
    '''
    day_data = a_day[1]
    day_nr_event = Event()
    day_nr_event.add('summary', 'Week %s - Nr %s' % (day_data.week, day_data.week_nr))


    stats_string = add_statistics_string(day_data, timetable_dict)
    day_nr_event.add('description', stats_string)


    day_nr_event['location'] = 'BHS'
    day_nr_event.add('dtstart', day_data.date + reg - plus_an_hour)
    day_nr_event.add('dtend', day_data.date + reg - plus_half_an_hour)
    day_nr_event['uid'] = 'dayNR' + str(a_day[0]) + \
                          str(day_data.date).replace(" ", "-")
    ical.add_component(day_nr_event)

    if day_data.L1:  # maybe all lessons should have been refactored to a dict.
        l1_event = Event()
        l1_event.add('summary', day_data.L1)
        l1_event['location'] = day_data.L1.split('@')[1]
        l1_event.add('dtstart', day_data.date + l1)
        l1_event.add('dtend', day_data.date + l1 + plus_a_lesson)
        l1_event['uid'] = 'L1' + str(a_day[0]) + \
                          str(day_data.date).replace(" ", "-")
        ical.add_component(l1_event)

    if day_data.L2:  # maybe all lessons should have been refactored to a dict.
        l2_event = Event()
        l2_event.add('summary', day_data.L2)
        l2_event['location'] = day_data.L2.split('@')[1]
        l2_event.add('dtstart', day_data.date + l2)
        l2_event.add('dtend', day_data.date + l2 + plus_a_lesson)
        l2_event['uid'] = 'L2' + str(a_day[0]) + \
                          str(day_data.date).replace(" ", "-")
        ical.add_component(l2_event)

    if day_data.L3:  # maybe all lessons should have been refactored to a dict.
        l3_event = Event()
        l3_event.add('summary', day_data.L3)
        l3_event['location'] = day_data.L3.split('@')[1]
        l3_event.add('dtstart', day_data.date + l3)
        l3_event.add('dtend', day_data.date + l3 + plus_a_lesson)
        l3_event['uid'] = 'L3' + str(a_day[0]) + \
                          str(day_data.date).replace(" ", "-")
        ical.add_component(l3_event)

    if day_data.L4:  # maybe all lessons should have been refactored to a dict.
        l4_event = Event()
        l4_event.add('summary', day_data.L4)
        l4_event['location'] = day_data.L4.split('@')[1]
        l4_event.add('dtstart', day_data.date + l4)
        l4_event.add('dtend', day_data.date + l4 + plus_a_lesson)
        l4_event['uid'] = 'L4' + str(a_day[0]) + \
                          str(day_data.date).replace(" ", "-")
        ical.add_component(l4_event)

    if day_data.L5:  # maybe all lessons should have been refactored to a dict.
        l5_event = Event()
        l5_event.add('summary', day_data.L5)
        l5_event['location'] = day_data.L5.split('@')[1]
        l5_event.add('dtstart', day_data.date + l5)
        l5_event.add('dtend', day_data.date + l5 + plus_a_lesson)
        l5_event['uid'] = 'L5' + str(a_day[0]) + \
                          str(day_data.date).replace(" ", "-")
        ical.add_component(l5_event)

    if day_data.meeting:
        meeting_event = Event()
        meeting_event.add('summary', day_data.meeting + ' meeting')
        meeting_event['location'] = 'Department/QEH'
        meeting_event.add('dtstart', day_data.date + l5 + plus_a_lesson +
                          plus_a_registration)
        meeting_event.add('dtend', day_data.date + l5 + plus_a_lesson +
                          plus_a_registration + plus_an_hour)
        meeting_event['uid'] = day_data.meeting + str(a_day[0]) + \
                               str(day_data.date).replace(" ", "-")
        ical.add_component(meeting_event)

    leaves = [day_data.y7_leave, day_data.y8_leave, day_data.y9_leave,
              day_data.y10_leave, day_data.y11_leave,
              day_data.ib1_leave, day_data.ib2_leave]
    leave_index = [i for i, x in enumerate(leaves) if x]
    # This may need upgrading for other calendars
    # 'Y789' has changed to 'Y7_leave', 'Y8_leave', 'Y9_leave'
    # 0.5 in leave column means away for the morning.
    leave_dict = {0: 'Y7 leave', 1: 'Y8 leave', 2: 'Y9 leave',
                  3: 'Y10 leave', 4: 'Y11 leave', 5: 'IB1 leave', 6: 'IB2 leave'}
    leave_string = '| '.join([leave_dict[i] for i in leave_index])

    if leave_string:
        leave_note = Event()
        leave_note.add('summary', leave_string)
        leave_note.add('description', leave_string)
        leave_note.add('dtstart', day_data.date + td(hours=6, minutes=20))
        leave_note.add('dtend', day_data.date + td(hours=6, minutes=0) +
                       plus_a_lunch)
        leave_note['uid'] = 'leaveInfo' + str(a_day[0]) + \
                            str(day_data.date).replace(" ", "-")
        ical.add_component(leave_note)


    return ical


def count_teaching_days(bhs_calendar):
    ''' goes through the dictionary containing
        the objects for each date
        and checks if it's a teaching day
        incrementing the counter
    '''
    bhs_calendar_days_list = sorted(bhs_calendar.items())
    counter = 0

    for a_day in bhs_calendar_days_list:
        day_data = a_day[1]
        if day_data.teaching_day:
            counter += 1

    return counter


def count_lesson_days(bhs_calendar, lesson_string,
                      adate=dt(2018, 8, 30), opt='left'):
    ''' goes through the dictionary containing
        the objects for each date
        and checks if there is a particular lesson that day
        incrementing the counter. For ex:
        Check for string 'IB2', discarding those days IB2s are on leave.
        (start on a given date, fwd or backwards)
        opt: can be left or done (days left or days already done)
    '''

    bhs_calendar_days_list = sorted(bhs_calendar.items())
    counter = 0


    for a_day in bhs_calendar_days_list:
        day_data = a_day[1]
        leaves = [day_data.y7_leave, day_data.y8_leave, day_data.y9_leave,
              day_data.y10_leave, day_data.y11_leave,
              day_data.ib1_leave, day_data.ib2_leave]

        leave_index = [i for i, x in enumerate(leaves) if x]
        # 0.5 in leave column means away for the morning.
        leave_dict = {0: 'Y7 leave', 1: 'Y8 leave', 2: 'Y9 leave',
                  3: 'Y10 leave', 4: 'Y11 leave', 5: 'IB1 leave', 6: 'IB2 leave'}

        lesson_list = [day_data.L1, day_data.L2, day_data.L3, day_data.L4, day_data.L5]


        if day_data.teaching_day:
            is_that_lesson_today = len([s for s in lesson_list if lesson_string in s])
            if is_that_lesson_today > 0:
                # which classes are on leave?
                are_on_leave = [leave_dict[ind] for ind in leave_index]
                # we use short_lesson_string to find 'Y11' instead of 'Y11 Phy 6' or 'Y11 Phy 1'
                short_lesson_string = lesson_string.split(' ')[0]
                is_that_lesson_on_leave = len([s for s in are_on_leave
                                                if short_lesson_string in s])
                if is_that_lesson_on_leave > 0:
                    pass
                else:
                    if opt == 'left' and day_data.date > adate:
                        counter += 1
                    if opt == 'left' and day_data.date < adate:
                        pass
                    if opt == 'done' and day_data.date > adate:
                        pass
                    if opt == 'done' and day_data.date < adate:
                        counter += 1
    # if opt == 'left':
    #     print 'there are %s lessons left of %s'  % (counter, lesson_string)
    # if opt == 'done':
    #     print 'You have already taught %s lessons of %s'  % (counter, lesson_string)
    return counter



def get_list_of_unique_lessons(timetable_dict):
    '''
    `input`: timetable_dict
    `output`: unique lessons, for ex:
    ['IB1 Phys', 'IB2 D.tech', 'Y10 Phys 1', 'Lunch Duties',
    'Y11 Phys 2', 'Y11 Phys 1', '9A Sc', 'IB2 Reg.']
    '''

    all_lessons = []

    for i in timetable_dict:
        all_lessons += timetable_dict[i]

    # regex = re.compile(ur'\@[\w\-]*', re.DOTALL)
    # lessons_without_location = [regex.sub('', lesson).strip() for lesson in all_lessons]
    lessons_without_location = [lesson.split(' @')[0].strip() for lesson in all_lessons]
    unique_lessons = list(set(lessons_without_location))
    # remove empty lessons:
    unique_lessons = [x for x in unique_lessons if x]
    # Sort them before returning them:
    sorted_unique_lessons = []
    all_class_strings = ['7', '8', '9', '10', '11', 'IB1', '12', 'IB2', '13']
    for sub_str in all_class_strings:
        matching = [s for s in unique_lessons if sub_str in s]
        if matching:
            for match in matching:
                sorted_unique_lessons.append(match)

    return sorted_unique_lessons


'''
You have 11 days of teaching left (excluding half days, holidays, PD days)
and have taught 162 days so far
IB2 Phys: 59 LESSONS TAUGHT | 0 LESSONS LEFT
Y11-1: 62 LESSONS TAUGHT | 0 LESSONS LEFT
Y10-1: 50 LESSONS TAUGHT | 4 LESSONS LEFT
Y9 Sc: 104 LESSONS TAUGHT | 8 LESSONS LEFT
Y10-6: 76 LESSONS TAUGHT | 6 LESSONS LEFT
IB1 Phys: 76 LESSONS TAUGHT | 6 LESSONS LEFT
Y10C Reg.: 151 LESSONS TAUGHT | 12 LESSONS LEFT

{'Y11 Phy 6': 82, 'Y8A Sc': 111, 'Y11 Phy 1': 84, 'IB1': 125, 'IB2': 56, 'Y10 Phy 1': 55} # # #




This excludes study leave and exams.
DISCLAIMER: You may have fewer lessons than indicated
here due to the usual suspects: Torch Day, Days out, trips, etc.
'''
