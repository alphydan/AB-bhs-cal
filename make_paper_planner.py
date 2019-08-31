from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch,cm
from reportlab.platypus import Image, Paragraph

from datetime import timedelta as td

from paper_planner_functions import total_weekly_lessons, \
                          weekly_lesson_configurations, \
                          weeks_dict,full_schedule_by_year, \
                          cal_list, all_weeks, \
                          how_many_different_classes, clean_list_u_classes, \
                          timetable_dict

from import_fun_and_stats import short_statistics



# Strategy:

###########################################################################
# 1. Count how many periods are in the week (eg. 15)                      #
# 2. Make dict of periods for each class                                  #
#    eg. {'Y8': 3, 'Y10BC': 2, 'Y10A': 1, 'Y11': 2 , 'IB1': 4, 'IB2': 3 } #
# 3. Find optimal box arrangement, but always in same order. !!           #
#    Typically up to 20 periods in a week (10 / 10)                       #
#    But could be 7 / 7 or similar.                                       #
#    For me the question is: Does Y11 stay left or right?                 #
# 4. Draw boxes                                                           #
###########################################################################



# BHS & Date Header
def create_header(c, aweek, size="Large"):
    # c.drawImage('../img/bhs_CMYK.tif', width-2.1*inch, height - 0.85 * inch, 89,30)

    # for skelly
    c.drawImage('../bhs-ical/img/bhs_CMYK.tif', width-2.1*inch, height - 0.67 * inch, 89,30)

    # canvas.drawImage(self, image, x,y, width=None,height=None,mask=None)
    if size == "Large":
        c.setFont("Helvetica", 20)
        c.drawString(width/2-3*cm, height-0.8*inch, aweek)
    if size == "Small":
        c.setFont("Helvetica", 12)
        c.drawString(left_margin+0.7*cm, height-0.8*inch, aweek)

# Draw margins:
def draw_margins(c):
    '''Draws Margins for printing
    '''
    c.line(left_margin, 0, left_margin, height)  # left_margin
    c.line(0, bottom_margin, width, bottom_margin)  # bottom
    c.line(width-right_margin, 0, width-right_margin, height)  # right
    c.line(0, height-top_margin, width, height-top_margin)  # top


    c.setStrokeColorRGB(1, 0.1, 0.1)  # red
    c.line(0.88*inch, 0, 0.88*inch, height)  # left_margin
    c.line(0, 0.31*inch, width, 0.31*inch)  # bottom
    c.line(width-0.88*inch, 0, width-0.88*inch, height)  # right
    c.line(0, height-0.31*inch, width, height-0.31*inch)  # top


#################
# Lesson Boxes  #
#################
def create_columns(lessons, side='L'):

        '''
        Creates boxes for Y8, Y10, Y11(1), Y11(6) (left)
        or for IB1, IB2, Lab requisitions (right)
        side can be 'L' or 'R'
        '''
        c.setLineWidth(2)
        c.setStrokeColorRGB(0.4, 0.4, 0.4)

        height_for_boxes = height-top_margin-bottom_margin
        c.setFont("Helvetica", 12)

        # lesson_title = {'L': clean_list_u_classes[:4],
        #                 'R': clean_list_u_classes[4:]}

        # for skelly 7 classes
        lesson_title = {'L': clean_list_u_classes[:5],
                        'R': clean_list_u_classes[5:]}


        # for lneame 7 classes
        lesson_title = {'L': clean_list_u_classes[:4],
                        'R': clean_list_u_classes[4:]}

        # for ncook with 3L / 2R classes
        # lesson_title = {'L': [clean_list_u_classes[0], clean_list_u_classes[1],
        #                       clean_list_u_classes[3]],
        #                 'R': [clean_list_u_classes[2], clean_list_u_classes[4]]}


        if sum(lessons) == 0:
            pass
        else:
            bx_height_unit = height_for_boxes/sum(lessons)
            box_width = (width-left_margin-right_margin)/2
            round_corner = 8

            for i, x in enumerate(lessons):
                height_of_box = bx_height_unit*x
                position_of_box = bx_height_unit*sum(lessons[0:(i+1)])
                if side == 'L':
                    box_left_margin = left_margin
                    text_left_margin = left_margin+box_width-1.4*cm
                    text_left_margin = left_margin+box_width-2*cm
                else:
                    box_left_margin = left_margin + box_width
                    text_left_margin = width - right_margin - 1*cm
                c.roundRect(box_left_margin, height-top_margin-position_of_box,
                            box_width, height_of_box, round_corner)
                if x != 0: # there are lessons
                        c.drawString(text_left_margin-0.4*cm,
                                     height-top_margin-position_of_box+
                                     height_of_box-0.5*cm, lesson_title[side][i])


