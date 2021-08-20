import requests
from django.contrib import auth
from django.shortcuts import render


from .auth import run
# Create your views here.
headers = run('OnerudeZombie', 'Aryan1122?')
content = requests.get(
    'https://shared.ap.a.pvp.net/content-service/v2/content', headers=headers).json()
agent_pic = requests.get(
    'https://valorant-api.com/v1/agents', headers=headers).json()['data']
puuid = requests.get(
    'https://api.henrikdev.xyz/valorant/v1/account/{}/{}'.format("OnerudeZombie", "NOOB"), headers=headers).json()['data']['puuid']
all = requests.get(
    'https://valorant-api.com/v1/agents?isPlayableCharacter=true').json()['data']
match = requests.get(
    'https://pd.ap.a.pvp.net/match-history/v1/history/{}'.format(puuid), headers=headers).json()['History']
loadout = requests.get(
    'https://pd.ap.a.pvp.net/personalization/v2/players/{}/playerloadout'.format(puuid), headers=headers).json()
Qskills = requests.get(
    'https://pd.ap.a.pvp.net/mmr/v1/players/{}'.format(puuid), headers=headers).json()['QueueSkills']
CompetitiveTier = requests.get(
    "https://valorant-api.com/v1/competitivetiers", headers=headers).json()


def home(request):

    Seasoninfo = Qskills['competitive']['SeasonalInfoBySeasonID']
    for i in Seasoninfo:
        Seasonid = i
        break
    rank = []
    rank.append(Seasoninfo[Seasonid]['Rank'])
    rankdetails = CompetitiveTier['data'][0]['tiers'][rank[0]]
    titles = requests.get(
        'https://valorant-api.com/v1/playertitles', headers=headers).json()['data']
    cards = requests.get(
        'https://valorant-api.com/v1/playercards', headers=headers).json()['data']
    PlayerCard = loadout['Identity']['PlayerCardID']
    PlayerTitle = loadout['Identity']['PlayerTitleID']
    Title = []
    Card = []
    for card in cards:
        if card['uuid'] == PlayerCard:
            Card.append(card)
    for title in titles:
        if title['uuid'] == PlayerTitle:
            Title.append(title)
    username = requests.get(
        'https://api.henrikdev.xyz/valorant/v1/account/{}/{}'.format("OneRudeZombie", "NOOB"), headers=headers).json()['data']
    progress = requests.get(
        'https://pd.ap.a.pvp.net/account-xp/v1/players/{}'.format(puuid), headers=headers).json()['Progress']

    return render(request, 'API/home.html', {'level': progress['Level'], 'xp': progress['XP'], 'username': username['name'], 'tag': username['tag'], 'card': Card, 'title': Title, 'rank': rankdetails})


def Match(request):
    match_info = requests.get(
        'https://pd.ap.a.pvp.net/match-details/v1/matches/{}'.format(match[0]['MatchID']), headers=headers).json()['matchInfo']

    map = []

    maps = requests.get('https://valorant-api.com/v1/maps',
                        headers=headers).json()['data']

    for mapId in maps:
        if mapId['mapUrl'] == match_info['mapId']:
            map.append(mapId['displayName'])
    return render(request, 'API/matches.html', {'match': match[0]['MatchID'], 'map': map,  'all': all})


def store(request):
    return render(request, 'API/store.html')


def current(request):
    return render(request, 'API/current.html')


def collection(request):
    return render(request, 'API/collection.html')


def agents(request):
    owned = requests.get(
        f'https://pd.ap.a.pvp.net/store/v1/entitlements/{puuid}/01bb38e1-da47-4e6a-9b3d-945fe4655707', headers=headers).json()['Entitlements']

    MainList = []
    characters_main = content['Characters']
    for agents in owned:
        for characters in characters_main:
            if characters['ID'].lower() == agents['ItemID']:
                MainList.append(characters['Name'])
    MainList = sorted(MainList)
    agent_name = []
    agent_locked = []
    for agent in agent_pic:
        if agent['displayName'] in {"Phoenix", "Jett", "Sova", "Sage", "Brimstone"}:
            continue
        for characters_pic in owned:
            if characters_pic['ItemID'] == agent['uuid']:
                agent_name.append(agent)
    locked = {agent['uuid'] for agent in all if not agent['isBaseContent']
              } - {agent['ItemID'] for agent in owned}
    for locked_agent in locked:
        for character_locked in agent_pic:
            if locked_agent == character_locked['uuid']:
                agent_locked.append(character_locked)
    return render(request, 'API/Agents.html', {'owned': MainList, 'agents': agent_name, 'agents_locked': agent_locked})


# def mapName(request, maps, match_info):
#     map = []
#     for mapId in maps:
#         if mapId['mapUrl'] == match_info['mapId']:
#             map.append(mapId['displayName'])
#     return render(request, 'API/home.html', {'map': map})
