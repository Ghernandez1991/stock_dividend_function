def divcalc(stock_list,how_much_per_month ):

    import pandas as pd
    import yfinance as yf
    from flask import Flask, jsonify, render_template


    #create blank lists to captures data from api
    list_of_tickers = []
    price_list = []
    shares_needed_list = []
    cost_of_shares_list = []
    #iterate down the list of tickers the user provides 
    for row in stock_list:        
        #append the current ticker to the list
        list_of_tickers.append(row)      

        #stock selected by yahoo api is equal to that passed in function 
        
        stock_selected  = yf.Ticker(f'{row}')
        
        #most recent price is previous close price        
        global most_recent_price
        most_recent_price = stock_selected.info['previousClose']
        #append current price to the list
        price_list.append(most_recent_price)
      
        #set the dividends to a pandas series 
        stock_selected_df = stock_selected.dividends
  
    
        #need to set series to an frame
        stock_selected_df = stock_selected_df.to_frame()
        #need to reset index to get date into a column
        stock_selected_df = stock_selected_df.reset_index()
        #need to check the dates on when dividend was issued. get the difference in days between the last item(last dividend), and second to last dividend
        difference = (stock_selected_df["Date"].iloc[-1] - stock_selected_df["Date"].iloc[-2]).days
        #if the date difference is greater than 90, this means dividends are paid quarterly
        if difference >=90:
            #divided the last dividend by three because we want it based on a monthly basis
            dividend = stock_selected_df['Dividends'].iloc[-1]/3
            #if it is less than 35, this means its monthly dividend. using 35 to catch off cases where it wasnt issued on exactly the 30th day
        elif difference <35:
            #if less than 35, grab the most recent dividend listed.
            dividend = stock_selected_df['Dividends'].iloc[-1]
            #for any other values, throw an error
        else:
            print("there is an error in the code")
        
        #calculate how many shares you need to reach the dividends per month            
        global shares_needed
        #calculate shares needed
        shares_needed = how_much_per_month / dividend
        #appened the shares needed to the list
        shares_needed_list.append(shares_needed)
        #print the current row(stock ticker), the list and the lenght of the list
        
        #calculate the total cost of shares needed based on the price      
        
        global cost_of_shares
        #calculate the cost of the shares
        cost_of_shares = shares_needed * most_recent_price
        #append the share cost to the list
        cost_of_shares_list.append(cost_of_shares)
      
        global df
        #list of column names
        column_names = ['Ticker', 'Price', 'Dividends_Per_Month', 'Shares_Needed', 'Cost_of_Shares']
        #create df with column names from list 
        df = pd.DataFrame(columns = column_names)
        
        #create a counter and set to zero
        counter = 0
        #as long as the counter is less than the lenght of the stock list the user passes, stay in this loop
        while counter < (len(stock_list)):
                 #iterate down the lenght of the stock list(passed by user)
            for i in range(len(stock_list)):
                
                #create a dictionary using the current item in the interation(i) and use it to grab the corresponding value in each list
                dictionary = {'Ticker': list_of_tickers[i], 'Price': price_list[i], 'Dividends_Per_Month': how_much_per_month, 'Shares_Needed': shares_needed_list[i], 'Cost_of_Shares': cost_of_shares_list[i]}
                #needed to create temporary dataframe and appened when going through second interation.
                df = df.append(dictionary, ignore_index=True)
                #add one to the counter
                counter = counter + 1
                #if the counter is greater than the number of tickers in the los, get out of the loop
                if counter >= len(list_of_tickers):
                    break
               
    return df