###################################
### Calendar Boxes (RIGHT page) ###
###################################

def draw_calendar_boxes():
    '''
    Draw the structure in which we will place the lesson
    information
    '''
    c.setFont("Helvetica", 12)
    date_margin = 0.9*cm
    box_height = (height-top_margin-bottom_margin)/5
    box_width = width-left_margin-right_margin-date_margin
    for i in range(0, 5):
        c.setStrokeColorRGB(0.1*i, 0.1*i, 0.1*i) # blue
        c.roundRect(left_margin+date_margin-1.5*cm,
                    bottom_margin+box_height*i, box_width, box_height, 8)

    for i in range(1, 5):
        c.line(left_margin+i*box_width/5+date_margin-1.5*cm, bottom_margin, left_margin +
               i*box_width/5+date_margin-1.5*cm, height-top_margin) # bottom

    week_day = {0: 'M', 1: 'T', 2: 'W', 3: 'Th', 4: 'Fr'}
    for key, value in week_day.items():
        c.drawString(left_margin-1.2*cm,
                 height-top_margin-box_height*key-box_height/2,
                 value)



def place_lesson_strings_on_L_canvas(canvas, monday, year_group_index,
                                     lessons_L, box_unit_height_L):
    '''
    calculates the position where strings should be placed for different
    year groups
    `year_group_index`: 0: Y8, 1: Y10, 2: Y11, 3: Y11(6)
    '''
    year_group_lessons = full_schedule_by_year[monday][year_group_index]
    for i, group_l in enumerate(year_group_lessons):
        date_string = group_l[0].strftime("%a %d")
        room_string = group_l[2].split('@')[1]
        canvas.drawString(left_margin+0.1*cm, #0.1
                          height-top_margin - 0.5*cm -
                          box_unit_height_L * \
                          (i+sum(lessons_L[0:year_group_index])),
                          date_string+' @'+room_string)

        # for ncook who has class group Y10 <-> Y9 reversal
        # if year_group_index == 3:
        #     canvas.drawString(left_margin+0.1*cm, #0.1
        #                   height-top_margin - 0.5*cm -
        #                   box_unit_height_L * \
        #                   (i+sum(lessons_L[0:year_group_index-1])),
        #                   date_string+' @'+room_string)
        # else:
        #     canvas.drawString(left_margin+0.1*cm, #0.1
        #                   height-top_margin - 0.5*cm -
        #                   box_unit_height_L * \
        #                   (i+sum(lessons_L[0:year_group_index])),
        #                   date_string+' @'+room_string)



