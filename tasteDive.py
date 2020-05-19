#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:19:10 2020

@author: anurag
"""
#
import requests
#import requests_with_caching
import json
import omdbapi
from omdbapi.movie_search import GetMovie

def get_movies_from_tastedive(name):

    parameters = {"q": name, "type": "movies", "limit": 5}
    tastedive_response = requests.get("https://tastedive.com/api/similar", params=parameters)
    movies = json.loads(tastedive_response.text)
    return movies
    # Movies is a dictionary

    #{'Similar': 
    #    {'Info': 
    
    #        [{'Name': 'Black Panther', 'Type': 'movie'}],
    #    'Results': 
    #     [{'Name': 'Captain Marvel', 'Type': 'movie'},
    #      {'Name': 'Avengers: Infinity War', 'Type': 'movie'},
    #      {'Name': 'Ant-Man And The Wasp', 'Type': 'movie'},
    #      {'Name': 'Deadpool 2', 'Type': 'movie'},
    #      {'Name': 'Jumanji: Welcome To The Jungle', 'Type': 'movie'}]}}


def  extract_movie_titles(movie_dict):
     movie_titles = []
     movie_info = movie_dict["Similar"]["Results"]
     for movie in movie_info:
        movie_titles.append(movie["Name"])
     return movie_titles


def get_related_titles(movie_titles):
    
    for title in movie_titles:
       new_titles = []
       movies = get_movies_from_tastedive(title)
       titles = extract_movie_titles(movies)
       for t in titles:
           if t not in new_titles:
               new_titles.append(t)
    return new_titles

def get_movie_data(movie_name):
    parameters = {'t': movie_name, 'r': 'json'}
    omdbapi_response = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=f5647f6', params=parameters)
    movie_dict = json.loads(omdbapi_response.text)
    return movie_dict


def get_movie_rating(movie_dict):
    rottenTomato_rating = 0
    if len(movie_dict['Ratings']):
        if movie_dict['Ratings'][1]['Source'] == 'Rotten Tomatoes':
            rottenTomato_rating = movie_dict['Ratings'][1]['Value'][:2]
            rottenTomato_rating = int(rottenTomato_rating)
    else:
        rottenTomato_rating = 0

    return rottenTomato_rating
    
def get_sorted_recommendations(movie_list):
    related_movies = get_related_titles(movie_list)
    ratings = []
    for movie in related_movies:
        a = get_movie_data(movie)
        ratings.append(get_movie_rating(a))

    results = zip(ratings, related_movies)
    sortedResults = sorted(results, reverse=True)    
    return sortedResults
               
if __name__ == "__main__"     :
    
    movie_dicts = get_movies_from_tastedive(input("insert a movie name :"))    
    movie_lists = extract_movie_titles(movie_dicts) 
    print("processing...")
    sortedRating = get_sorted_recommendations(movie_lists)   
    print(sortedRating,"\n Completed")    