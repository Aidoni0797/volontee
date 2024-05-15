from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import AuthUserForm, RegUserForm, AddCard, ConnectionWithVolonteer, GetToken
from .models import Player, Card, CardGame, Deck
from .suu import result_sum, result_summ
from django.core.cache import cache
import requests

def index(request):
    form = ConnectionWithVolonteer()
    return render(
        request,
        'common/index.html',
        context={
            'form': form
        }
    )

def setting(request):
    form = GetToken()
    return render(
        request,
        'common/service.html',
        context={
            'form': form
        }
    )

def login_player(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(
                reverse('game:show_game', kwargs={'id': request.user.id})
            )
        else:
            return render(
                request,
                'common/player.html',
                {
                    'form': AuthUserForm(),
                    'message': 'Such user does not exist.'
                }
            )
    return render(
        request,
        'common/player.html',
        {
            'form': AuthUserForm()
        }
    )


def show_game(request, id):
    try:
        playerr, created = Player.objects.get_or_create(
            user_id=request.user.id,
            defaults={'user': request.POST.get('username'), 'first_name': str(request.user.username)}
        )
        playerr.save()
        deck = Deck.objects.create()
        for card in Card.objects.all():
            deck.cards.add(card)
        game, created = CardGame.objects.get_or_create(user=playerr, deck=deck)
        xx = game.hit()
        game.save()
        data = {"first_card_player_suits": xx[0], "first_card_player_ranks": xx[1],
                "second_card_player_suits": xx[2], "second_card_player_ranks": xx[3],
                "total_player": result_sum(xx[1], xx[3]),
                "first_card_dealer_suits": xx[4], "first_card_dealer_ranks": xx[5],
                "second_card_dealer_suits": xx[6], "second_card_dealer_ranks": xx[7],
                "total_dealer": result_sum(xx[5], xx[7])}
        cache.set('kerek_bolad', data)
        return render(request, "common/game.html", context=data)
    except CardGame.DoesNotExist:
        return render(
            request,
            template_name='exceptions/not_found.html'
        )
    else:
        return render(
            request,
            template_name='common/game.html',
            context={
                # 'game': game
            }
        )


def start_game(request) -> HttpResponse:
        return HttpResponseRedirect(
            reverse('game:login_player')
        )

# которые игрок может взять в блекджеке, зависит от конкретных правил игры, но обычно оно составляет от 4 до 6 карт
def add_card(request):
    form = ConnectionWithVolonteer()
    if request.method == 'POST':
        name1 = request.POST.get('name1')
        tele = request.POST.get('tele')
        number = request.POST.get('number')
        text = request.POST.get('text')
        return render(
            request,
            'common/index.html',
            {
                'form': form
            }
        )

    game = CardGame.objects.first()
    game1 = CardGame.objects.first()
    xx = game.add_hit()
    xx1 = game1.add_hit()
    game.save()
    game1.save
    kerek_bolad = cache.get('kerek_bolad')
    data = kerek_bolad | {"third_card_player_suits": xx[0], "third_card_player_ranks": xx[1], "total_player": result_summ(kerek_bolad['total_player'], xx[1])} | {"third_card_dealer_suits": xx1[0], "third_card_dealer_ranks": xx1[1], "total_dealer": result_summ(kerek_bolad['total_dealer'], xx1[1])}
    return render(request, "common/game.html", context=data)


def connectvolonterr(request) -> HttpResponse:
    form = ConnectionWithVolonteer()
    if request.method == 'POST':
        name1 = request.POST.get('name1')
        tele = request.POST.get('tele')
        number = request.POST.get('number')
        text = request.POST.get('text')
        return render(
                request,
                'common/index.html',
                {
                    'form': form
                }
            )

def register_player(request) -> HttpResponse:
    form = RegUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(
                request,
                'common/register.html',
                {
                    'form': form,
                    'message': 'The entered passwords do not match.'
                }
            )
        User.objects.create_user(username, email=email, password=password1)
        user = authenticate(request, username=username, password=password1)
        login(request, user)
        return HttpResponseRedirect(
            reverse('game:show_game', kwargs={'id': request.user.id})
        )
    else:
        return render(
            request,
            'common/register.html',
            {
                'form': form,
            }
        )



# def contact(request):
#     if request.method == "POST":
#         sender_name = request.POST.get('sender-name',False)
#         sender_number = request.POST.get('sender-number',False)
#         sender_email = request.POST.get('sender-email',False)
#         sender_subject = request.POST.get('sender-subject',False)
#         message = request.POST.get('message',False)
#
#         send_mail (
#             sender_name,
#             sender_number,
#             sender_email,
#             ['aidanadroid100@gmail.com'],
#             sender_subject,
#             message,
#             )
#
#         return render (request,'common/index.html', {'sender_name': 'aidanadroid100@gmail.com'})
#     else:
#         return render (request,'common/index.html', {'sender_name': 'aidanadroid100@gmail.com'})
token = ''
chat_id = ''
def get_token(request):
    form = GetToken()
    if request.method == 'POST':
        global token
        global chat_id
        token = request.POST.get('your_token')
        chat_id = request.POST.get('your_chat_id')
    form = ConnectionWithVolonteer()
    return render(
            request,
            'common/index.html',
            context={
                'form' : form
            }
        )

def contact(request):
    form = ConnectionWithVolonteer()
    if request.method == 'POST':
        name1 = request.POST.get('name')
        tele = request.POST.get('tele')
        number = request.POST.get('number')
        text = request.POST.get('text')
        textt = '\nName: ' + str(name1) + '\nTele: ' + str(tele) + '\nNumber: ' + str(number) + '\nText: ' + str(text)
    else:
        textt = ''

    print(textt)
    #     return render(
    #         request,
    #         'common/index.html',
    #         {
    #             'form': form
    #         }
    #     )
    global token
    global chat_id
    print('Token:', token)
    print('Chat_id:', chat_id)
    # смертельно опасно
    # token = "7028439538:AAE2J60FhhPSpwbnXB4dq1S_hIU9H5vAxfg"
    # chat_id = "1163463444"
    # Ниже ссылка для получение информации о chat_id (не забываем)
    # https://api.telegram.org/bot7028439538:AAE2J60FhhPSpwbnXB4dq1S_hIU9H5vAxfg/getUpdates
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + str(textt)
    results = requests.get(url_req)
    return render(request, 'common/index.html', {'form': form})
    # print(results.json())
#
#
# send_msg("Hello volonteer!")