def place_lesson_strings_on_R_canvas(canvas, monday, year_group_index,
                                     lessons_R, box_unit_height_R):
    '''
    calculates the position where strings should be placed for different
    year groups
    `year_group_index`: 4: IB1, 5: IB2
    '''
    year_group_lessons = full_schedule_by_year[monday][year_group_index]
    for i, group_l in enumerate(year_group_lessons):
        date_string = group_l[0].strftime("%a %d")
        room_string = group_l[2].split('@')[1]
        # IB1 & IB2
        # canvas.drawString(width/2+0.35*cm, # 0.2 for normal margin
        #                   height-top_margin - 0.5*cm -
        #                   box_unit_height_R * \
        #                   (i+sum(lessons_R[:year_group_index-4])),
        #                   date_string+' @'+room_string)
        # for skelly who has 7 different lessons
        canvas.drawString(width/2+0.4*cm, # 0.2 for normal margin
                          height-top_margin - 0.5*cm -
                          box_unit_height_R * \
                          (i+sum(lessons_R[:year_group_index-4])), #neame: index-4, kelly: index-5?
                          date_string+' @'+room_string)

        # for ncook who has 5 different lessons
        # and a swap of groups 2 and 3 with L/R
        # if year_group_index == 2:
        #     canvas.drawString(width/2+0.35*cm, # 0.2 for normal margin
        #                   height-top_margin - 0.5*cm -
        #                   box_unit_height_R * \
        #                   (i+sum(lessons_R[:year_group_index-2])),
        #                   date_string+' @'+room_string)
        # else:
        #     canvas.drawString(width/2+0.35*cm, # 0.2 for normal margin
        #                 height-top_margin - 0.5*cm -
        #                   box_unit_height_R * \
        #                   (i+sum(lessons_R[:year_group_index-3])),
        #                   date_string+' @'+room_string)


