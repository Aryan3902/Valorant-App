# from typing_extensions import Required
# from aiohttp.client import request
# from django.http.response import HttpResponse
import requests
# from django.contrib import auth
from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from .name import main
# from .auth import run
# Create your views here.
CompetitiveTier = requests.get(
            "https://valorant-api.com/v1/competitivetiers").json()
maps = requests.get('https://valorant-api.com/v1/maps').json()['data']

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
        # agent_pic = requests.get(
        # 'https://valorant-api.com/v1/agents').json()['data']
        matchDetails = requests.get(f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/ap/{puuid}').json()
        # Qskills = requests.get(
        #     f'https://pd.ap.a.pvp.net/mmr/v1/players/{puuid}', headers=headers).json()
        # Qskills = Qskills['QueueSkills']
        
        # competitiveupdate = requests.get(
        #     f'https://pd.ap.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates?startIndex=0&endIndex=15&queue=competitive', headers=headers).json()['Matches']
        
        # gamemodes = requests.get(
        # 'https://valorant-api.com/v1/gamemodes', headers=headers).json()['data']
        
        request.session['matchDetails'] = matchDetails
        
        # request.session['competitveupdate'] = competitiveupdate
        
        # request.session['Qskills'] = Qskills
        # request.session['gamemodes'] = gamemodes
        request.session['headers'] = headers
        request.session['puuid'] = puuid        
        # request.session['agentPic'] = agent_pic
        return redirect('/home/')
    else:
        return render(request, 'API/login.html')


def home(request):
    matchDetails = request.session['matchDetails']
    
    # competitiveupdate = request.session['competitveupdate'] 
    # gamemodes = request.session['gamemodes']
    headers = request.session['headers']
    puuid = request.session['puuid']
    # agent_pic = request.session['agentPic'] 
    # Qskills = request.session['Qskills']
    # details = requests.get(
    #     f'https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/ap/{puuid}').json()['data']
    # print(details)
    # gameUsername = details['name']
    # tagLine = details['tag']
    
    
    
    # gamemodes[0]['displayName'] = 'Unrated'

    # username = gameUsername
    
    # rrupdate = competitiveupdate[0]['RankedRatingEarned']
    # kills = 0
    # deaths = 0
    # id = []
    # for ids in matchDetails:
    #     id.append(ids['MatchID'])
    # for matches in range(20):
    #     match_info = requests.get('https://pd.ap.a.pvp.net/match-details/v1/matches/{}'.format(
    #         id[matches]), headers=headers).json()['players']
    #     for player in match_info:
    #         if player['gameName'] == username:
    #             kills = kills + player['stats']['kills']
    #             deaths = deaths + player['stats']['deaths']
    # kd = round(kills/deaths, 2)
    # Seasoninfo = Qskills['competitive']['SeasonalInfoBySeasonID']
    # for i in Seasoninfo:
    #     Seasonid = i
    #     break
    # unrated = Qskills['unrated']['SeasonalInfoBySeasonID'][Seasonid]
    # urwins = unrated['NumberOfWinsWithPlacements']
    # urtotal = unrated["NumberOfGames"]
    # urloss = urtotal - urwins
    # winpur = round(urwins*100/urtotal, 2)

    # spikerush = Qskills['spikerush']['SeasonalInfoBySeasonID'][Seasonid]
    # srwins = spikerush['NumberOfWinsWithPlacements']
    # srtotal = spikerush["NumberOfGames"]
    # srloss = srtotal - srwins
    # winpsr = round(srwins*100/srtotal, 2)

    # compwins = Seasoninfo[Seasonid]['NumberOfWinsWithPlacements']
    # comptotal = Seasoninfo[Seasonid]["NumberOfGames"]
    # comploss = comptotal-compwins
    # rr = Seasoninfo[Seasonid]["RankedRating"]
    # winpcomp = round(compwins*100/comptotal, 2)

    # custom = Qskills['custom']['SeasonalInfoBySeasonID'][Seasonid]
    # cuwins = custom['NumberOfWinsWithPlacements']
    # cutotal = custom["NumberOfGames"]
    # culoss = cutotal - cuwins
    # winpcu = round(cuwins*100/cutotal, 2)

    # rank = []
    # rank.append(Seasoninfo[Seasonid]['Rank'])
    # rankdetails = CompetitiveTier['data'][0]['tiers'][rank]

    userparty = {}
    partyDetails = []

    # lastmatch = requests.get(
    #     'https://pd.ap.a.pvp.net/match-details/v1/matches/{}'.format(matchDetails[0]['MatchID']), headers=headers).json()
    lastmatch = matchDetails['data'][0]
    # match_details = lastmatch['matchInfo']
    # timeplayed_sec = (match_details['gameLengthMillis']/1000) % 60
    # timeplayed_min = match_details['gameLengthMillis']/60000
    players = lastmatch['players']
    for user in players['all_players']:
        if user['puuid'] == puuid:
            username = user['name']
            teamid = user['team']
            tagLine = user['tag']
            agent_lastpic = user['assets']['agent']['small']
            killcount = user['stats']['kills']
            deathcount = user['stats']['deaths']
            assistscount = user['stats']['assists']
            PlayerTitle = user['player_title']
            Card = user['assets']['card']['large']
            userLevel = user['level']
            break

    MMRdata = requests.get(f"https://api.henrikdev.xyz/valorant/v2/mmr/ap/{username}/{tagLine}").json()['data']
    MMRcurrent = MMRdata['current_data']
    rank = MMRcurrent['currenttier']
    rrupdate = MMRcurrent['mmr_change_to_last_game']
    rr = MMRcurrent['ranking_in_tier']
    last = MMRdata["by_season"]
    first = last['e3a2']
    second = last['e3a1']
    third = last['e2a3']
    rankdetails = CompetitiveTier['data'][0]['tiers']
    presentRank = rankdetails[rank]
    try:
        lastRank = rankdetails[first["final_rank"]]
    except:
        lastRank = None
    try:
        secondRank = rankdetails[second["final_rank"]]
    except:
        lastRank = None
    try:
        thirdRank = rankdetails[third["final_rank"]]
    except:
        lastRank = None
    
    

    titles = requests.get(
        'https://valorant-api.com/v1/playertitles').json()['data']
    # cards = requests.get(
    #     'https://valorant-api.com/v1/playercards',).json()['data']

    Allmaps =  {
        "Split":"https://media.valorant-api.com/maps/d960549e-485c-e861-8d71-aa9d1aed12a2/listviewicon.png",
        "Fracture":"https://media.valorant-api.com/maps/b529448b-4d60-346e-e89e-00a4c527a405/listviewicon.png",
        "Ascent":"https://media.valorant-api.com/maps/7eaecc1b-4337-bbf6-6ab9-04b8f06b3319/listviewicon.png",
        "Bind":"https://media.valorant-api.com/maps/2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba/listviewicon.png",
        "Breeze":"https://media.valorant-api.com/maps/2fb9a4fd-47b8-4e7d-a969-74b4046ebd53/listviewicon.png",
        "Icebox":"https://media.valorant-api.com/maps/e2ad5c54-4114-a870-9641-8ea21279579a/listviewicon.png",
        "Haven": "https://media.valorant-api.com/maps/2bee0dc9-4ffe-519b-1cbd-7fbe763a6047/listviewicon.png"
    }
    
    

    for title in titles:
        if title['uuid'] == PlayerTitle:
            Title = title['titleText']
    # for agents in agent_pic:
    #     if agent_lastid == agents['uuid']:
    #         agent_lastpic = agents['displayIconSmall']
    matchresult = lastmatch['teams'][teamid.lower()]
    if matchresult['has_won']:
        result = 'Victory'
    else:
        result = 'Defeat'
    roundsWon = matchresult['rounds_won']
    roundsLost = matchresult['rounds_lost']
    # for teams in matchresult:
    #     if teams['teamId'] == teamid:
    #         if teams['won']:
    #             result = 'Victory'
    #         else:
    #             result = 'Defeat'
    #         roundsWon = teams['roundsWon']
    #         roundsPlayed = teams['roundsPlayed']
    #         roundsLost = abs(roundsPlayed-roundsWon)
    Lastgamemode = lastmatch['metadata']['mode']
    # if gamemode == 'ggteam':
    #     gamemode = 'Escalation'
    # if gamemode == 'onefa':
    #     gamemode == 'Replication'
    # for mapId in maps:
    #     if mapId['mapUrl'] == match_details['mapId']:
    #         mapname = mapId['displayName']
    #         mappic = mapId['listViewIcon']
    mapname = lastmatch['metadata']['map']
    mappic = Allmaps[mapname]
    gamemode = {
        'Unrated':"https://media.valorant-api.com/gamemodes/96bd3920-4f36-d026-2b28-c683eb0bcac5/displayicon.png",
        "Deathmatch":"https://media.valorant-api.com/gamemodes/a8790ec5-4237-f2f0-e93b-08a8e89865b2/displayicon.png",
        "Escalation":"https://media.valorant-api.com/gamemodes/a4ed6518-4741-6dcb-35bd-f884aecdc859/displayicon.png",
        "Replication":"https://media.valorant-api.com/gamemodes/4744698a-4513-dc96-9c22-a9aa437e4a58/displayicon.png",
        "Spike Rush":"https://media.valorant-api.com/gamemodes/e921d1e6-416b-c31f-1291-74930c330b7b/displayicon.png",
        "Snowball Fight":"https://media.valorant-api.com/gamemodes/57038d6d-49b1-3a74-c5ef-3395d9f23a97/displayicon.png",
        "Competitive":presentRank['smallIcon'],
        "Custom":'https://inceptum-stor.icons8.com/s2he3DWV4kZd/valorant%20icon.png'
    }
    gamemodeIcon = gamemode[Lastgamemode]
    # for mode in gamemodes:
    #     if mode['displayName'].upper() == gamemode.upper():
    #         gamemodeIcon = mode['displayIcon']
    #         break
    #     if gamemode == "competitive":
    #         gamemodeIcon = rankdetails['smallIcon']
    #         break
    #     else:
    #         gamemodeIcon = 'https://inceptum-stor.icons8.com/s2he3DWV4kZd/valorant%20icon.png'
    #         gamemode = 'Custom'
    # i = 0
    for user in players[teamid.lower()]:

        # if user['name'] == username:
        #     continue
        userparty = {}
        agent = user['assets']['agent']['small']
        card = user['assets']['card']['wide']
        # card = requests.get(cardurl).json()['data']['wideArt']
        # agent = requests.get(agenturl).json()['data']['displayIcon']
        userparty['name'] = user['name']
        userparty['tag'] = user['tag']
        userparty['kills'] = user['stats']['kills']
        userparty['deaths'] = user['stats']['deaths']
        userparty['assists'] = user['stats']['assists']
        userparty['cardurl'] = card
        userparty['agenturl'] = agent

        partyDetails.append(userparty)
            # i = i+1
            # if gamemode == 'Custom':
            #     if i == 4:
            #         break

    return render(request, 'API/home.html', {'level': userLevel,  'username': username,"lastRank":lastRank,"secondRank":secondRank,"thirdRank": thirdRank,
                                             'tag': tagLine, 'card': Card, 'title': Title, 'rank': presentRank, 'rr': rr, 'rrchange': rrupdate,
                                             'mapname': mapname, 'mappic': mappic, 'result': result.upper(), 'agentpic': agent_lastpic, 'icon': gamemodeIcon,
                                             'won': roundsWon, 'lost': roundsLost, 'killcount': killcount, 'deathcount': deathcount, 'assistscount': assistscount,
                                             'party': partyDetails,'gamemode':Lastgamemode})


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
