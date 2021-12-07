from django.http import JsonResponse
import requests
import random
from allauth.socialaccount.models import SocialToken, SocialAccount
from requests_oauthlib import OAuth1
import os
from django.contrib.auth import logout
from .user import User as MyUser, FollowingUser
from django.contrib.auth.decorators import login_required
from .models import Profile, User, UserProfile
from . import words
import re
from .models import Publication, About, Volunteer, Country, Comment
from django.views.decorators.csrf import csrf_exempt
from .forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from bs4 import BeautifulSoup
# import requests
from time import perf_counter
from cachetools import TTLCache, cached
from django.views.decorators.cache import cache_page
from django.core.cache import cache
words = words.words

# HTTP Error 400


def bad_request(request, *args, **kwargs):
    response = render(
        request,
        'djangoTwitter/400.html'
    )
    response.status_code = 400
    return response

# HTTP Error 500


def server_error(request, *args, **kwargs):
    response = render(
        request,
        'djangoTwitter/500.html'
    )
    response.status_code = 500
    return response

# HTTP Error 404


def page_not_found(request, *args, **kwargs):
    response = render(
        request,
        'djangoTwitter/404.html'
    )
    response.status_code = 404
    return response

# HTTP Error 403


def permission_denied(request, *args, **kwargs):
    response = render(
        request,
        'djangoTwitter/403.html',
        context=RequestContext(request)
    )
    response.status_code = 403
    return response


def tweetSentiment(sentence):
    L = words[0]
    R = words[1]
    ia = 0
    la = 0
    a = []
    e = re.sub(r"(\?|#|\.|\.\.|\/|\‘|\’|\'|\,|\!|:|\\|\*)", "", sentence)
    s = re.sub(
        r"((https?|s?ftp|ssh)\:\/\/[^\"\s\<\>]*[^.,;'\">\:\s\<\>\)\]\!])", "", e).split(" ")
    for i in s:
        if i.lower() in L:
            ia += 1
        if i.lower() in R:
            la += 1
    return ia - la


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def tweetsBySentiment(tweets):
    great = 0
    good = 0
    neutral = 0
    bad = 0
    terrible = 0
    for i in tweets:
        tweet = ''
        try:
            tweet = i['retweeted_status']['full_text']
        except:
            tweet = i['full_text']
        sa = tweetSentiment(tweet)
        if sa == 0:
            neutral += 1
        if sa == 1:
            good += 1
        if sa >= 2:
            great += 1
        if sa == -1:
            bad += 1
        if sa <= -2:
            terrible += 1
    return great, good, neutral, bad, terrible


