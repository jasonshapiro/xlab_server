import logging
import random

from experiments.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User

def budget_lines(request):
    
    bl_list = list()
    
    def homemade_string_parser():
        #TODO: modify so that b_lines are selected selectively
        #
        #For each experiment (Java object XLabBudgetLineExperiement): 
        #  id (integer), title, lat, lon, radius, probabilistic (true if you get either X or Y, false if you get both),  prob_x (probability of getting X, only applicable if probabilistic is true), x_label (label of x axis), x_units (units of x axis), x_max (maximum x intercept), x_min (minimum x intercept), y_label (label of y axis), y_uints (units of y axis), y_max (maximum y intercept), y_min (minimum y intercept), 
        #
        #Then, for each experiment, a number of sessions for the set of budget lines subjects get at a given time (Java object Session):
        #  "session_parser" (for parsing), id (1 through number of Sessions), line_chosen (which line in the session will actually dictate rewards),
        #
        #Then, for each session,  a number of lines (Java object Line):
        #  "line_parser" (for parsing), id (1 through number of Lines), x_int (x-intercept of line), y_int (y-intercept of line), winner ("X" if only X is rewarded, "Y" otherwise, only applicable if probabilistic is true)
        #
        #Example encompassing a two-session probabilistic experiment in which line and a three-session non-probabilistic experiment (note it will come as one continuous string, with a newline between the experiments):
        #
        #"14,Muscovite Risk/Reward,Moscow,55.75,37.70,200,1,0.5,Reward if X chosen,Rubles,1500,750,Reward if Y chosen,Rubles,1500,750,
        #  session_parser,1,3,
        #    line_parser,1,800,1000,X,
        #    line_parser,2,1350,850,X,
        #    line_parser,3,1150,1250,Y,
        #    line_parser,4,1150,1250,Y,
        #  session_parser,2,2,
        #    line_parser,1,1100,1000,Y,
        #    ine_parser,2,750,1150,X,
        #    line_parser,3,1450,850,X,
        #    line_parser,4,850,1050,Y,
        #16,Kamchatkan Diet Selector,Petropavlovsk-Kamchatsky,53.01,158.65,200,1,0.5,Regional Fried Dough,Rubles,1000,500,Pickled Produce,Rubles,1000,500,
        #  session_parser,1,1,
        #    line_parser,1,800,700,X,
        #    line_parser,2,750,850,X,
        #    line_parser,3,550,500,Y,
        #    line_parser,4,600,750,Y,
        #  session_parser,2,4,
        #    line_parser,1,500,600,Y,
        #    line_parser,2,750,650,X,
        #    line_parser,3,650,850,X,
        #    line_parser,4,850,950,Y,
        #  session_parser,3,1,
        #    line_parser,1,600,600,Y,
        #    line_parser,2,650,650,X,
        #    line_parser,3,650,950,X,
        #    line_parser,4,750,950,Y,"

        b_lines = BudgetLine.objects.all()
        
        if (len(b_lines) == 0):
            return "blank"
        else:
            for bl in b_lines:
                bl_list.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' % (bl.id,bl.budget_line_info.title,#2
                                          bl.geofence.title,bl.geofence.lat, bl.geofence.lon, bl.geofence.radius,#4
                                          '1' if bl.budget_line_info.probabilistic else '0',bl.budget_line_info.prob_x,#2
                                          bl.budget_line_info.x_label, bl.budget_line_info.x_units, bl.budget_line_info.x_max, bl.budget_line_info.x_min,#4
                                          bl.budget_line_info.y_label, bl.budget_line_info.y_units, bl.budget_line_info.y_max, bl.budget_line_info.y_min ) )#4
                for i in range(1,bl.budget_line_info.number_sessions+1):
                    line_chosen = (int)((random.random() * bl.budget_line_info.number_sessions) // 1)
                    bl_list[len(bl_list)-1] = bl_list[len(bl_list)-1] + ('session_parser,%s,%s,' % ( i, line_chosen) )
                    for j in range(1,bl.budget_line_info.lines_per_session+1):
                        x_intercept = (random.random() * (bl.budget_line_info.x_max - bl.budget_line_info.x_min) + bl.budget_line_info.x_min)
                        y_intercept = (random.random() * (bl.budget_line_info.y_max - bl.budget_line_info.y_min) + bl.budget_line_info.y_min)
                        if (random.random() < bl.budget_line_info.prob_x):
                            winner = 'x'
                        else:
                            winner = 'y'                            
                        bl_list[len(bl_list)-1] = bl_list[len(bl_list)-1] + ( 'line_parser,%s,%s,%s,%s,' % (j, x_intercept, y_intercept, winner) )
            return "\n".join(bl_list)
    
    #TODO: Make this
    #def json_response():
        
    try:
        if request.method == 'GET':
            #TODO: This is an ugly hack. A non idempotent request like this
            # should be a POST, not GET. I can't quickly find a way around
            # Django's CSRF protection. If you're reading this, fix this code!
            # DV: Apparently a GET needs to get the token, followed by a POST. This could be a serious pain.
            # http://stackoverflow.com/questions/4455845/how-do-i-generate-a-django-csrf-key-for-my-iphone-and-android-apps-that-want-to
            
            if 'bl_id' in request.GET:
                bl_username = request.GET['bl_username']
                bl_id = request.GET['bl_id']
                bl_session = request.GET['bl_session']
                bl_line = request.GET['bl_line']
                bl_lat = request.GET['bl_lat']
                bl_lon = request.GET['bl_lon']
                bl_x = request.GET['bl_x']
                bl_y = request.GET['bl_y']
                bl_x_intercept = request.GET['bl_x_intercept']
                bl_y_intercept = request.GET['bl_y_intercept']
                bl_winner = request.GET['bl_winner']
                bl_line_chosen_boolean = request.GET['bl_line_chosen_boolean']
                
                bl = BudgetLine.objects.get(pk=bl_id)

                bl_user = User.objects.get(username=bl_username)
                # tq_response = True if tq_response == "1" else False
                
                # TODO clean up response
                
                blr = BudgetLineResult(user = bl_user, budget_line_info = bl, session = bl_session, line = bl_line, x_intercept = bl_x_intercept, y_intercept = bl_y_intercept, x = bl_x, y = bl_y, lat = bl_lat, lon = bl_lon, winner = bl_winner, line_chosen_boolean = bl_line_chosen_boolean)
                blr.save()

                logging.info("BL result was saved successfully - %s, %s" % (bl_id, bl_username))

                response = HttpResponse("1")
            else:
                response = HttpResponse(homemade_string_parser())


    except Exception as e:
        logging.exception( str(e) )
        response = HttpResponse("0")

    return response


def text_questions(request):
    
    def homemade_string_parser():
        t_questions = TextQuestion.objects.all()
        if (len(t_questions) == 0):
            return "blank"
        else:
            tq_list = list()
            for tq in t_questions:
                tq_list.append( "%s,%s,%s,%s,%s,%s" % (tq.id, tq.geofence.title, tq.geofence.lat,
                tq.geofence.lon, tq.geofence.radius, tq.text_question_info.question ) )

            return "\n".join(tq_list)

    try:
        if request.method == 'GET':
            #TODO: This is an ugly hack. A non idempotent request like this
            # should be a POST, not GET. I can't quickly find a way around
            # Django's CSRF protection. If you're reading this, fix this code!
            if 'tq_id' in request.GET:
                tq_username = request.GET['tq_username']
                tq_id = request.GET['tq_id']
                tq_lat = request.GET['tq_lat']
                tq_lon = request.GET['tq_lon']
                tq_response = request.GET['tq_response']

                tq = TextQuestion.objects.get(pk=tq_id)

                tq_user = User.objects.get(username=tq_username)
                # tq_response = True if tq_response == "1" else False
                
                # TODO clean up response
                
                tqr = TextQuestionResult(user=tq_user, text_question_info=tq, lat = tq_lat, lon = tq_lon, response=tq_response)
                tqr.save()

                logging.info("TQ result was saved successfully - %s, %s, %s" % (tq_id, tq_response, tq_username))

                response = HttpResponse("1")
            else:
                response = HttpResponse(homemade_string_parser())

    except Exception as e:
        logging.exception( str(e) )
        response = HttpResponse("0")

    return response