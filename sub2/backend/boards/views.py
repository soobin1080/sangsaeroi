from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Board,Reply
from .serializers import BoardSerializer,ReplySerializer

# Create your views here.

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class=BoardSerializer

    def get_queryset(self):
        return Board.objects.all().order_by("-board_write_date")

    def perform_create(self,serializer):
        serializer.save()


class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class=ReplySerializer

    def get_queryset(self):
        return Reply.objects.all().order_by("-reply_write_date")

    def perform_create(self,serializer):
        serializer.save()
