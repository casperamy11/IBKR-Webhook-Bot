#Imports

from datetime import datetime
from sanic import Sanic
from sanic import response
from ib_insync import *

# Create Sanicobject called app.
app = Sanic(__name__)
app.ib = None

# Create root to easily let us know its on/working.
@app.route('/')

async def root(request):
    return response.text('online')

#Listen for signals and submit orders
@app.route('/webhook1', methods=['POST'])
async def webhook1(request):
     if request.method == 'POST':
        #Check if we need to reconnect with IB
        await checkIfReconnect()
        # Parse the string data from tradingview into a python dict
        data = request.json
        order = MarketOrder("BUY",1,account=app.ib.wrapper.accounts[0])
        #contract = Crypto(data['symbol'][0:3],'PAXOS',data['symbol'][3:6]) #Get first 3 chars BTC then last 3 for currency USD
        #or stock for example 
        contract = Stock('AAPL','SMART','USD')
        app.ib.placeOrder(contract, order)
     return response.json({})

@app.route('/webhook2', methods=['POST'])
async def webhook2(request):
     if request.method == 'POST':
        #Check if we need to reconnect with IB
        await checkIfReconnect()
        # Parse the string data from tradingview into a python dict
        data = request.json
        order = MarketOrder("SELL",1,account=app.ib.wrapper.accounts[0])
        #contract = Crypto(data['symbol'][0:3],'PAXOS',data['symbol'][3:6]) #Get first 3 chars BTC then last 3 for currency USD
        #or stock for example 
        contract = Stock('AAPL','SMART','USD')
        app.ib.placeOrder(contract, order)
     return response.json({})

#Check every minute if we need to reconnect to IB
async def checkIfReconnect():
    if not app.ib.isConnected() or not app.ib.client.isConnected():
            app.ib.disconnect()
            app.ib = IB()
            app.ib.connect('127.0.0.1', 7497,clientId=1)

#Run App
if __name__ == "__main__":
    #Connect to IB
    app.ib = IB()
    app.ib.connect('127.0.0.1', 7497,clientId=1)
    app.run(port=5000)


