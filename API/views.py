from aiohttp.client import request
from django.http.response import HttpResponse
import requests
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .name import main
from .auth import run
# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        params = (
        ('username', username),
        ('password', password),
        )

        headers = requests.get('https://valo.saumay.dev/auth/login', params=params).json()
        puuid = headers['puuid']
        agent_pic = requests.get(
        'https://valorant-api.com/v1/agents').json()['data']
        match = requests.get(
        'https://pd.ap.a.pvp.net/match-history/v1/history/{}?startIndex=0&endIndex=20'.format(puuid), headers=headers).json()['History']
        Qskills = requests.get(
            f'https://pd.ap.a.pvp.net/mmr/v1/players/{puuid}', headers=headers).json()
        Qskills = Qskills['QueueSkills']
        CompetitiveTier = requests.get(
            "https://valorant-api.com/v1/competitivetiers").json()
        competitiveupdate = requests.get(
            f'https://pd.ap.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates?startIndex=0&endIndex=15&queue=competitive', headers=headers).json()['Matches']
        maps = requests.get('https://valorant-api.com/v1/maps').json()['data']
        gamemodes = requests.get(
        'https://valorant-api.com/v1/gamemodes', headers=headers).json()['data']
        
        request.session['match'] = match
        request.session['CompetitiveTier'] = CompetitiveTier
        request.session['competitveupdate'] = competitiveupdate
        request.session['maps'] = maps
        request.session['Qskills'] = Qskills
        request.session['gamemodes'] = gamemodes
        request.session['headers'] = headers
        request.session['puuid'] = puuid        
        request.session['agentPic'] = agent_pic
        return redirect('/home/')
    else:
        return render(request, 'API/login.html')


def home(request):
    match = request.session['match']
    CompetitiveTier = request.session['CompetitiveTier'] 
    competitiveupdate = request.session['competitveupdate'] 
    maps = request.session['maps']
    gamemodes = request.session['gamemodes']
    headers = request.session['headers']
    puuid = request.session['puuid']
    agent_pic = request.session['agentPic'] 
    Qskills = request.session['Qskills']
    details = requests.get(
        f'https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/ap/{puuid}').json()['data']
    gameUsername = details['name']
    tagLine = details['tag']
    
    
    
    gamemodes[0]['displayName'] = 'Unrated'

    username = gameUsername
    progress = requests.get(
        'https://pd.ap.a.pvp.net/account-xp/v1/players/{}'.format(puuid), headers=headers).json()['Progress']
    rrupdate = competitiveupdate[0]['RankedRatingEarned']
    # kills = 0
    # deaths = 0
    id = []
    for ids in match:
        id.append(ids['MatchID'])
    # for matches in range(20):
    #     match_info = requests.get('https://pd.ap.a.pvp.net/match-details/v1/matches/{}'.format(
    #         id[matches]), headers=headers).json()['players']
    #     for player in match_info:
    #         if player['gameName'] == username:
    #             kills = kills + player['stats']['kills']
    #             deaths = deaths + player['stats']['deaths']
    # kd = round(kills/deaths, 2)
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
            i = i+1
            if gamemode == 'Custom':
                if i == 4:
                    break

    return render(request, 'API/home.html', {'level': progress['Level'], 'xp': progress['XP'], 'username': username,
                                             'tag': tagLine, 'card': Card, 'title': Title, 'rank': rankdetails, 'compwins': compwins, 'comptotal': comptotal, 'comploss': comploss,
                                             'winpcomp': winpcomp, 'rr': rr, 'urwins': urwins, 'urtotal': urtotal, 'urloss': urloss, 'winpur': winpur,
                                             'srwins': srwins, 'srtotal': srtotal, 'srloss': srloss, 'winpsr': winpsr,
                                             'cuwins': cuwins, 'cutotal': cutotal, 'culoss': culoss, 'winpcu': winpcu, 'rrchange': rrupdate,
                                             'sec': int(timeplayed_sec), 'min': int(timeplayed_min), 'gamemode': gamemode.upper(),
                                             'mapname': mapname, 'mappic': mappic, 'result': result.upper(), 'agentpic': agent_lastpic, 'icon': gamemodeIcon,
                                             'won': roundsWon, 'lost': roundsLost, 'aryan': mode['displayName'], 'killcount': killcount, 'deathcount': deathcount, 'assistscount': assistscount, 'scorecount': scorecount,
                                             'party': partyDetails})


