import requests
from django.contrib import auth
from django.shortcuts import render


from .auth import run
# Create your views here.
headers = run('baburaooo7', 'mayank1234')
content = requests.get(
    'https://shared.ap.a.pvp.net/content-service/v2/content', headers=headers).json()
agent_pic = requests.get(
    'https://valorant-api.com/v1/agents', headers=headers).json()['data']
puuid = requests.get(
    'https://api.henrikdev.xyz/valorant/v1/account/{}/{}'.format("baburao", "1942"), headers=headers).json()['data']['puuid']
all = requests.get(
    'https://valorant-api.com/v1/agents?isPlayableCharacter=true').json()['data']
match = requests.get(
    'https://pd.ap.a.pvp.net/match-history/v1/history/{}'.format(puuid), headers=headers).json()['History']


def home(request):

    # headers = {
    #     'Authorization': 'Bearer eyJraWQiOiJzMSIsInR5cCI6ImF0K2p3dCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyNjA1N2Q3ZS1iNTI3LTUzNTAtYTFhYy1lNmM1YmJlOTI4OGYiLCJzY3AiOlsib3BlbmlkIl0sImNsbSI6WyJvcGVuaWQiXSwiZGF0Ijp7ImxpZCI6IkhlRDBNa3FTOW1sbUlSc0lEOG5GclEiLCJjIjoiZWMxIn0sImlzcyI6Imh0dHBzOlwvXC9hdXRoLnJpb3RnYW1lcy5jb20iLCJleHAiOjE2MjcwNDkyNDIsImlhdCI6MTYyNzA0NTY0MiwianRpIjoiUk1PU2xkaXJZVjgiLCJjaWQiOiJwbGF5LXZhbG9yYW50LXdlYi1wcm9kIn0.T9fHWivaCdkWzrEAHDSpFsjmaSy5UgcJHeXBMPAoLlZWMLDKSgHcISJP1kC8qQ5FI7zj9RJg9BNtrCjR1NLdKi-m7zpTgiuBoQ4d_9LFhZWyjJYZnWm8pGtUG4Sunlj__PNfZwqfaQT_zTx52hmQNa8m0hzwewgnV2jJldtt4Mg',
    #     'X-Riot-Entitlements-JWT': 'eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoibi1yVm5WNEVJd3F6dGJHeVh6YS16ZyIsInN1YiI6IjI2MDU3ZDdlLWI1MjctNTM1MC1hMWFjLWU2YzViYmU5Mjg4ZiIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNjI3MDQ1NjQzLCJqdGkiOiJSTU9TbGRpcllWOCJ9.mQCiCMTjX4b41Nm-qnqM7lIiJI0NZRkCorJStDGISZafB3760xtAJFfUEKRCHL_udajKBC5yRsYygmfj7HeKKLSaUvNDeDv4FM7F2oHL_bdCMEQ04DDiwL-T4PMIXtQIWWYuj-Y9BGUaTv5T679nJzv-NIwNt4ROPczQtzYQC4vQ3RqDkLGWUcu2OiNazHoo374NjyzXzjYJTwKVBkLw-tc4v7yNLgubEn0oREgnG7YfaGgno1O9EfUSLEnEmLmrzlBk4cuJEBk5Sxu0Da9-TGrCikOxECsZBiFspz_6cWh6DG5z8SEVNEGOoGXqqs3wJ2pm_bvISqkuSLP0R2dg_Q',
    # }

    username = requests.get(
        'https://api.henrikdev.xyz/valorant/v1/account/{}/{}'.format("baburao", "1942"), headers=headers).json()['data']
    progress = requests.get(
        'https://pd.ap.a.pvp.net/account-xp/v1/players/{}'.format(puuid), headers=headers).json()['Progress']

    # for map_letter in range(11, 20):
    #     if match_info['matchInfo']['mapId'][map_letter] == '/':
    #         break
    #     map.append(match_info['matchInfo']['mapId'][map_letter])

    return render(request, 'API/home.html', {'level': progress['Level'], 'xp': progress['XP'], 'username': username['name'], 'tag': username['tag']})


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
