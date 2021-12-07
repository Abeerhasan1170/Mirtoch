from .models import Profile


class User:
    def __init__(self, jsonresp):
        self.created_at = jsonresp['created_at']
        self.id = jsonresp['id']
        self.full_text = jsonresp['full_text']
        self.favourite_count = jsonresp['favorite_count']
        self.retweet_count = jsonresp['retweet_count']
        try:
            self.media = jsonresp['extended_entities']['media'][0]['media_url_https']
        except:
            self.media = None
        self.favourites_count = jsonresp['user']['favourites_count']
        self.followers_count = jsonresp['user']['followers_count']
        self.friends_count = jsonresp['user']['friends_count']
        user_profile = Profile.objects.filter(
            user_name=jsonresp['user']['screen_name']).first()
        self.location = ''
        if user_profile:
            if user_profile.associated_country:
                self.location = user_profile.associated_country.name
            else:
                self.location = ''
        self.name = jsonresp['user']['name']
        self.profile_image = jsonresp['user']['profile_image_url_https'].replace(
            'normal', '400x400')
        self.screen_name = jsonresp['user']['screen_name']
        self.statuses_count = jsonresp['user']['statuses_count']
        self.bio = jsonresp['user']['description']
        self.website = jsonresp['user']['url']
        try:
            self.retweet = True
            self.created_at = jsonresp['retweeted_status']['created_at']
            self.full_text = jsonresp['retweeted_status']['full_text']
            self.favourite_count = jsonresp['retweeted_status']['favorite_count']
            self.retweet_count = jsonresp['retweeted_status']['retweet_count']
            try:
                self.media = jsonresp['retweeted_status']['extended_entities']['media'][0]['media_url_https']
            except:
                self.media = None
            self.favourites_count = jsonresp['retweeted_status']['user']['favourites_count']
            self.followers_count = jsonresp['retweeted_status']['user']['followers_count']
            self.friends_count = jsonresp['retweeted_status']['user']['friends_count']
            self.location = jsonresp['retweeted_status']['user']['location']
            self.name = jsonresp['retweeted_status']['user']['name']
            self.profile_image = jsonresp['retweeted_status']['user']['profile_image_url_https'].replace(
                'normal', '400x400')
            self.screen_name = jsonresp['retweeted_status']['user']['screen_name']
            self.statuses_count = jsonresp['retweeted_status']['user']['statuses_count']
            self.website = jsonresp['retweeted_status']['user']['url']
            self.bio = jsonresp['retweeted_status']['user']['description']
        except:
            self.retweet = False

    @classmethod
    def create_user(self, jsonresp):
        return User(jsonresp)


class FollowingUser:
    def __init__(self, jsonresp):
        self.name = jsonresp['name']
        self.screen_name = jsonresp['screen_name']
        self.description = jsonresp['description']
        self.profile_image = jsonresp['profile_image_url'].replace(
            'normal', '400x400')
        # self.created_at = jsonresp['status']['created_at']
        # self.full_text = jsonresp['status']['full_text']
        try:
            pass
        except:
            pass

    @classmethod
    def a(self, jsonresp):
        return FollowingUser(jsonresp)
