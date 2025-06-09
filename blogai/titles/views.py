from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .title_generator import generate_titles

class TitleSuggestionView(APIView):
    def post(self, request):
        content = request.data.get("content", "")
        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        titles = generate_titles(content)
        return Response({"suggestions": titles})
