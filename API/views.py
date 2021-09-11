import requests
from django.contrib import auth
from django.shortcuts import render


from .auth import run
# Create your views here.
Username = 'OneRudeZombie'
gameUsername = 'SEN Cheems'
password = 'Aryan1122?'
headers = run(Username, password)
agent_pic = requests.get(
    'https://valorant-api.com/v1/agents').json()['data']
puuid = requests.get(
    'https://api.henrikdev.xyz/valorant/v1/account/{}/{}'.format(gameUsername, "NOOB"), headers=headers).json()['data']['puuid']
all = requests.get(
    'https://valorant-api.com/v1/agents?isPlayableCharacter=true').json()['data']
match = requests.get(
    'https://pd.ap.a.pvp.net/match-history/v1/history/{}?startIndex=0&endIndex=20'.format(puuid), headers=headers).json()['History']
Qskills = requests.get(
    'https://pd.ap.a.pvp.net/mmr/v1/players/{}'.format(puuid), headers=headers).json()['QueueSkills']
CompetitiveTier = requests.get(
    "https://valorant-api.com/v1/competitivetiers").json()
competitiveupdate = requests.get(
    f'https://pd.ap.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates?startIndex=0&endIndex=15&queue=competitive', headers=headers).json()['Matches']

maps = requests.get('https://valorant-api.com/v1/maps').json()['data']
gamemodes = requests.get(
    'https://valorant-api.com/v1/gamemodes', headers=headers).json()['data']
gamemodes[0]['displayName'] = 'Unrated'


