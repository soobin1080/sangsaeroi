from django.urls import path
from .views import BoardViewSet,ReplyViewSet

board_list=BoardViewSet.as_view({"get":"list","post":"create"})
board_detail=BoardViewSet.as_view({"get":"retrieve","patch":"partial_update","delete":"destroy"})

reply_list=ReplyViewSet.as_view({"get":"list","post":"create"})
reply_detail=ReplyViewSet.as_view({"get":"retrieve","patch":"partial_update","delete":"destroy"})

urlpatterns = [
    path("board/",board_list,name="board-list"),
    path("board/<int:pk>",board_detail,name="board-detail"),
    
    path("reply/",reply_list,name="reply-list"),
    path("reply/<int:pk>",reply_detail,name="reply-detail"),
] 