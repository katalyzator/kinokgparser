# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render
import requests

BASE_URL = 'http://kino.kg/'


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

    return film_names


def get_time_of_film(cinema_name, film_name, day):
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
    next_td = ''
    for i in td:
        if i.a != None:
            if i.a.text == film_name:
                next_td = i

    time_table = next_td.next_sibling.next_sibling.next_element.next_element
    trow = time_table.find_all('tr', {'align': 'center'})[1:]

    list_json = []

    for j in trow:
        list_json.append(j.find('td').text[10:16])

    return list_json


def get_film_detail(film_name, cinema_name, day):
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
    film_link = ''
    for i in td:
        if i.a != None:
            if i.a.text == film_name:
                film_link = i.find('a', href=True)['href']

    film_soup = BeautifulSoup(get_html('http://kino.kg' + film_link), 'html.parser')
    detail_div = film_soup.find('div', class_='movie_detail')
    all_div = detail_div.find_all('div')

    production = ''
    director = ''
    actors = ''
    duration = ''
    genre = ''
    description = detail_div.find('br').next_sibling.text
    for i in all_div:
        if i.find('strong') != None:

            if i.find('strong').text == "Производство:":
                production = i.find('strong').find_parent('div').text

            if i.find('strong').text == "Режиссер:":
                director = i.find('strong').find_parent('div').text

            if i.find('strong').text == "Актеры:":
                actors = i.find('strong').find_parent('div').text

            if i.find('strong').text == "Продолжительность:":
                duration = i.find('strong').find_parent('div').text

            if i.find('strong').text == "Жанр:":
                genre = i.find('strong').find_parent('div').text


    movie_detail = {
        "production": production,
        "director": director,
        "actors": actors,
        "duration": duration,
        "genre": genre,
        "description": description,
    }

    return movie_detail


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    main_div_soup = soup.find('div', class_='menu_items')
    sub_div = main_div_soup.find_all('div', class_='menu_item')

    cinema_name_json = [{
        'cinema_name': i.a.text,
        'films': [{
            "today": [{
                "name": today,
                "times": [{
                    "time": time
                } for time in get_time_of_film(i.a.text, today, "Today")],
                "movie_detail": [get_film_detail(today, i.a.text, "Today")],
            } for today in get_today_film(i.a.text, 'Today')],
            # "tomorrow": [{
            #     "name": tomorrow
            # } for tomorrow in get_today_film(i.a.text, 'Tomorrow')],
            # "aftertomorrow": [{
            #     "name": aftertomorrow
            # } for aftertomorrow in get_today_film(i.a.text, 'AfterTomorrow')],
        }]

    } for i in sub_div]

    return cinema_name_json


def main(request):
    objects = parse(get_html(BASE_URL))
    print objects

    return JsonResponse(dict(data=objects))
