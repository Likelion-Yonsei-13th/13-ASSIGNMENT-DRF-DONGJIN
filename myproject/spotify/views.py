from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .utils import get_spotify_access_token

class ArtistSearchView(APIView):
    def get(self, request):
        artist_name = request.query_params.get('name')
        if not artist_name:
            return Response({"error": "쿼리 파라미터에 'name'이 필요합니다."}, status=400)
        
        token = get_spotify_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": artist_name, "type": "artist", "limit": 1}

        response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
        data = response.json()

        if "artists" not in data or not data["artists"]["items"]:
            return Response({"error": "아티스트를 찾을 수 없습니다."}, status=404)
        
        artist = data["artists"]["items"][0]
        return Response({
            "name": artist["name"],
            "genres": artist["genres"], 
            "followers": artist["followers"]["total"],
            "image_url": artist["external_urls"]["spotify"]
        })