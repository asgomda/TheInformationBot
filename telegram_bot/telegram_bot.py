import os
import telebot
import random

# importing the API_KEY
from secrets import API_KEY

# importing the imdb library for movies
import imdb
# importing the yahoo finance library for fin info
import yfinance as YF 

# creating the bot
bot = telebot.TeleBot(API_KEY)

# creating an instance of the imdb class

imd = imdb.IMDb()

# list of responses
response_list = ["Hey! How are you doing?", "Hey, what's up?", "Hey, what's going on?", "Hello, what's new?", "Hey, what do you want to find out?"]

# the start command
# information about the bot
@bot.message_handler(commands=['start'])
def start(message):
    start_message = "This bot is capable of telling you the recent stock prices\n of your favourite socks as well as the information about your\n favourite movies\n To search a movie, type movie/mov/m movie_name \n To search the price of a stock, type price stock_name"
    bot.send_message(message.chat.id, start_message)


# handling greetings for when the use uses commands
@bot.message_handler(commands=['Hello', 'Greet', 'hello', 'greet', 'hi', 'Hi', 'hey', 'Hey'])
def hello(message):
    bot.send_message(message.chat.id, random.choice(response_list))


# the greetins function to handle greetings 
def greetings(message):
    greetings_list = ['hello', 'hi', 'howdy', 'greetings', 'hey', 'greet']
    request = message.text.lower()
    if request in greetings_list:
        return True
    else:
        return False

def isMovie(message):
    # validating the request
    request = message.text.split()
    if (len(request) < 2) or  (request[0].lower() not in ['mov', 'movie', 'm']):
        return False
    else:
        return True


# handling normal text greetings
@bot.message_handler(func=greetings)
def send_greetings(message):
   bot.send_message(message.chat.id, random.choice(response_list)) 


# handling movies throung imdb api
@bot.message_handler(func=isMovie)
def send_movie(message):
    request = message.text[message.text.find(" ")+1:] # getting the movie
    print("this is the request "+ request)
    response = ""

    try:
        movie_name = imd.search_movie(request)[0]
        
        movie_id = imd.get_imdbID(movie_name)

        movie = imd.get_movie(movie_id)

        
        plot = movie['plot'][0]
        response+=(plot + "\n")

        # printing the genres
        response += "Genres: \n"

        for genre in movie['genres']:
            response += (genre + " "*6)
        # su
        bot.send_message(message.chat.id, response)

    except:
        #movie_name = imd.search_movie(request)

        bot.send_message(message.chat.id, "Movie not available!")


# checking for messages
bot.polling()

