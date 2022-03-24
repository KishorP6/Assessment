import datetime

from kraken.api_call import api_call
import pytest
import json
import websocket
import _thread
import time
import json

'''
@pytest.fixture
def order_book():
    a = api_call()
    xbtusd_book = {'pair': 'XBTUSD', 'count': '10'}  # Limiting to 10 Asks/Bids for Assignment purpose
    xbtusd_orders = a.api_endpt('Depth', xbtusd_book)
    return xbtusd_orders
'''


# Test Depth Method for XBTUSD Pair
def test_xbt_orderbook():
    a = api_call()
    xbtusd_book = {'pair': 'XBTUSD', 'count': '10'}  # Limiting to 10 Asks/Bids for Assignment purpose
    xbtusd_orders = a.api_endpt('Depth', xbtusd_book)
    assert xbtusd_orders.status_code == 200
    orders = xbtusd_orders.json()
    asks = orders['result']['XXBTZUSD']['asks'][0][0]
    bids = orders['result']['XXBTZUSD']['bids'][0][0]

    msg = ("Pari: XBTUSD  and Ask is {} and bid is {}" )
    print(msg.format(asks,bids))

    assert asks > bids


# Test Depth Method for XBTUSD Pair
def test_ltc_orderbook():
    a = api_call()
    book = {'pair': 'LTCUSD', 'count': '10'}  # Limiting to 10 Asks/Bids for Assignment purpose
    orders = a.api_endpt('Depth', book)
    assert orders.status_code == 200
    json_orders = orders.json()
    asks = json_orders['result']['XLTCZUSD']['asks'][0][0]
    bids = json_orders['result']['XLTCZUSD']['bids'][0][0]

    msg = ("Pari: LTCUSD  and Ask is {} and bid is {}")
    print(msg.format(asks, bids))

    assert asks > bids

# Test Depth Method for XBTUSD Pair
def test_unknow_pair():
    a = api_call()
    unk_book = {'pair': 'LTCUSDEUR', 'count': '10'}  # Limiting to 10 Asks/Bids for Assignment purpose
    unk_orders = a.api_endpt('Depth', unk_book)
    assert unk_orders.status_code == 200
    error_msg = unk_orders.json()['error']
    expexted_msg = "EQuery:Unknown asset pair"
    print(error_msg)

    assert expexted_msg in  error_msg


def test_websocket():
    def ws_message(ws, message):
        print("WebSocket thread: %s" % message)
        ws_assert_timestamp(message)

    def ws_assert_timestamp(data):
        json_message = json.loads(data)

        if 'event' in json_message:
            return
        else:
            sub_data = json_message[1]
            latest_timestamp = float(sub_data[0][2])

            ws_timestamp.append(latest_timestamp)
            time_interval = (latest_timestamp) - (ws_timestamp[-2])
            if time_interval > 0:
                print("Time stamp received in subscription data is increasing over time")
            print(time_interval)
            assert time_interval > 0


    def ws_open(ws):
        ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')

    def ws_close(ws):
        ws.keep_running = False

    def ws_thread(*args):
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open=ws_open, on_message=ws_message,on_close=ws_close)
        ws.run_forever()

    _thread.start_new_thread(ws_thread, ())

    msg_counter = 0
    ws_timestamp = [time.time()]

    while True:
        time.sleep(5)
        msg_counter = msg_counter + 1
        if msg_counter > 2:
    # Exit the thread after receiving 10 messages
            break
        #print("Main thread: %d" % time.time())

