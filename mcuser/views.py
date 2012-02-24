import base64
import datetime
import logging
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.context_processors import csrf
from django.db.models import Max
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required

from lib.utils import *
from mcuser.forms import *
from mcuser.models import *
from xlab.env_settings import *

def index(request):
    
    #TODO: Add usernme sign-up. Also, figure out how to do so from app.
    return HttpResponseRedirect("/admin/")
    
@login_required
def mcadmin(request):
    
    c = {}
    
    if not request.user.is_authenticated():
        
        #TODO: comment this out and test
        # Not really necessary as the @login_required decorator requires login...
        
        pass
    
    else:
        invite_accepted = 1 if "invite_accepted" in request.GET else 0

        #Check if we have meta data for the user
        try:
            user_md = UserMetaData.objects.get(user=request.user)
            c.update({'timezone': user_md.timezone})
            
        except UserMetaData.DoesNotExist:
            c.update({'client_login_required': True})

        c.update({'invite_accepted': invite_accepted,
            'user_is_approver': user_is_approver(request.user)})

        return render_to_response('mcuser/index.html',
            c, context_instance=RequestContext(request))

@login_required
def profile(request):
    return HttpResponseRedirect("/")

def register(request):
    if request.method == 'POST':
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationFormWithEmail()

    return render_to_response("registration/register.html", {'form': form,},
            context_instance=RequestContext(request))

@staff_member_required
def invite (request):
    try:
        c = {}

        form = InviteForm(request.POST or None, user=request.user)
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            group = form.cleaned_data['group']

            invite_code = base64.urlsafe_b64encode(os.urandom(32))
            invite = Invite(user=request.user.id, name=name, invite_email=email,
                invite_code=invite_code, group=Group.objects.get(pk=group))
            invite.save()

            invite_url = "<http://%s/user/invite/accept/?id=%s>" % (DOMAIN, invite_code)

            #Send the invite e-mail
            subject = "Invitation"
            message = ("Hi,\n\nThank you for your interest in testing %s. "
                "%s is a smart phone application paired with an online data "
                "collection and analysis service that can be used to monitor "
                "patterns of risky behavior of motorists. "
                "Please click on the following link to create an account:\n\n%s \n\n"
                "(You may have to copy and paste the link into your browser address bar if it is appearing on multiple lines)"
                "\n\nThanks,\nThe %s Team") % (COMPANY_NAME, COMPANY_NAME, invite_url, COMPANY_NAME)

            send_email(SENDER_EMAIL_ID, email, subject, message)
            c.update({"success_msg": "An invitation was e-mailed to %s" % email})
            logging.info("Invitation sent [by: %s] [to: %s]" % (request.user.username, email))

        # Get all the invitations
        # TODO: Add pagination
        invitations = Invite.objects.all().order_by('-id')
        c.update({"invitations": invitations})
        
    except Exception as e:
        logging.exception( str(e) )
        c.update({"error_msg": str(e)})


    c.update({'form': form})
    c.update(csrf(request))

    return render_to_response('mcuser/invite.html', c,
            context_instance=RequestContext(request))

def accept_invite (request):
    #Check if the invite ID is valid
    try:
        invite_code = request.GET['id']
        invite = Invite.objects.get(invite_code=invite_code)
        if invite.is_accepted == True:
            return HttpResponseRedirect("/?invite_accepted=1")
    except (Invite.DoesNotExist, KeyError):
        raise Http404

    if request.method == 'POST':
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.groups.add(invite.group)
            new_user.save()

            invite.is_accepted = True
            invite.save()

            #Send an e-mail with instructions on how to install the client application
            phone_model = form.cleaned_data['phone_model']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']

            if phone_model == "android":
                subject = "Android application installation instructions"
                message = ("Hi,\n\nYou have successfully created an account. "
                    "Please follow these steps to install the application on your phone:\n\n"
                    "- Confirm that you have a working EDGE or 3G data connection on the phone.\n"
                    "- Launch the Android Market application, search for MileSense and install it. "
                    "If you're reading this on your phone, just click on this link - "
                    "<https://market.android.com/details?id=com.milesense.android>\n"
                    "- Open the application and login with the username and password you "
                    "selected when you signed up. \n"
                    "- Press the home button to send the application to the "
                    "background, and you're done! \n\n"
                    "You can visit http://%s to view your driving data.\n\nPlease reply to this "
                    "email if you have any questions or need help.\n\nThanks,\nThe %s Team") % \
                    (DOMAIN, COMPANY_NAME)
            else:
                subject = "iPhone application status"
                message = ("Hi,\n\nYou have successfully registered for an account. "
                    "We will get in touch when our iPhone application is ready for use.\n\n"
                    "Thanks for your patience!\n\nThe %s team") % COMPANY_NAME

            send_email(SENDER_EMAIL_ID, email, subject, message)

            # Send an e-mail to the team
            update_subject = "Account created - %s" % (username)
            update_msg = "A new account has been created.\n\nUsername: %s\nE-mail: %s\nPhone model: %s" % \
                (username, email, phone_model)
            send_email(SENDER_EMAIL_ID, TEAM_MAIL_IDS, update_subject, update_msg)

            logging.info("New account created [username: %s] [email: %s] [phone model: %s]" % \
                (username, email, phone_model))

            return HttpResponseRedirect("/?invite_accepted=1")
    else:
        form = UserCreationFormWithEmail(email=invite.invite_email)

    return render_to_response("mcuser/accept_invite.html",
            {'form': form},
            context_instance=RequestContext(request))
