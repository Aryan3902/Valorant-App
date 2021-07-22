from django.shortcuts import render
import requests
import django.contrib.staticfiles
from django.http import response
# Create your views here.


def home(request):

    headers = {
        'Authorization': 'Bearer eyJraWQiOiJzMSIsInR5cCI6ImF0K2p3dCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyNjA1N2Q3ZS1iNTI3LTUzNTAtYTFhYy1lNmM1YmJlOTI4OGYiLCJzY3AiOlsib3BlbmlkIl0sImNsbSI6WyJvcGVuaWQiXSwiZGF0Ijp7ImxpZCI6IndWQnBrNHRTSjYyTlhlbEo2SF9ieGciLCJjIjoidWUxIn0sImlzcyI6Imh0dHBzOlwvXC9hdXRoLnJpb3RnYW1lcy5jb20iLCJleHAiOjE2MjY5Njg1MzMsImlhdCI6MTYyNjk2NDkzMywianRpIjoieGJjSnhvSEdKR0kiLCJjaWQiOiJwbGF5LXZhbG9yYW50LXdlYi1wcm9kIn0.ctUc9r61FdONr3aAgnMP5q7G9LEnCikSQjkSyeOh3kOZk2nhLvgQXn2XF0JA8fPJ46fPTyRzAony7tOTMwawBeUZYJyIU7lI8-tUqPOyHF20zaV6Gi93HuF2oi1hcqCnXCy9knUMeM_gpuGzZ6Ho1qJXs5s-umCUFM4R2-yBXS0',
        'X-Riot-Entitlements-JWT': 'eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoiUDdaZ2ZiNEJSSEpGX3BVZkxoRWhPUSIsInN1YiI6IjI2MDU3ZDdlLWI1MjctNTM1MC1hMWFjLWU2YzViYmU5Mjg4ZiIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNjI2OTY0OTM0LCJqdGkiOiJ4YmNKeG9IR0pHSSJ9.cygNJtUI5ATcmML0FZqoA5UFSLdlW6RC-kRR0-XKKiLBwURlAA-53VzvzCO7QxfIVBJV7GrpMH6hy8M8iG4PeH118kYQPbOLrgA9L5-1rMGqY4aMCnEZqtz7ZdGk21bn2TcpNhhdx1NXM-QlZA_8h6BX7SlCkvKigiQcDpwh_5i_e1Ma-OWI_K38MTqNlJF9ecOhKco2TkFFiBWj0xuHcn9o6W4Eg5zLfRzP97Z5PUoMTOH-h-Sd5hXk_o192X3X2MJcxg91eHda2CgiRTtJPnde1aYaIretpQMRoxLFfsk_UdVg0KOMp0yUQSTEuggEjRSyelu80nA0wpr-1f4Axg',
    }

    response = requests.get(
        'https://pd.ap.a.pvp.net/account-xp/v1/players/26057d7e-b527-5350-a1ac-e6c5bbe9288f', headers=headers).json()
    list1 = []
    list1.append(response['Progress'])
    return render(request, 'API/home.html', {'response': list1[0]})
