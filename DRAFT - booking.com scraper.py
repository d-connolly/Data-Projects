# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 16:47:16 2024

@author: Declan
"""
##DRAFT BOOKING.COM SCRAPER

## Import modules
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup


## OPEN - Code taken from Medium.com
class Hotel:
    raw_html = None
    name = None
    score = None
    price = None
    link = None
    details = None

    def __init__(self, raw_html):
        self.raw_html = raw_html
        self.name = get_hotel_name(raw_html)
        self.score = get_hotel_score(raw_html)
        self.price = get_hotel_price(raw_html)
        self.link = get_hotel_detail_link(raw_html)

    def get_details(self):
        if self.link:
            self.details = HotelDetails(self.link)
            
class HotelDetails:
    latitude = None
    longitude = None

    def __init__(self, details_link):
        detail_page_response = session.get(BOOKING_URL + details_link, headers=REQUEST_HEADER)
        soup_detail = BeautifulSoup(detail_page_response.text, "lxml")
        self.latitude = get_coordinates(soup_detail)[0]
        self.longitude = get_coordinates(soup_detail)[1]


## Amended to remove rating filter
def create_url(people, country, city, date_in, date_out, rooms):
    url = f"https://www.booking.com/searchresults.en-gb.html?selected_currency=GBP&checkin_month={date_in.month}" \
          f"&checkin_monthday={date_in.day}&checkin_year={date_in.year}&checkout_month={date_out.month}" \
          f"&checkout_monthday={date_out.day}&checkout_year={date_out.year}&group_adults={people}" \
          f"&group_children=0&order=price&ss={city}%2C%20{country}" \
          f"&no_rooms={rooms}&nflt=ht_id%3D204"

def get_search_result(people, country, city, date_in, date_out, rooms):
    result = []
    data_url = create_url(people, country, city, date_in, date_out, rooms)
    response = session.get(data_url, headers=REQUEST_HEADER)
    soup = BeautifulSoup(response.text, "lxml")
    hotels = soup.select("#hotellist_inner div.sr_item.sr_item_new")
    for hotel in hotels:
        result.append(Hotel(hotel))
    session.close()
    return result

def get_hotel_name(hotel):
    identifier = "span.sr-hotel__name"
    if hotel.select_one(identifier) is None:
        return ''
    else:
        return hotel.select_one(identifier).text.strip()

def get_hotel_price(hotel):
    identifier = "div.bui-price-display__value.prco-text-nowrap-helper.prco-inline-block-maker-helper"
    if hotel.select_one(identifier) is None:
        return ''
    else:
        return hotel.select_one(identifier).text.strip()[2:]

def get_coordinates(soup_detail):
    coordinates = []
    if soup_detail.select_one("#hotel_sidebar_static_map") is None:
        coordinates.append('')
        coordinates.append('')
    else:
        coordinates.append(soup_detail.select_one("#hotel_sidebar_static_map")["data-atlas-latlng"].split(",")[0])
        coordinates.append(soup_detail.select_one("#hotel_sidebar_static_map")["data-atlas-latlng"].split(",")[1])
    return coordinates
## CLOSE - Code taken from Medium.com


## Repository of US states
us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 
             'Colorado', 'Connecticut', 'Washington DC', 'Delaware', 
             'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 
             'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
             'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 
             'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 
             'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 
             'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 
             'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 
             'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

## Repository of US winter dates
date_range = pd.date_range(start='21/12/2024', end='19/03/2025')

## Store for hotel data
hotel_data = []

## Temporary variables to update search parameters
hotel_data_len = len(hotel_data)
hotel_data_len_temp = hotel_data_len

n = 0
m = 0

state = us_states[n]

stay_date = date_range[m]
leave_date = date_range[m+1]

## Initial Search Parameters 
search_params = {
    'people': 2,
    'rooms': 1,
    'country': 'United States',
    'city': state,
    'date_in': stay_date,
    'date_out': leave_date,
    }

## Data scraper - Designed to take the first 20 results listed for each state for every day in the winter period. 
for listing in get_search_result(**search_params):
    hotel_data.append(listing)
    m+=1
    search.params.update({
        'date_in:' : stay_date[n],
        'date_out' : leave_date[n+1]
        })
    
    if hotel_data_len_temp == 20:
        hotel_data_len_temp = 0
        n+=1
        search.params.update({
            'city' : state[n],
            })
    

## Transform data into an excel file
df = pd.DataFrame(hotel_data)
df.to_excel('hotel_data.xlsx', index=False) 
  
