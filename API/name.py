import re
import aiohttp
import asyncio
import json


async def autho(username, password):
    session = aiohttp.ClientSession()
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()
    pattern = re.compile(
        'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    access_token = data[0]
    id_token = data[1]
    expires_in = data[2]

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    user_id = data['sub']
    print('User ID: ' + user_id)

    await session.close()

    return user_id


def main(username, password):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    headers = loop.run_until_complete(autho(username, password))
    return headers
    loop.close()
