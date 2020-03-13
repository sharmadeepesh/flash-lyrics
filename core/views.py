from django.shortcuts import render
from django.http import HttpResponse
from core.models import song, result

from bs4 import BeautifulSoup
import requests
import json
import spotipy
import spotipy.util as util
import urllib.parse
import random

client_id = "6315f27b26664ac5af1ff41d962458b8"
client_secret = "2cd8131dbae54f19b96308160492db1a"

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

# Create your views here.
def index(request):
    return render(request,'landing.html')

def artist(request,artist):
    images = []
    names = []
    artists = []
    artist = urllib.parse.unquote(artist)
    if result.objects.filter(artist=artist).exists():
        results = result.objects.filter(artist=artist)
        for elem in results:
            song_name = elem.name
            artist_name = elem.artist
            image_link = elem.image
            names.append(song_name)
            artists.append(artist_name)
            images.append(image_link)
        final = list(zip(names, artists, images))
        data = {
            'results' : final,
        }
        return render(request, 'core/artist.html', context=data)
    else:
        return render(request,'core/not_found.html')
        

def search(request):
    response = ""
    artist = []
    song_name = ""
    artist_name = ""
    image_link = ""
    images = []
    name = []
    token =util.oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    access_token = token.get_access_token()
    if request.method == "POST":
        token = "https://accounts.spotify.com/authorize?client_id={}8&response_type=token&redirect_uri=http://flashlyrics.herokuapp.com/search"
        response = requests.get(token.format(client_id))
        r = response.headers
        song_name = request.POST.get('song_name')
        song_to_render = song_name
        url = "https://api.spotify.com/v1/search?q={}&type=track&access_token={}"
        search_url = url.format(song_name,access_token)
        response = requests.get(search_url)
        response = json.loads(response.text)
        response = response['tracks']['items']
        if len(response) == 0:
            return render(request,'core/not_found.html')
        else:
            for items in response:
                if items['album']['artists'][0]['name'] == "Various Artists":
                    pass
                elif len(items['album']['artists'][0]['name']) > 40:
                    pass
                else:
                    song_name = (items['name']).replace('/','')
                    image_link = items['album']['images'][0]['url']
                    artist_name = items['album']['artists'][0]['name']
                    artist_name = (items['album']['artists'][0]['name']).replace('/','-')
                    name.append(song_name)
                    images.append(image_link)
                    artist.append(artist_name)
                    if result.objects.filter(name=song_name,artist=artist_name,image=image_link).exists():
                        pass
                    else:
                        Search = result(name=song_name,artist=artist_name,image=image_link)
                        Search.save()
            final = list(zip(name, artist, images))
            data = {
                'results' : final,
                'song_to_render' : song_to_render,
            }
            return render(request,'core/results.html',context=data)
    else:
        return render(request,'core/search.html')

def lyrics(request,artist,name):
    lyrics = ""
    if song.objects.filter(name=name, artist=artist).exists():
        Song = song.objects.filter(name = name, artist=artist)
        name = Song[0].name
        lyrics = Song[0].lyrics
        lyrics = lyrics.replace('â','\'')
        context = {
            'artist' : artist,
            'name' : name,
            'lyrics' : lyrics,
        }
        return render(request,"core/lyrics.html",context=context)
    else:
        url = "https://search.azlyrics.com/search.php?q={}"
        query = artist + ' ' + name
        user_agent = random.choice(user_agent_list)
        print(user_agent)
        response = requests.get(url.format(urllib.parse.quote(query)))
        soup = BeautifulSoup(response.text,'html.parser')
        try:
            link = soup.find('td',{'class':'text-left'})
            song_url = link.find('a').get('href')
            response = requests.get(song_url).text
            soup = BeautifulSoup(response,'html.parser')
            for goods in soup.find_all('div',{'class':None}):
                if len(goods.text)==0:
                    pass
                lyrics += goods.text
            try:
                Song = song(name=name, artist = artist, lyrics = lyrics)
                Song.save()
                context = {
                    'artist' : artist,
                    'name' : name,
                    'lyrics' : lyrics,     
                }
                return render(request,"core/lyrics.html", context = context)
            except KeyError:
                return render(request,"core/404.html")
        except AttributeError:
            return render(request,"core/lyrics_not_found.html")
    

'''def name_add_lyrics(request, artist, name):
    return render(request,"core/name_add_lyrics.html")

def lyric_added(request, artist, name):
    lyrics = request.POST.get('lyrics')
    Song = song(name=name, artist=artist, lyrics=lyrics)
    Song.save()
    context = {
        'name' : name,
        'artist' : artist,
    }
    return render(request, "core/success.html", context=context)'''