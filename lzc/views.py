from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from lzc.models import User

import json
import sys
import urllib, urllib2, httplib2

reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.

def blog(request):
	userlist = User.objects.all()
	paras = {
		'user': userlist
	}
	return render_to_response("login.html", paras)

def log(request):
      url = 'https://api.weibo.com/oauth2/authorize'
      client_id = '111990827'
      redirect_uri = 'http://linzc.xyz/log_success'
      para = "?client_id=" + client_id + "&response_type=code&redirect_uri=" + redirect_uri
      return HttpResponseRedirect(url + para)

def log_success(request):
      if 'code' in request.GET:
            code = request.GET['code']
      else :
            return HttpResponse('Error: no code!')
      url = 'https://api.weibo.com/oauth2/access_token'
      redirect_uri = 'http://linzc.xyz/log_success'
      #redirect_uri = 'http://lzc.herokuapp.com/success'
      data = {
        'client_id': 111990827,
        'client_secret': '1c2705aa915a6612de43124a0dd298c9',
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
      }
      req = urllib2.Request(url, urllib.urlencode(data))
      response = urllib2.urlopen(req)
      res_data = response.read()
      res = json.loads(res_data)
      
      if 'uid' in res and 'access_token' in res :
            userlist = User.objects.filter(uid = res['uid'])
            if not userlist :
                  user = User(uid = res['uid'])
            else :
                  user = userlist.first()
            user.access_token = res['access_token'] 

            user_info = get_user_info(user.uid, user.access_token)
            user.name = user_info['screen_name']
            user.save()
            request.session['uid'] = res['uid']
            return HttpResponseRedirect('/posts/'+user.uid) 

def get_user_info(uid, access_token):
      url = 'https://api.weibo.com/2/users/show.json' 
      paras = urllib.urlencode({'uid':uid, 'access_token':access_token}) 
      response, content = httplib2.Http().request(url + '?' + paras)
      return json.loads(content) # change content to a json


def homepage(request):
      user = User.objects.filter(uid = request.session['uid']).first()
      response = get_weibo(user.uid, user.access_token)
      user_text = get_text_list(response)
      keywords = get_keywords(user_text).split(',')
      keywords = keywords[0:len(keywords)-1] 
     
      if 'keywords' in request.GET:
      	new_user_text = []
      	for text in user_text:
      		if request.GET['keywords'] in text:
      			new_user_text.append(text)
      	user_text = new_user_text
      para = {
            'name': user.name,
            'uid': user.uid ,
            'text': user_text,
            'keywords': keywords
      }
      return render_to_response(
            'homepage.html', para,
            context_instance = RequestContext(request)
      )		

def users(request):
      userlist = User.objects.all()
      dic = {'users': []}
      for u in userlist:
      	newuser = {}
      	newuser['name'] = u.name
      	newuser['uid'] = u.uid
        dic['users'].append(newuser)
      return HttpResponse(json.dumps(dic, ensure_ascii=False))  # change json to a string


def posts(request, userid):
	user = User.objects.filter(uid = userid).first()
	request.session['uid'] = userid
	response = get_weibo(user.uid, user.access_token)
	user_text = get_text_list(response)
	if len(user_text) == 0:
		keywords = ""
	else :
		keywords = get_keywords(user_text).split(',')
		keywords = keywords[0:len(keywords)-1] 
	if 'keywords' in request.GET:
		new_user_text = []
		for text in user_text:
			if request.GET['keywords'] in text:
				new_user_text.append(text)
		user_text = new_user_text
	
	para = {
    	'name': user.name,
    	'uid': user.uid ,
    	'text': user_text,
    	'keywords': keywords
    }
	return render_to_response(
    	'homepage.html', para,
    	context_instance = RequestContext(request)
    )		
''''
      user = User.objects.filter(uid = userid).first()
      if not user :
            return HttpResponse('No this user')
      else :
            post = {"posts": [], "uid": user.uid}
            response = get_weibo(user.uid, user.access_token) 
            user_text = get_text_list(response)
            post['posts'] = user_text
            if 'keywords' in request.GET:
                  if request.GET['keywords'] == '1' :
                        content = get_keywords(user_text)
                        post['keywords'] = json.loads(content)
            return HttpResponse(json.dumps(post, ensure_ascii=False)) 
'''
def get_weibo(uid, access_token):
      url = 'https://api.weibo.com/2/statuses/user_timeline.json'
      paras = urllib.urlencode({'uid' : uid, 'access_token' : access_token})
      response, content = httplib2.Http().request(url + '?' + paras) 
      return json.loads(content)  #content['statuses']['text'] 


def get_keywords(text):
      url = 'http://api.yutao.us/api/keyword/'
      text = ' '.join(text)
      res, keywords = httplib2.Http().request(url + text)
      if text.strip()=="":
      	return []
      return keywords								
      

def get_text_list(response):
	  user_text = []
	  for text in response['statuses']:
	  		user_text.append(text['text'])
	  return user_text

