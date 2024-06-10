from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
import requests
import json

def auth_fedex():
    try:
        #Input Data
        data={
            'grant_type': 'client_credentials',
            'client_id':config('FEDEX_API_KEY'),
            'client_secret':config('FEDEX_SECRET_KEY')
        }
        #Heder
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
            }
        #make API Call
        response=response = requests.post(f"{config('FEDEX_BASE_API_URL')}/oauth/token", data=data, headers=headers)
        return response.json()
    except Exception as e:
        print('Error authenticating with FedEx API:',e)
        raise ValueError('Failed to authenticate with FedEx API')
    
class FedexTrackingView(APIView):
    def get(self,req):
        authRes=auth_fedex()
        # Input Data 
        data=json.dumps({
            'includeDetailedScans':True,
            'trackingInfo':[
                {
                    'trackingNmberInfo':{
                        'trackingNumber':122816215025810
                    }
                }
            ]
        })
        headers={
            'Content-Type':'application/json',
            'X-locale':'en_US',
            'Authorization':'Bearer'+authRes["access_token"]


        }
        #make API Call
        response = requests.post(f"{config('FEDEX_BASE_API_URL')}/track/v1/trackingnumbers", data=data, headers=headers)

        if response.status_code ==200:

            return Response({"Tracking Details":response.text})
        
        else:
            return Response({'error':'Failed to featch tracking information '},status=response.status_code)
