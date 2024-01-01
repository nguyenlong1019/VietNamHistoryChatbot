from django.urls import path
from .views import (
    home_page,
    chat_page,
    login_page,
    register_page,
    logout_page,
    create_chat,
    retrive_chat,
    delete_chat,
    load_chats,
    chat_message_view
)


urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('chat/', chat_page, name='chat'),
    path('logout/', logout_page, name='logout'),
    path('chat/load/', load_chats, name='load-chats'),
    path('chat/create/', create_chat, name='create-chat'),
    path('chat/retrive/<int:pk>/', retrive_chat, name='retrive-chat'),
    path('chat/delete/<int:pk>/', delete_chat, name='delete-chat'),
    path('api/chat/create/', chat_message_view, name='create-chat-and-message'),
    path('api/chat/<int:chat_id>/add-message/', chat_message_view, name='add-message-chat')
]