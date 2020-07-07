from django.db import models
from django.utils import timezone
from accounts.models import User
from django.conf import settings

# Create your models here.

class Board(models.Model):
    board_writer=models.CharField(max_length=30,blank=False)
    board_subject=models.CharField(max_length=50,blank=False)
    board_content=models.TextField()
    board_write_date=models.DateTimeField(auto_now_add=True)
    board_update_date=models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Reply(models.Model):
    board=models.ForeignKey(Board,on_delete=models.CASCADE)
    reply_writer=models.CharField(max_length=30,blank=False)
    reply_content=models.CharField(max_length=200,blank=False)
    reply_write_date=models.DateTimeField(auto_now_add=True)
    reply_update_date=models.DateTimeField(auto_now=True)
    objects = models.Manager()