def store(request):
    headers = request.session['headers']
    puuid = request.session['puuid']
    store = requests.get(
        f'https://pd.ap.a.pvp.net/store/v2/storefront/{puuid}', headers=headers).json()
    single_skin = store['SkinsPanelLayout']['SingleItemOffers']
    store = []
    for skin in single_skin:
        skins = f'https://media.valorant-api.com/weaponskinlevels/{skin}/displayicon.png'
        store.append(skins)
    return render(request, 'API/store.html', {'store': store})




def collection(request):
    headers = request.session['headers']
    puuid = request.session['puuid']

    loadout = requests.get(
        f'https://pd.ap.a.pvp.net/personalization/v2/players/{puuid}/playerloadout', headers=headers).json()['Guns']
    weapons = requests.get(
        "https://valorant-api.com/v1/weapons").json()['data']
    skins = []

    for owned in loadout:
        for gun in weapons:
            collect = {}
            collect['Name'] = gun['displayName']
            # if owned['ID'] == gun['uuid']:
            for skin in gun['skins']:
                if owned['SkinID'] == skin['uuid']:
                    collect['skin'] = skin['chromas'][0]['fullRender']
                    # if skin['displayName'][:8] == 'Standard':
                    #     collect['skin'] = skin['chromas'][0]['fullRender']
                    # else:
                    #     collect['skin'] = skin['displayIcon']
                    skins.append(collect)
            for items in skins:
                if items['Name'] == "Classic":
                    Classic = items
                if items['Name'] == "Shorty":
                    Shorty = items
                if items['Name'] == "Frenzy":
                    Frenzy = items
                if items['Name'] == "Ghost":
                    Ghost = items
                if items['Name'] == "Sheriff":
                    Sheriff = items
                if items['Name'] == "Stinger":
                    Stinger = items
                if items['Name'] == "Spectre":
                    Spectre = items
                if items['Name'] == "Bucky":
                    Bucky = items
                if items['Name'] == "Judge":
                    Judge = items
                if items['Name'] == "Bulldog":
                    Bulldog = items
                if items['Name'] == "Guardian":
                    Guardian = items
                if items['Name'] == "Phantom":
                    Phantom = items
                if items['Name'] == "Vandal":
                    Vandal = items
                if items['Name'] == "Marshal":
                    Marshal = items
                if items['Name'] == "Operator":
                    Operator = items
                if items['Name'] == "Ares":
                    Ares = items
                if items['Name'] == "Odin":
                    Odin = items
                if items['Name'] == "Melee":
                    Melee = items
    print(Ghost)
    return render(request, 'API/collection.html', {'Classic': Classic, 'Shorty': Shorty, 'Frenzy': Frenzy, 'Ghost': Ghost, 'Sheriff': Sheriff, 'Stinger': Stinger,
                                                   'Spectre': Spectre, 'Bucky': Bucky, 'Judge': Judge, 'Bulldog': Bulldog, 'Guardian': Guardian, 'Phantom': Phantom, 'Vandal': Vandal, 'Marshal': Marshal, 'Operator': Operator, 'Odin': Odin,
                                                   'Melee': Melee, 'Ares': Ares})


def agents(request):
    headers = request.session['headers']
    puuid = request.session['puuid']
    agent_pic = request.session['agentPic'] 
    all = requests.get(
    'https://valorant-api.com/v1/agents?isPlayableCharacter=true').json()['data']
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
