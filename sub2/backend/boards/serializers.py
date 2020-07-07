from rest_framework import serializers
from .models import Board,Reply

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','board_writer','board_subject','board_update_date','board_content',
        ]

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id','board','reply_writer','reply_content','reply_write_date','reply_update_date'
        ]
