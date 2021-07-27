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

# checking input
def isWSB(message):
    if message.text.strip().lower() == 'wsb':
        return True
    else:
        return False
# handling commands for wsc
@bot.message_handler(func=isWSB) 
def sendWSB(message):
    # response to store the data
    response = ''
    stocks_list = ['tsla', 'gme', 'amc', 'nok', 'msft']
    stock_data = []

    try: 
        for stock in stocks_list:
            # getting data from yahoo finance api
            data = YF.download(tickers=stock, period='2d', interval='1d')
            data = data.reset_index()
            response+= f"-----{stock}-----\n"
            stock_data.append([stock])
            cols = ['stock']
            for ind,row in data.iterrows():
                stock_pos = len(stock_data) -1
                price = round(row['Close'], 2)
                formated_date = row['Date'].strftime('%m/%d')
                response += f"{formated_date}: {price}\n"
                stock_data[stock_pos].append(price)
                cols.append(formated_date)
            print()
        # formatting the response
        response = f"{cols[0] : <15}{cols[1] : ^15}{cols[2] : >15}\n"
        for row in stock_data:
            response += f"{row[0] : <15}{row[1] : ^15}{row[2] : >15}\n"
        response += "\nWSB Stock Data"

        #print(response)
        bot.send_message(message.chat.id, response)
    except:
        bot.send_message(message.chat.id, "Could not fetch Data")
    


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

#handling stock requests
def requested_stock(message):
    req = message.text.split()
    if(len(req) < 2 or req[0].lower() not in "price"):
        return False
    else:
        return True


@bot.message_handler(func=requested_stock)
def send_stock(message):
    # finding and sending stock
    request = message.text.split()[1]
    data = YF.download(tickers=request, period='5m', interval = '1m')

    # checking if data is valid
    if data.size > 1:
        data = data.reset_index()
        data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        response = f"{data['Close'].to_string(header=False)}\n\n{request} Stock Data"
        bot.send_message(message.chat.id, response)
        
    else:
        bot.send_message(message.chat.id, "No Data Available!")

# checking for messages
bot.polling()

