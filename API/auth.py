import re
import aiohttp
import asyncio


async def auth(username, password):
    async with aiohttp.ClientSession() as s:
        data = {
            'client_id': 'play-valorant-web-prod',
            'nonce': '1',
            'redirect_uri': 'https://playvalorant.com/opt_in',
            'response_type': 'token id_token',
        }

        await s.post('https://auth.riotgames.com/api/v1/authorization', json=data)

        data = {
            'type': 'auth',
            'username': username,
            'password': password
        }

        async with s.put('https://auth.riotgames.com/api/v1/authorization', json=data) as response:
            response = await response.json()
            print("rcvd 2nd req")

        pattern = re.compile(
            'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        acces_data = pattern.findall(
            response['response']['parameters']['uri'])[0]

        async with s.post('https://entitlements.auth.riotgames.com/api/token/v1',
                          headers={'Authorization': f'Bearer {acces_data[0]}'}, json={}) as response:
            response = await response.json()

        entitlements_token = response["entitlements_token"]

        headers = {
            'Authorization': f"Bearer {acces_data[0]}",
            'X-Riot-Entitlements-JWT': entitlements_token,
            'X-Riot-ClientPlatform': "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
            'X-Riot-ClientVersion': "release-03.04-shipping-15-598547"
        }
        return headers


def run(username, password):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    headers = loop.run_until_complete(auth(username, password))
    return headers
    loop.close()
