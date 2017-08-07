# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render
import requests

BASE_URL = 'http://kino.kg/'
ALA_TOO_URL_TODAY = 'http://kino.kg/cinema.asp?cinemaid=105&type=1&day=0#top'
ALA_TOO_URL_TOMORROW = 'http://kino.kg/cinema.asp?cinemaid=105&type=1&day=1#top'


def get_html(url):
    response = requests.get(url)

    return response.text


def get_today_film(cinema_name, day):
    main_soup = BeautifulSoup(get_html(BASE_URL), 'html.parser')

    link = ''
    # item for name
    main_div = main_soup.find('div', class_='menu_items')
    sub_div = main_div.find_all('div', class_='menu_item')
    for name in sub_div:
        if name.a.text == cinema_name:
            link = name.find('a', href=True)['href']

    html = ''

    if day == 'Today':
        html = get_html('http://kino.kg' + link + '&type=1&day=0#top')

    if day == 'Tomorrow':
        html = get_html('http://kino.kg' + link + '&type=1&day=1#top')

    if day == 'AfterTomorrow':
        html = get_html('http://kino.kg' + link + '&type=1&day=2#top')

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('div', class_='detail_content')

    td = table.find_all('td')
    film_names = []
    for i in td:
        if i.a != None:
            film_names.append(i.a.text)
            print i.a.text

    return film_names


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    main_div_soup = soup.find('div', class_='menu_items')
    sub_div = main_div_soup.find_all('div', class_='menu_item')

    cinema_name_json = [{
        'cinema_name': i.a.text,
        'films': [{
            "today": [{
                "name": today
            } for today in get_today_film(i.a.text, 'Today')],
            "tomorrow": [{
                "name": tomorrow
            } for tomorrow in get_today_film(i.a.text, 'Tomorrow')],
            "aftertomorrow": [{
                "name": aftertomorrow
            } for aftertomorrow in get_today_film(i.a.text, 'AfterTomorrow')],
        }]

    } for i in sub_div]

    return cinema_name_json


def main(request):
    objects = parse(get_html(BASE_URL))
    print objects

    return JsonResponse(dict(data=objects))