def loginWithTwitter(request):
    if request.user.is_authenticated:
        url = 'https://api.twitter.com/1.1/friends/list.json?tweet_mode=extended'
        u = SocialAccount.objects.get(user__username=request.user)
        auth = OAuth1(os.environ.get('API_KEY'), os.environ.get('API_SECRET_KEY'), os.environ.get(
            'ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
        resposne = requests.get(url, auth=auth)
        followings = resposne.json()['users']
        tweetObjects = []
        for i in followings:
            u = FollowingUser.a(i)
            tweetObjects.append(u)
        datas = []
        for i in tweetObjects:
            data = {
                'name': i.name,
                'profile_image': i.profile_image,
                'screen_name': i.screen_name,
            }
            datas.append(data)
        return render(request, 'djangoTwitter/vertical.html', {'data': datas, 'total_following': len(followings)})
    else:
        return render(request, 'djangoTwitter/vertical.html')


def logoutUser(request):
    logout(request)
    return redirect('mirtoch:home')


def userProfile(request, name):
    url = f'https://api.twitter.com/1.1/statuses/user_timeline.json?count=50&screen_name={name}&tweet_mode=extended'
    auth = OAuth1(os.environ.get('API_KEY'), os.environ.get('API_SECRET_KEY'),
                  os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
    resposne = requests.get(url, auth=auth)
    tweets = resposne.json()
    tweetObjects = []
    for i in tweets:
        try:
            if i['possibly_sensitive'] is False:
                u = MyUser.create_user(i)
                tweetObjects.append(u)
        except:
            u = MyUser.create_user(i)
            tweetObjects.append(u)
    if len(tweetObjects) <= 0:
        return render(request, 'djangoTwitter/sensitiveContent.html')
    datas = []
    for i in tweetObjects:
        data = {
            "id": i.id,
            "created_at": f'{i.created_at[11:16]} . {i.created_at[4:10]}, {i.created_at[-4:]}',
            "full_text": i.full_text,
            "favourite_count": i.favourite_count,
            "retweet_count": i.retweet_count,
            "favourites_count": i.favourites_count,
            "followers_count": i.followers_count,
            "friends_count": i.friends_count,
            "location": i.location,
            "name": i.name,
            "profile_image": i.profile_image,
            "screen_name": i.screen_name,
            "statuses_count": i.statuses_count,
            "media": i.media,
            "website": i.website,
            "retweet": i.retweet,
            "bio": i.bio
        }
        datas.append(data)
    # sentiment = []
    all_notifications = []
    if request.user.is_authenticated:
        all_notifications = request.user.notifications.all()
    try:
        p = Profile.objects.get(user_name=name)
    except:
        p = []
    print(datas[0])
    return render(request, 'djangoTwitter/profile.html', {'data': datas, 'sentiment': sentiment, 'profile': p, 'all_notifications': all_notifications})


def profileView(request):
    try:
        s = request.GET.get('screenName')
        return userProfile(request, s)
    except:
        return HttpResponse('<h1>User not found</h1>')


def scrap_corona_data():
    page = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(page.content, 'html.parser')
    countries = soup.find(id="main_table_countries_today")
    country_data_list = countries.find(
        'tbody').find_all("tr")
    attributes = ['no', 'country', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered',
                  'active_cases', 'serious_critical', 'cases_per_mill_pop']

    all_countries_data = []
    for country in country_data_list:
        country_stats = []
        for i in country.find_all("td"):
            country_stats.append(''.join(i.text.split(',')))
        detail = dict(zip(attributes, country_stats))
        country_obj = {
            "country": detail['country'],
            "total_cases": detail['total_cases'],
            "new_cases": detail['new_cases'].split('+')[::-1][0],
            "total_deaths": detail['total_deaths'],
            "total_recovered": detail['total_recovered']
        }
        all_countries_data.append(country_obj)

    all_cnts = Country.objects.all()
    country_names = [ct.name for ct in all_cnts]
    relevant_country_data = [
        cnt for cnt in all_countries_data if cnt['country'] in country_names]
    for count in relevant_country_data:
        for country in all_cnts:
            if count['country'] == country.name:
                country.total_cases = count['total_cases']
                country.new_cases = count['new_cases']
                country.total_deaths = count['total_deaths']
                country.total_recovered = count['total_recovered']
                country.save()


# @cache_page(60*10)
def home(request):
    all_notifications = {}
    all_countries = {}
    default_country = ''
    try:
        if request.user.is_authenticated:
            all_notifications = request.user.notifications.all()
            user_profiles = User.objects.select_related(
                'userprofile').get(username=request.user)
            if user_profiles:
                if user_profiles.userprofile.default_country:
                    default_country = user_profiles.userprofile.default_country.country_code
                else:
                    default_country = ''
        else:
            default_country = request.session['default_country']
    except Exception as e:
        print(e)
        default_country = ''
    t2_start = perf_counter()
    custom_countries, all_countries = sort_country_tweets(default_country)
    t2_stop = perf_counter()
    print("Query time: ", t2_stop - t2_start)
    all_tweets, top_tweets = get_all_tweets(default_country, all_countries)
    return render(request, "djangoTwitter/home.html", {
                            'all_tweets': all_tweets,
                            'top_tweets': top_tweets,
                            'default_country': default_country,
                            'all_countries': custom_countries,
                            'all_notifications': all_notifications})


def sort_country_tweets(default_country):
    all_countries = Country.objects.all()
    custom_countries = []
    for country in all_countries:
        country_obj = {
            "country_code": country.country_code,
            "name": country.name,
            "total_cases": country.total_cases,
            "new_cases": country.new_cases,
            "total_deaths": country.total_deaths,
            "total_recovered": country.total_recovered,
            "selected": False
        }
        custom_countries.append(country_obj)
    for cnt in custom_countries:
        if default_country == cnt['country_code']:
            cnt['selected'] = True
    return custom_countries, all_countries


@csrf_exempt
def change_default_country(request):
    country = request.POST.get('country')
    if not request.user.is_authenticated:
        request.session['default_country'] = country
        return JsonResponse('403', safe=False)
    if not country:
        user_profiles = UserProfile.objects.get(user=request.user)
        user_profiles.default_country = None
        user_profiles.save()
        return JsonResponse('200', safe=False)
    user_profiles = UserProfile.objects.get(user=request.user)
    my_country = Country.objects.get(country_code=country)
    user_profiles.default_country = my_country
    user_profiles.save()
    return JsonResponse('200', safe=False)


def fetch_tweets(list_id):
    print("hit the api")
    responses = []
    r = []
    auth = OAuth1(os.environ.get('API_KEY'),
                  os.environ.get('API_SECRET_KEY'),
                  os.environ.get('ACCESS_TOKEN'),
                  os.environ.get('ACCESS_TOKEN_SECRET'))
    url = f'https://api.twitter.com/1.1/lists/statuses.json?list_id={list_id}&tweet_mode=extended&count=50'
    resposne = requests.get(url, auth=auth).json()
    for i in resposne:
        try:
            if i['possibly_sensitive'] is False:
                responses.append(i)
        except:
            responses.append(i)
    r.append(responses)
    return r

# def get_all_tweets(country, all_countries):
#     responses = []
#     if not country or country is None:
#         for country in all_countries:
#             list_id = country.list_id
#             responses = fetch_tweets(list_id, responses)
#     else:
#         my_country = all_countries.filter(country_code=country).first()
#         list_id = my_country.list_id
#         responses = fetch_tweets(list_id, responses)
#     userobj = []
#     for res in responses:
#         if 'errors' not in res:
#             for i in res:
#                 u = MyUser.create_user(i)
#                 userobj.append(u)
#     datas = []
#     for i in userobj:
#         data = {
#             "id": i.id,
#             "favourite_count": i.favourite_count,
#             "retweet_count": i.retweet_count,
#             "created_at": f'{i.created_at[11:16]} . {i.created_at[4:10]}, {i.created_at[-4:]}',
#             "name": i.name,
#             "screen_name": i.screen_name,
#             "profile_image": i.profile_image,
#             "location": i.location,
#             "media": i.media,
#             "full_text": i.full_text,
#         }
#         datas.append(data)
#     top_tweets = pick_top_tweets(datas)
#     all_tweets = organize_tweets_by_category(datas)
#     return all_tweets, top_tweets


# with one list id

def get_all_tweets(country, all_countries):
    responses = []
    country = all_countries.first()
    list_id = country.list_id
    t1_start = perf_counter()
    responses = fetch_tweets(list_id)
    t1_stop = perf_counter()
    print("Elapsed time: ", t1_stop - t1_start)
    userobj = []
    for res in responses:
        if 'errors' not in res:
            for i in res:
                u = MyUser.create_user(i)
                userobj.append(u)
    datas = []
    for i in userobj:
        data = {
            "id": i.id,
            "favourite_count": i.favourite_count,
            "retweet_count": i.retweet_count,
            "created_at": f'{i.created_at[11:16]} . {i.created_at[4:10]},\
                            {i.created_at[-4:]}',
            "name": i.name,
            "screen_name": i.screen_name,
            "profile_image": i.profile_image,
            "location": i.location,
            "media": i.media,
            "full_text": i.full_text,
        }
        datas.append(data)
    top_tweets = pick_top_tweets(datas)
    all_tweets = organize_tweets_by_category(datas)
    return all_tweets, top_tweets


def pick_top_tweets(datas):
    '''Get only top tweets from the existing users'''
    top_tweets = []
    categories = ['G', 'A', 'M', 'P', 'O']
    for cat in categories:
        g = Profile.objects.filter(category=cat)
        for data in datas:
            for names in g:
                if data['screen_name'] == names.user_name:
                    data['category'] = cat
                    top_tweets.append(data)
    new_list = top_tweets[:]
    random.shuffle(new_list)
    return new_list[:4]


def organize_tweets_by_category(datas):
    ''' Orginize tweets by categories before displaying them in UI'''
    all_tweets = []
    categories = ['G', 'A', 'M', 'P', 'O']
    for cat in categories:
        g = Profile.objects.filter(category=cat)
        for data in datas:
            for names in g:
                if data['screen_name'] == names.user_name:
                    data['category'] = cat
                    all_tweets.append(data)

    filtered_tweets = {}
    for cat in categories:
        cat_tweets = []
        for tweet in all_tweets:
            if tweet['category'] == cat:
                cat_tweets.append(tweet)
        filtered_tweets[cat] = cat_tweets[:8]
    return filtered_tweets


# @cache_page(60*10)
def get_category(request, catname):
    '''Get tweets from a specific category based on given url'''
    # all_countries = []
    all_notifications = []
    # try:
    #     all_countries = Country.objects.all()
    #     if request.user.is_authenticated:
    #         all_notifications = request.user.notifications.all()
    #         user_profiles = User.objects.select_related(
    #             'userprofile').get(username=request.user)
    #         if user_profiles:
    #             country = user_profiles.userprofile.default_country.country_code
    #     else:
    #         country = request.session['default_country']
    # except Exception as e:
    #     country = ''
    responses = fetch_tweets(Country.objects.first().list_id)
    ###### With multiple list id #######
    # if not country or country is None:
    #     for cntr in all_countries:
    #         list_id = cntr.list_id
    #         responses = fetch_tweets(list_id, responses)
    # else:
    #     my_country = all_countries.filter(country_code=country).first()
    #     list_id = my_country.list_id
    #     responses = fetch_tweets(list_id, responses)

    userobj = []
    datas = []
    for res in responses:
        if 'errors' not in res:
            for i in res:
                u = MyUser.create_user(i)
                userobj.append(u)
    for i in userobj:
        data = {
            "id": i.id,
            "favourite_count": i.favourite_count,
            "retweet_count": i.retweet_count,
            "created_at": f'{i.created_at[11:16]} . {i.created_at[4:10]},\
                            {i.created_at[-4:]}',
            "name": i.name,
            "screen_name": i.screen_name,
            "profile_image": i.profile_image,
            "location": i.location,
            "media": i.media,
            "full_text": i.full_text,
        }
        datas.append(data)
    all_tweets = []
    categories = ['government', 'active', 'media', 'business', 'political']
    error = False
    if catname not in categories:
        error = 'Category not Found'
        return render(request, 'djangoTwitter/category.html', {
            'error': error, 'all_notifications': all_notifications})
    g = get_profiles_based_on_categories(request, catname)
    for data in datas:
        for names in g:
            if data['screen_name'] == names.user_name:
                data['category'] = names.category
                all_tweets.append(data)
    if len(all_tweets) == 0:
        error = 'No tweets in this category yet'
    return render(request, 'djangoTwitter/category.html', {
        'category': catname.capitalize(),
        'all_tweets': all_tweets, 'error': error,
        'all_notifications': all_notifications})


def get_profiles_based_on_categories(request, catname):
    '''Helper function for filtering out categorized tweets'''
    g = []
    if catname == 'government':
        g = Profile.objects.filter(category='G')
    if catname == 'political':
        g = Profile.objects.filter(category='O')
    if catname == 'active':
        g = Profile.objects.filter(category='A')
    if catname == 'media':
        g = Profile.objects.filter(category='M')
    if catname == 'business':
        g = Profile.objects.filter(category='P')
    return g


def query_user(request):
    client_ip = get_client_ip(request)
    total_calls = cache.get(client_ip)
    username = request.GET.get('screenName')
    print(username)
    if total_calls is None:
        total_calls = 0
    if cache.get(client_ip):
        if total_calls >= 100:
            messages.success(request, "You have exceeded the limit. Please try\
                    again after 15 minutes")
    try:
        s = request.GET.get('screenName')
        cache.set(client_ip, total_calls + 1, timeout=60*15)
        return userProfile(request, s)
    except Exception:
        return HttpResponse('<h1>User not found</h1>')


def about(request):
    about = About.objects.all()
    all_notifications = []
    if request.user.is_authenticated:
        all_notifications = request.user.notifications.all()
    return render(request, 'djangoTwitter/about.html', {'about': about, 'all_notifications': all_notifications})


def publications(request):
    pub = Publication.objects.all().order_by('-date')
    recent_pub = Publication.objects.all().order_by('-pk')[0:5]
    all_notifications = []
    if request.user.is_authenticated:
        all_notifications = request.user.notifications.all()
    return redirect(f'{recent_pub[0].slug}/')
    # return render(request, 'djangoTwitter/publications.html', {'pub': pub, 'all_notifications': all_notifications, 'recent_pub': recent_pub})


@csrf_exempt
def add_comment(request):
    if request.method == "POST" and request.user.is_authenticated:
        comment = request.POST.get('comment')
        slug = request.POST.get('slug')
        user = request.user
        pub = Publication.objects.filter(slug=slug).first()
        new_comment = Comment(user=user, publication=pub, content=comment)
        new_comment.save()
        return JsonResponse('200', safe=False)
    else:
        return JsonResponse('400', safe=False)


def single_publication(request, slug):
    # return HttpResponse(slug)
    current_pub = Publication.objects.filter(slug=slug).first()
    recent_pub = Publication.objects.all().order_by('-pk')[0:5]
    comments = Comment.objects.filter(publication=current_pub).order_by('-pk')
    all_notifications = []
    if request.user.is_authenticated:
        all_notifications = request.user.notifications.all()
    return render(request, 'djangoTwitter/singlepublication.html', {
        'current_pub': current_pub, 'all_notifications': all_notifications,
        'comments': comments, 'recent_pub': recent_pub})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            payload = {
                'email': email,
                'username': username,
                'exp': datetime.utcnow() + timedelta(minutes=60)
            }
            token = jwt.encode(payload, os.environ.get('API_SECRET_KEY'),
                               algorithm='HS256').decode('utf-8')
            sender = os.getenv('EMAIL_HOST_USER')
            link = os.environ.get('CURRENT_URL') + f"/verify/{token}"
            email_subject = "Mirtoch Email verification"
            message = render_to_string('djangoTwitter/activation.html', {
                'title': email_subject,
                'username': username,
                'verification_link': link
            })
            send_mail(email_subject, '', sender, [
                      email, ], html_message=message)
            messages.success(
                request, f'Account created for {username}. Check your email for a verification link')
            form.save()
    else:
        form = UserCreationForm()
    return render(request, 'djangoTwitter/register.html', {'form': form})


def verify_email(request, token):
    message = 'Welcome to Mirtoch'
    btn_txt = 'Login'
    try:
        email = jwt.decode(token, os.environ.get('API_SECRET_KEY'))['email']
        username = jwt.decode(token, os.environ.get('API_SECRET_KEY'))['username']
        user = User.objects.get(username=username)
        user_profile = User.objects.select_related(
            'userprofile').get(username=username)
        is_verified = user_profile.userprofile.is_verified
        if is_verified:
            site_link = get_current_site(request)
            message = 'User account is already verified. Login to continue'
            return render(request, 'djangoTwitter/success_verify.html', {'form': form})
        user_profile.userprofile.is_verified = True
        user_profile.save()
        message = 'Your email has been verified successfully. Login to continue'
    except Exception as e:
        print(e)
        message = 'Oops! The verification link has expired'
        btn_txt = 'Contact Admin'
    return render(request, 'djangoTwitter/success_verify.html', {'message': message, 'btn_txt': btn_txt})


def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        user_profile = None
        if user:
            try:
                user_profile = User.objects.select_related(
                    'userprofile').get(username=username)
                is_verified = user_profile.userprofile.is_verified
            except Exception as e:
                print(e)
                is_verified = False
            if is_verified or user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('mirtoch:home')
            else:
                messages.info(
                    request, 'User account is not yet verified via email')
                form = AuthenticationForm()
        else:
            messages.error(request, 'Invalid username or password')
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'djangoTwitter/login.html', {'form': form})


@csrf_exempt
def sendmessage(request):
    if request.method == 'POST':
        fname = request.POST.get('name')
        lname = request.POST.get('surname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        v = Volunteer(first_name=fname, last_name=lname,
                      email=email, comment=message)
        v.save()
    return HttpResponse(' ')


def terms(request):
    return render(request, 'djangoTwitter/terms.html')


def sentiment(request, name):
    url = f'https://api.twitter.com/1.1/statuses/user_timeline.json?count=50&screen_name={name}&tweet_mode=extended'
    auth = OAuth1(os.environ.get('API_KEY'), os.environ.get('API_SECRET_KEY'),
                  os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
    resposne = requests.get(url, auth=auth)
    tweets = resposne.json()
    ps = []
    for i in tweets:
        try:
            if i['possibly_sensitive'] is False:
                ps.append(i)
        except:
            ps.append(i)
    if len(ps) > 0:
        sentiment = tweetsBySentiment(tweets)
        return JsonResponse(sentiment, safe=False)
    else:
        return JsonResponse([0, 0, 0, 0], safe=False)