def home(request):
    username = gameUsername
    progress = requests.get(
        'https://pd.ap.a.pvp.net/account-xp/v1/players/{}'.format(puuid), headers=headers).json()['Progress']
    rrupdate = competitiveupdate[0]['RankedRatingEarned']
    kills = 0
    deaths = 0
    id = []
    for ids in match:
        id.append(ids['MatchID'])
    for matches in range(20):
        match_info = requests.get('https://pd.ap.a.pvp.net/match-details/v1/matches/{}'.format(
            id[matches]), headers=headers).json()['players']
        for player in match_info:
            if player['gameName'] == username:
                kills = kills + player['stats']['kills']
                deaths = deaths + player['stats']['deaths']
    kd = round(kills/deaths, 2)
    Seasoninfo = Qskills['competitive']['SeasonalInfoBySeasonID']
    for i in Seasoninfo:
        Seasonid = i
        break
    unrated = Qskills['unrated']['SeasonalInfoBySeasonID'][Seasonid]
    urwins = unrated['NumberOfWinsWithPlacements']
    urtotal = unrated["NumberOfGames"]
    urloss = urtotal - urwins
    winpur = round(urwins*100/urtotal, 2)

    spikerush = Qskills['spikerush']['SeasonalInfoBySeasonID'][Seasonid]
    srwins = spikerush['NumberOfWinsWithPlacements']
    srtotal = spikerush["NumberOfGames"]
    srloss = srtotal - srwins
    winpsr = round(srwins*100/srtotal, 2)

    compwins = Seasoninfo[Seasonid]['NumberOfWinsWithPlacements']
    comptotal = Seasoninfo[Seasonid]["NumberOfGames"]
    comploss = comptotal-compwins
    rr = Seasoninfo[Seasonid]["RankedRating"]
    winpcomp = round(compwins*100/comptotal, 2)

    custom = Qskills['custom']['SeasonalInfoBySeasonID'][Seasonid]
    cuwins = custom['NumberOfWinsWithPlacements']
    cutotal = custom["NumberOfGames"]
    culoss = cutotal - cuwins
    winpcu = round(cuwins*100/cutotal, 2)

    rank = []
    rank.append(Seasoninfo[Seasonid]['Rank'])
    rankdetails = CompetitiveTier['data'][0]['tiers'][rank[0]]

    userparty = {}
    partyDetails = []
    lastmatch = requests.get(
        'https://pd.ap.a.pvp.net/match-details/v1/matches/{}'.format(match[0]['MatchID']), headers=headers).json()
    match_details = lastmatch['matchInfo']
    timeplayed_sec = (match_details['gameLengthMillis']/1000) % 60
    timeplayed_min = match_details['gameLengthMillis']/60000
    players = lastmatch['players']
    card_id = "https://valorant-api.com/v1/playercards/"
    agent_id = "https://valorant-api.com/v1/agents/"
    for user in players:
        if user['gameName'] == username:
            teamid = user['teamId']
            agent_lastid = user['characterId']
            killcount = user['stats']['kills']
            deathcount = user['stats']['deaths']
            assistscount = user['stats']['assists']
            scorecount = user['stats']['score']
            partyid = user['partyId']
            PlayerCard = user['playerCard']
            PlayerTitle = user['playerTitle']

    titles = requests.get(
        'https://valorant-api.com/v1/playertitles').json()['data']
    cards = requests.get(
        'https://valorant-api.com/v1/playercards',).json()['data']

    # for partyusers in players:
    #     if partyusers['partyId'] == partyid and partyusers['gameName'] != username:
    #         userparty.append(partyusers)
    # for party in players:
    #     for allcards in cards:
    #         if allcards['uuid'] == party['playerCard'] and party['partyId'] == partyid and party['gameName'] != username:
    #             partycards.append(allcards)

    Title = []
    Card = []

    for card in cards:
        if card['uuid'] == PlayerCard:
            Card.append(card)

    for title in titles:
        if title['uuid'] == PlayerTitle:
            Title.append(title)
    for agents in agent_pic:
        if agent_lastid == agents['uuid']:
            agent_lastpic = agents['displayIconSmall']
    matchresult = lastmatch['teams']
    for teams in matchresult:
        if teams['teamId'] == teamid:
            if teams['won']:
                result = 'Victory'
            else:
                result = 'Defeat'
            roundsWon = teams['roundsWon']
            roundsPlayed = teams['roundsPlayed']
            roundsLost = abs(roundsPlayed-roundsWon)
    gamemode = match_details['queueID']
    if gamemode == 'ggteam':
        gamemode = 'Escalation'
    if gamemode == 'onefa':
        gamemode == 'Replication'
    for mapId in maps:
        if mapId['mapUrl'] == match_details['mapId']:
            mapname = mapId['displayName']
            mappic = mapId['listViewIcon']

    for mode in gamemodes:
        if mode['displayName'].upper() == gamemode.upper():
            gamemodeIcon = mode['displayIcon']
            break
        if gamemode == "competitive":
            gamemodeIcon = rankdetails['smallIcon']
            break
        else:
            gamemodeIcon = 'https://inceptum-stor.icons8.com/s2he3DWV4kZd/valorant%20icon.png'
            gamemode = 'Custom'
    i = 0
    for user in players:

        if user['partyId'] == partyid and user['gameName'] != username:
            userparty = {}
            agenturl = agent_id + user['characterId']
            cardurl = card_id + user['playerCard']
            card = requests.get(cardurl).json()['data']['wideArt']
            agent = requests.get(agenturl).json()['data']['displayIcon']
            userparty['gameName'] = user['gameName']
            userparty['tagLine'] = user['tagLine']
            userparty['kills'] = user['stats']['kills']
            userparty['deaths'] = user['stats']['deaths']
            userparty['assists'] = user['stats']['assists']
            userparty['cardurl'] = card
            userparty['agenturl'] = agent

            partyDetails.append(userparty)
            # i = i+1
            # if gamemode == 'Custom':
            #     if i == 5:
            #         break

    return render(request, 'API/home.html', {'level': progress['Level'], 'xp': progress['XP'], 'username': username,
                                             'tag': 'NSOOB', 'card': Card, 'title': Title, 'rank': rankdetails, 'kills': kills,
                                             'deaths': deaths, 'kd': kd, 'compwins': compwins, 'comptotal': comptotal, 'comploss': comploss,
                                             'winpcomp': winpcomp, 'rr': rr, 'urwins': urwins, 'urtotal': urtotal, 'urloss': urloss, 'winpur': winpur,
                                             'srwins': srwins, 'srtotal': srtotal, 'srloss': srloss, 'winpsr': winpsr,
                                             'cuwins': cuwins, 'cutotal': cutotal, 'culoss': culoss, 'winpcu': winpcu, 'rrchange': rrupdate,
                                             'sec': int(timeplayed_sec), 'min': int(timeplayed_min), 'gamemode': gamemode.upper(),
                                             'mapname': mapname, 'mappic': mappic, 'result': result.upper(), 'agentpic': agent_lastpic, 'icon': gamemodeIcon,
                                             'won': roundsWon, 'lost': roundsLost, 'aryan': mode['displayName'], 'killcount': killcount, 'deathcount': deathcount, 'assistscount': assistscount, 'scorecount': scorecount,
                                             'party': partyDetails})


