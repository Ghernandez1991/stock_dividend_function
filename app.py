import pandas as pd
import yfinance as yf
from flask import Flask, jsonify, render_template, request



app = Flask(__name__)



import pandas as pd
import yfinance as yf
from flask import Flask, jsonify, render_template, request
from function import divcalc
    
    
#how_much_per_month = int(input('How much per month are you looking to make in dividends?'))

#input_string = input("Enter stock tickers(all caps-no spaces) separated by comma ")
#stock_list  = input_string.split(",")

#divcalc(stock_list, how_much_per_month )

#df = divcalc(stock_list, how_much_per_month )


@app.route("/",  methods=("POST", "GET"))
def pie():

    
    #stock_list = request.form.get(fname)
    #how_much_per_month = request.form.get(lname)
    #print(stock_list, how_much_per_month)
    if request.method == "POST": 
       # getting input with name = fname in HTML form 
       global stock_list
       stock_list = request.form.get("ticker") 
       # getting input with name = lname in HTML form  
       global how_much_per_month
       how_much_per_month = request.form.get("income")  
       #return (print(first_name))
       return(stock_list, how_much_per_month)

      
       
       #df = divcalc(stock_list, how_much_per_month )
    #return render_template("homepage.html", tables = [df.to_html(classes='data')], titles=df.columns.values)
    #print(ticker, income)
    return render_template("homepage.html" )
  


    #return render_template('homepage.html', tables = [df.to_html(classes='data')], titles=df.columns.values)

@app.route("/secondpage",  methods=("POST", "GET"))
def secondpage():
    #stock_list = stock_list
    #how_much_per_month = how_much_per_month

    stock_list, how_much_per_month = pie()
    how_much_per_month = int(how_much_per_month)

    df = divcalc(stock_list, how_much_per_month )


    return render_template("secondpage.html", tables = [df.to_html(classes='data')], titles=df.columns.values)


if __name__ == "__main__":

    app.run()