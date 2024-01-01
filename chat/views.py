from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Chat, Message 
from django.http import JsonResponse
import json # dùng thư viện để xử lý json từ bên client gửi đến


import openai

openai_api_key = "API"
openai.api_key = openai_api_key


def ask_openai(message):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response.choices[0].text.strip()
    return answer


def home_page(request):
    return render(request, 'chat/home.html')


@login_required(login_url='/login/')
def chat_page(request):
    return render(request, 'chat/chat.html')


@login_required(login_url='/login/')
def load_chats(request):
    chats = list(Chat.objects.filter(user=request.user).values())
    chats = chats[::-1]
    return JsonResponse({'chats': chats}, status=200)


@login_required(login_url='/login/')
def create_chat(request):
    chat = Chat.objects.create(user=request.user ,name='')
    chat.save()
    return JsonResponse({'message': 'Chat Created Successfully!', 'chat_id': chat.id}, status=200)


@login_required(login_url='/login/')
def retrive_chat(request, pk):
    if request.method == 'POST':
        # lấy chat
        chat = Chat.objects.get(user=request.user, pk=pk)
        messages = chat.get_messages()
        print(messages)
        # lấy tất cả các message thuộc về chat
        # trả về và cập nhật giao diện
        serialized_messages = []
        for message in messages:
            serialized_message = {
                'id': message.id,
                'question': message.question,
                'answer': message.answer,
                'created_at': message.created_at
            }
            serialized_messages.append(serialized_message)

        return JsonResponse({'message': 'Get chat successfully!', 'messages': serialized_messages}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method!'}, status=400)


@login_required(login_url='/login/')
def chat_message_view(request, chat_id=None):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data) # data chính là request.body lấy được từ client, chính là message
        # answer = "Chatbot đưa ra câu trả lời cho bạn!!!"
        answer = ask_openai(data)
        # print(answer, type(answer))
        if chat_id:
            # xử lý khi gửi dữ liệu tại chat đã tạo
            chat = Chat.objects.get(user=request.user, pk=chat_id)

            if chat.name == '':
                chat.name = data[:30]
                chat.save()

            message = Message.objects.create(chat=chat, question=data, answer=answer)
            return JsonResponse({'message': 'Message created successfully!', 'chat_id': chat.id, 'answer_question': answer}, status=201)
        else:
            # xử lý khi chưa tạo chat
            chat = Chat.objects.create(user=request.user, name=data[:30])  # chỉ lấy 30 ký tự đầu là name
            message = Message.objects.create(chat=chat, question=data, answer=answer)
            return JsonResponse({'message': 'Chat and Message created successfully!', 'chat_id': chat.id, 'answer_question': answer}, status=201)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)


@login_required(login_url='/login/')
def delete_chat(request, pk):
    chat = Chat.objects.get(user=request.user, pk=pk)
    if request.method == 'POST':
        if chat:
            chat.delete()
            return JsonResponse({'message': 'Chat Deleted Successfully!!'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid Chat!!!'})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat')
        else:
            messages.error(request, "Invalid Email Or Password!!!")
            return redirect('login')
    return render(request, 'chat/login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm-password']

        if password1 == password2:
            # kiểm tra user đã tồn tại hay chưa?
            if User.objects.filter(username=username).exists():
                messages.info(request, "Email has already existed!!!")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('chat')
        else:
            messages.error(request, "Password does not match!!!")
            return redirect('register')
    else:
        return render(request, 'chat/register.html')


@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return redirect('home')
