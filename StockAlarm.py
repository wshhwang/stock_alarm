#Created by William Hwang
#
from urllib.parse import quote_plus # access URL and pull out data from website
from bs4 import BeautifulSoup #parse and pull out individual items
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
import smtplib #for email

print(time.strftime("%a %b %d, %Y",time.localtime()))
print(time.strftime("%H:%M:%S PST", time.localtime()))
today= time.strftime("%a, %Y",time.localtime())
closed_days = ["Sat","Sun"]
if today in closed_days:
    print("Stock Market is closed today. The stock market will reopen next Monday")

baseUrl = "https://www.google.com/search?q=stock+"
plusUrl = input ('Stock Name: ')
original_price = float(input ('Purchase Stock Price: $'))
shares = int(input("Number of Shares: "))
original_total_price= float(original_price*shares)
url = baseUrl +quote_plus(plusUrl)

#Run google webdriver without openning chrome
options= Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(url)

#set up for html scrap
html = driver.page_source
soup = BeautifulSoup(html)

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587 )
    server.ehlo() #Extended HELO (EHLO)// receving server it supports extensios compatible with ESMTP
    server.starttls() #encrypt connection
    server.ehlo()
    ######## Email information
    server.login('sender_email@gmail.com','Gmail App passwords') #using "Gmail App passwords"

    subject = ('Check stock price on Robinhood!',"+${:.2f}".format(float(current_total_price-original_total_price)))

    body= [stock_name,"${:.2f}".format(float(current_price)),"+{:.2f}%".format(float(diff_percentage)),"+${:.2f}".format(float(current_total_price-original_total_price))]
    msg = f"Subject: {subject} \n\n {body}"
    server.sendmail(   
        ########## Email Information
        'sender_email@gmail.com',
        'recipient_email@gmail.com',
        msg
    )
    print("Email Has Been Sent.")
    print("Highly recommended to sell the stocks now while you have the profit!")
    server.quit()

#look for the exact title and price from F12 Developer mode

r= soup.select('.aviV4d')
for i in r:
    stock_name = i.select_one('.vk_bk').text
    current_price= float(i.select_one('.IsqQVc.NprOob.XcVN5d').text)

#calculate based on current stock price
current_total_price = float(float(current_price)*shares)
diff_percentage = ((current_price - original_price)/original_price)*100

#main function using while Loop
email_delay = 10
decision = True
while decision:
        #current_time = time.strftime("%H:%M:%S", time.localtime())
        print()
        print()
        print("Stock Name:",stock_name)
        print("            $""{:.2f}".format(current_price))
        
        # Negative profit
        if diff_percentage<0:
            print ("-"+"{:.2f}".format(diff_percentage)+"%")
        print ("            +"+"{:.2f}".format(diff_percentage)+"%")
        print()

        # Postive profit more than +5%                
        if diff_percentage>=5:
        #####Send email
            print ("Original Balance: $ "+"{:.2f}".format(float(original_total_price)))
            print ("Current Total Balance: + $ "+"{:.2f}".format(float(current_total_price)))
            print ()
            print ("Current profit: + "+"{:.2f}".format(diff_percentage)+"%")
            print ("              : +$ "+"{:.2f}".format(float(diff_percentage*shares)))           
            print () 
            #send email every 5 minutes(300sec)= 30*10 (while loop delay= 10secs)
            #if (email_delay%10) == 0: 
            #    send_mail()
            send_mail()
            
            email_delay += 1

        # print current time            
        print(time.strftime("%H:%M:%S", time.localtime()))
        print()
        
        # Tell market is closed
        current_market_time= int(time.strftime("%H", time.localtime()))
        if current_market_time>13:
            print("Stock Market is currently closed.")
            print()
            #decision = False  
        time.sleep(5)       
        delay = 5
        while delay != 0 :    
            time.sleep(1)
            delay -=1    
    
driver.close()