def Match(request):
    match_info = requests.get(
        'https://pd.ap.a.pvp.net/match-details/v1/matches/{}'.format(match[0]['MatchID']), headers=headers).json()['matchInfo']

    map = []

    for mapId in maps:
        if mapId['mapUrl'] == match_info['mapId']:
            map.append(mapId['displayName'])
    return render(request, 'API/matches.html', {'match': match[0]['MatchID'], 'map': map,  'all': all})


def store(request):
    store = requests.get(
        f'https://pd.ap.a.pvp.net/store/v2/storefront/{puuid}', headers=headers).json()
    single_skin = store['SkinsPanelLayout']['SingleItemOffers']
    store = []
    for skin in single_skin:
        skins = f'https://media.valorant-api.com/weaponskinlevels/{skin}/displayicon.png'
        store.append(skins)
    return render(request, 'API/store.html', {'store': store})


def current(request):
    owned = requests.get(
        f'https://pd.ap.a.pvp.net/store/v1/entitlements/{puuid}/01bb38e1-da47-4e6a-9b3d-945fe4655707', headers=headers).json()['Entitlements']

    MainList = []
    for agents in owned:
        for characters in agent_pic:
            if characters['uuid'] == agents['ItemID']:
                MainList.append(characters['displayName'])
    MainList = sorted(MainList)
    agent_name = []
    for agent in agent_pic:
        if agent['displayName'] in {"Phoenix", "Jett", "Sova", "Sage", "Brimstone"}:
            continue
        for characters_pic in owned:
            if characters_pic['ItemID'] == agent['uuid']:
                agent_name.append(agent)
    return render(request, 'API/current.html', {'owned': MainList, 'agents': agent_name})


def collection(request):
    loadout = requests.get(
        f'https://pd.ap.a.pvp.net/personalization/v2/players/{puuid}/playerloadout', headers=headers).json()['Guns']

    collect = []
    for gun in loadout:
        skin = gun['SkinID']
        skins = f'https://media.valorant-api.com/weaponskins/{skin}/displayicon.png'
        if skins == 'https://media.valorant-api.com/weaponskins/940fb417-4a9c-3004-41f5-3e8f1f4178b2/displayicon.png':
            continue
        else:
            collect.append(skins)
    return render(request, 'API/collection.html', {'collection': collect})


def agents(request):
    owned = requests.get(
        f'https://pd.ap.a.pvp.net/store/v1/entitlements/{puuid}/01bb38e1-da47-4e6a-9b3d-945fe4655707', headers=headers).json()['Entitlements']

    MainList = []
    for agents in owned:
        for characters in agent_pic:
            if characters['uuid'] == agents['ItemID']:
                MainList.append(characters['displayName'])
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
