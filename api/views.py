from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from rest_framework.permissions import AllowAny
import requests
import os
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml



class GetAddressDetails(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetAddressSerializer
    '''To get latitude and longitude of the given address'''

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            address = data.get('address').replace(" ", "+")[2:]
            output_format = data.get('output_format')
            key = os.environ.get('google_map_api')
            url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}'
            try:
                r = requests.get(url=url)
                response = r.json()
                api_status = response.get('status')
                if not api_status:
                    payload = {
                        'message': "We Couldn't Fetch Address Details From Google APIs.Try Again Later",
                        'status': False
                    }
                else:
                    if  output_format =='json':
                        payload = {
                            "coordinates": response.get('results')[0].get('geometry').get('location'),
                            "address": response.get('results')[0].get('formatted_address')
                        }
                    else:
                        """output_format = 'xml' case"""
                        """converting dict to xml format"""
                        data = {
                            "address": response.get('results')[0].get('formatted_address'),
                            "coordinates": response.get('results')[0].get('geometry').get('location')
                        }
                        xml = dicttoxml(data, attr_type=False)
                        payload = parseString(xml).toprettyxml()
            except Exception:
                payload = {
                    'message': "We Couldn't Fetch Address Details From Google APIs.Try Again Later",
                    'status': False
                }
        else:
            payload = {
                "status": False,
                "message": serializer.errors,
            }
        return Response(payload, status=status.HTTP_200_OK)
