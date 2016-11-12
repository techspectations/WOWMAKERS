from django.shortcuts import render

# Create your views here.
import json,  random, re,requests
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *

NEWS_SECTIONS = ['wellness','top-stories','business','editors-pick',
'columns','multimedia','currency','life-style','entertainment',
'sports','news','in-depth']

# UTILITY FUNCTIONS

# creates a new user if he is messaging for first time.
def create_user(fbid):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name', 'access_token':'EAACZCBHTxqYQBAL0fqNJOmKLJEunGZCrLEo38r5oSyjoNFi2I1mGmqOQ9pjXPVtZBGDNZBQdYVHR21L655La3ZCUBQd2MuqSqYZCZBuU3XZAsEaHqWqHC6uag1ZAgxC5GmAECG2Wfxt120pkIo0A2Yt1atPZAJiV8IevkMr2ZAPooMLnAZDZD'}
    user_details = requests.get(user_details_url, user_details_params).json()
    pprint(user_details)
    print(user_details_url)
    user_name = ""
    if 'first_name' in user_details:
        user_name = user_details['first_name']
    if 'name' in user_details:
        user_name = user_details['name']
    user = Subscriber(id = int(fbid),name=user_name)
    user.save()
    post_facebook_message(fbid,"Hello "+user_name+". Welcome to MoBot, stay connected to us get all the local news right in your messenger :) " )
    post_facebook_subscribe_daily_button(fbid)

# sends a message to the person with given id.
def post_facebook_message(fbid, received_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAACZCBHTxqYQBAL0fqNJOmKLJEunGZCrLEo38r5oSyjoNFi2I1mGmqOQ9pjXPVtZBGDNZBQdYVHR21L655La3ZCUBQd2MuqSqYZCZBuU3XZAsEaHqWqHC6uag1ZAgxC5GmAECG2Wfxt120pkIo0A2Yt1atPZAJiV8IevkMr2ZAPooMLnAZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":received_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())       

# attachs the required buttons to reply message
def post_facebook_buttons(fbid,buttonarray):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAACZCBHTxqYQBAL0fqNJOmKLJEunGZCrLEo38r5oSyjoNFi2I1mGmqOQ9pjXPVtZBGDNZBQdYVHR21L655La3ZCUBQd2MuqSqYZCZBuU3XZAsEaHqWqHC6uag1ZAgxC5GmAECG2Wfxt120pkIo0A2Yt1atPZAJiV8IevkMr2ZAPooMLnAZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, 
        "message":{
            "attachment":{"type":"template",
                "payload":{"template_type":"button",
                "text":"Do you want to subscribe to our daily news letter",
                "buttons":[
                    buttonarray
                    ]}
            }
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())  


# retrns the edit distance between two points
def edit_distance(s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
                
        return v1[len(t)]

# used to store sections to database
def fetch_and_store_sections():
    r = requests.get('https://developer.manoramaonline.com/api/editions/en/sections', headers={'Authorization': '34aa328d-8354-50dc-bbeb-da209b13a458'})
    return (r)
def get_matching_section(a):
    a = a.lower().replace(' ','-')
    a_len = len(a)
    selected = "none"
    min_point = 3
    for i in NEWS_SECTIONS:
        cur_point = edit_distance(a,i)
        if(cur_point < min_point):
            min_point = cur_point
            selected = i
    return selected

def print_help(fbid):
    user = Subscriber.objects.get(id = int(fbid))
    text = "Hi "+user.name +"! \n"
    text += "Here are some tips\n"
    text += " use subscribe <topic name> to subscribe to a"





def post_facebook_subscribe_daily_button(fbid):
    buttonarray = [
          {
            "type":"postback",
            "title":"Yes",
            "payload":"subscribe_daily_yes"
          },
          {
            "type":"postback",
            "title":"No, thanks",
            "payload":"subscribe_daily_no"
          }
        ] 
    post_facebook_buttons(buttonarray)  

# Create your views here.dfs
class FbBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '1234':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                fbid = message['sender']['id']
                if 'message' in message:
                    # Print the message to the terminal
                    try:
                        user = Subscriber.objects.get(id=(int(message['sender']['id'])))
                    except:
                        create_user(message['sender']['id'])

                    
                    pprint(message)   
                    if 'text' in message['message']:
                        if(message['mess'])
                    else:
                        post_facebook_message(fbid,"Thank you :) ")   
                elif 'postback' in message:
                    if(message['postback']['payload'] == "subscribe_daily_yes"):
                        user = Subscriber.objects.get(id = int(fbid))
                        user.is_subscribed = True
                        user.save()
                        post_facebook_message(fbid,"You have been subscribed to our daily news letter. Thanks")

        return HttpResponse()