def add_lesson_details(canvas, full_schedule_by_year, all_weeks):
    ''' Add lesson details (date, where, which lesson) to the canvas
        input: crazy dict of dicts with lists of lists (see paper_planner_functions.py)
               (full_schedule_by_year)
        output: None (writing to canvas)
    '''
    for aweek in all_weeks:


        ###############################
        #    Common Definitions

        monday = aweek[1][0]
        friday = aweek[1][0] + td(days=4)
        week_dates_string = "%s - %s" % (monday.strftime("%d %b"), \
                                        friday.strftime("%d %b"))


        ##### THIS SECTION IS JUST INFO GATHERING  ####
        lessons_this_week = 0
        for class_index in range(how_many_different_classes):
            lessons_this_week += len(full_schedule_by_year[monday][class_index])

        lessons_first_3 = 0
        for class_index in range(3):
            lessons_first_3 += len(full_schedule_by_year[monday][class_index])

        lessons_first_4 = 0
        for class_index in range(4):
            lessons_first_4 += len(full_schedule_by_year[monday][class_index])

        lessons_first_5 = 0
        for class_index in range(5):
            lessons_first_5 += len(full_schedule_by_year[monday][class_index])

        # print '---------------->', lessons_this_week
        # print 'first 3: ', lessons_first_3
        # print 'first 4: ',  lessons_first_4
        # print 'first 5: ', lessons_first_5, '--->>>', (lessons_this_week/2, lessons_first_5)

        # print 'diff to 3 ', lessons_this_week/2.0 - lessons_first_3
        # print 'diff to 4', lessons_this_week/2.0 - lessons_first_4
        # print 'diff to 5', lessons_this_week/2.0 - lessons_first_4
        # print '\n'

        #####  INFO GATHERING END  ####


        # for aFeito - 6 class groups
        # lessons_L = [len(full_schedule_by_year[monday][0]),
        #              len(full_schedule_by_year[monday][1]),
        #              len(full_schedule_by_year[monday][2]),
        #              len(full_schedule_by_year[monday][3])]
        # lessons_R = [len(full_schedule_by_year[monday][4]),
        #              len(full_schedule_by_year[monday][5])]



        # for ncook - 5 class groups
        # lessons_L = [len(full_schedule_by_year[monday][0]),
        #              len(full_schedule_by_year[monday][1]),
        #              len(full_schedule_by_year[monday][3])]
        # lessons_R = [len(full_schedule_by_year[monday][2]),
        #              len(full_schedule_by_year[monday][4])]


        # for Skelly - 7 class groups
        # lessons_L = [len(full_schedule_by_year[monday][0]),
        #              len(full_schedule_by_year[monday][1]),
        #              len(full_schedule_by_year[monday][2]),
        #              len(full_schedule_by_year[monday][3]),
        #              len(full_schedule_by_year[monday][4])]
        # lessons_R = [len(full_schedule_by_year[monday][5]),
        #              len(full_schedule_by_year[monday][6])]


        # for neame - 7 class groups
        lessons_L = [len(full_schedule_by_year[monday][0]),
                     len(full_schedule_by_year[monday][1]),
                     len(full_schedule_by_year[monday][2]),
                     len(full_schedule_by_year[monday][3]),]
        lessons_R = [len(full_schedule_by_year[monday][4]),
                     len(full_schedule_by_year[monday][5]),
                     len(full_schedule_by_year[monday][6])]



        # How many left-column lessons this week? Y8, Y10, Y11(1), Y11(6)
        nr_L_column_lessons = sum(lessons_L)
        nr_R_column_lessons = sum(lessons_R)


        ###############################
        #    FIRST PAGE (Calendar)

        create_header(canvas, week_dates_string, size="Small")
        draw_calendar_boxes()
        box_unit_width = (width-right_margin-left_margin)/5
        box_unit_height = (height-top_margin-bottom_margin)/5
        c.setFont("Helvetica", 10)
        for aday in cal_list:
            if aday[1].date == monday:
                if len(aday[1].all_lessons) > 0:

                    # Extra info: Statistics
                    if len(aday[1].stats) > 0:
                        short_stats = short_statistics(aday[1], timetable_dict)
                        for i, ss in enumerate(short_stats):
                            if i < 3:
                                c.drawString(left_margin+1.75*inch+i*3*cm,
                                         height-1.5*cm, ss )
                            else:
                                c.drawString(left_margin+1.75*inch+(i-3)*3*cm,
                                         height-2*cm, ss )

            # lessons in each box of the weekly calendar
            for add_day in range(0, 5):
                if aday[1].date == (monday+td(days=add_day)):
                    if len(aday[1].all_lessons) > 0:

                        # make list of all on leave that day
                        leave = [aday[1].y7_leave, aday[1].y8_leave,
                                 aday[1].y9_leave, aday[1].y10_leave,
                                 aday[1].y11_leave, aday[1].ib1_leave,
                                 aday[1].ib2_leave]

                        list_of_classes = ['Y7', 'Y8', 'Y9', 'Y10', 'Y11', 'IB1', 'IB2']
                        leave_or_not_list = zip(list_of_classes, leave)

                        # print the lessons in each day of the calendar
                        for i, le in enumerate(aday[1].all_lessons):
                            c.drawString(left_margin-0.3*cm+box_unit_width*(i-1)*0.94, #0.93
                                         height-top_margin-0.5*cm -
                                         box_unit_height*add_day,
                                         le)

                            # return a tuple if this particular class
                            # which has lesson "le" happens to be on leave
                            le_on_leave = [(x,y) for x,y in leave_or_not_list \
                             if (x in le and y == True)]

                            if len(le_on_leave) > 0:
                                # print 'some on leave: ', le_on_leave, le
                                c.setFont("Helvetica-Bold", 9)
                                c.drawString(left_margin-0.3*cm+box_unit_width*i*0.93,
                                         height-top_margin-0.85*cm -
                                         box_unit_height*add_day,
                                                 'ON LEAVE')
                                c.setFont("Helvetica", 10)

                            c.drawString(left_margin-1.2*cm,
                            height-top_margin-0.5*cm-box_unit_height*(add_day+0.5),
                                aday[1].date.strftime("%d"))



                        # day of the month left of the boxes:
                    else:
                        c.drawString(left_margin-1.2*cm,
                            height-top_margin-0.5*cm-box_unit_height*(add_day+0.5),
                                aday[1].date.strftime("%d"))

                            # day number left of the boxes:
                            # c.drawString(left_margin-1.1*cm,
                            #     height-top_margin-0.5*cm-box_unit_height*(add_day+0.5)+2.1*cm,
                            #     str(aday[1].day_number))
                            # c.circle(left_margin-1*cm,
                            #          height-top_margin-0.5*cm-box_unit_height*(add_day+0.5)+2.23*cm,
                            #          0.25*cm, stroke=1, fill=0)


        c.showPage() # finish page and move to next one

        ###############################
        #    SECOND PAGE (Planning)


        create_header(canvas, week_dates_string)
        # add week number and letter
        tuesday = monday + td(days=1)
        for aday in cal_list:
            if aday[1].date == tuesday and aday[1].week and aday[1].week_nr:
                c.drawString(left_margin+0.4*cm, height-top_margin+0.5*cm, 'Week-' \
                             + aday[1].week + " #" + aday[1].week_nr)




        if nr_L_column_lessons > 0:
            box_unit_height_L = (height-top_margin-bottom_margin)/ \
                                 nr_L_column_lessons
            c.setFont("Helvetica", 12)

            place_lesson_strings_on_L_canvas(c, monday, 0,
                                             lessons_L, box_unit_height_L)
            place_lesson_strings_on_L_canvas(c, monday, 1,
                                             lessons_L, box_unit_height_L)
            place_lesson_strings_on_L_canvas(c, monday, 2,
                                             lessons_L, box_unit_height_L)
            place_lesson_strings_on_L_canvas(c, monday, 3,
                                             lessons_L, box_unit_height_L)

            # for skelly which has 5 lessons to the left
            # place_lesson_strings_on_L_canvas(c, monday, 4,
            #                                  lessons_L, box_unit_height_L)

            # for ncook place Y10 L, Y9 R
            # place_lesson_strings_on_L_canvas(c, monday, 0,
            #                                  lessons_L, box_unit_height_L)
            # place_lesson_strings_on_L_canvas(c, monday, 1,
            #                                  lessons_L, box_unit_height_L)
            # place_lesson_strings_on_L_canvas(c, monday, 3,
            #                                  lessons_L, box_unit_height_L)


            create_columns(lessons_L, 'L')
            create_columns(lessons_R, 'R')

        if nr_R_column_lessons > 0:
            box_unit_height_R = (height-top_margin-bottom_margin)/nr_R_column_lessons

            place_lesson_strings_on_R_canvas(c, monday, 4,
                                              lessons_R, box_unit_height_R)
            place_lesson_strings_on_R_canvas(c, monday, 5,
                                              lessons_R, box_unit_height_R)

            # for ncook who has many in column L
            # place_lesson_strings_on_R_canvas(c, monday, 2,
            #                                  lessons_R, box_unit_height_R)
            # place_lesson_strings_on_R_canvas(c, monday, 4,
            #                                   lessons_R, box_unit_height_R)
            # place_lesson_strings_on_R_canvas(c, monday, 5,
            #                                   lessons_R, box_unit_height_R)

            # for skelly who has 3 lessons to the right
            # place_lesson_strings_on_R_canvas(c, monday, 5,
            #                                   lessons_R, box_unit_height_R)

            place_lesson_strings_on_R_canvas(c, monday, 6,
                                              lessons_R, box_unit_height_R)


        # Additional Information
        tuesday = monday + td(days=1)
        for aday in cal_list:
            if aday[1].date == tuesday:
                if aday[1].meeting:
                    c.rotate(90)
                    meeting_string = "%s meeting on %s" % \
                                     (aday[1].meeting, aday[1].date.strftime("%a %d"))
                    c.drawString(height/2, -width+1.2*cm, meeting_string) # 1.5cm for normal width


        c.showPage()





#################################
# Let's Make the actual Canvas! #
#################################



width, height = letter
top_margin = 1*inch
left_margin = 0.8*inch # 1.2*inch
right_margin = 0.68*inch
bottom_margin = 0.45*inch

c = canvas.Canvas("BHS_Paper_Planner.pdf", pagesize=letter)
c.setAuthor("Alvaro Feito Boirac")

add_lesson_details(c, full_schedule_by_year, all_weeks)

# make text go straight up
c.rotate(-90)
# change color
c.setFillColorRGB(0.77, 0, 0.77)
# say hello (note after rotate the y coord needs to be negative!)
# c.drawString(3*inch, -3*inch, "Hello World")
c.showPage()

# Second Page
c.setStrokeColorRGB(0.1, 0.1, 1) # blue
# draw_margins(c)

### Header ###
create_header(c, "Sept 11 - Sept 15")
c.save()
