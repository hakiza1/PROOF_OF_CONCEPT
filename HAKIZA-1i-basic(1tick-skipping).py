import asyncio
from deriv_api import DerivAPI
from deriv_api import APIError
from rx import Observable
import os
import sys
import websockets
import random
from datetime import datetime, timedelta


# ====================
# Secure Configuration
# ====================
DERIV_API_TOKEN = os.getenv('DERIV_TOKEN', '')
DERIV_WEBSOCKET_URL = os.getenv('DERIV_WEBSOCKET', '')

if len(DERIV_API_TOKEN) == 0:
    print("DERIV_API_TOKEN environment variable is not set. Exiting...")
    sys.exit(1)


# ====================
# Global Configuration
# ====================
CONFIG = {
    "SYMBOLS": ["stpRNG", "stpRNG2",  "stpRNG3", "1HZ10V", "1HZ25V", "1HZ50V", "R_10", "R_25", "R_50", "JD10", "JD25", "JD50"],
    "BOTS": ["BOT1", "BOT2"],
    "MAX_RETRIES": 3,
    "CANDLE_DURATION1": 1,
    "CANDLE_DURATION2": 1,
    "API_TOKEN": DERIV_API_TOKEN,
    "WEBSOCKET_URL": DERIV_WEBSOCKET_URL
}

SYMBOL_STATES = {
    symbol: {
        "BOT1": {
            "last_candle_open1": None,
            "last_candle_close1": None,
            "current_candle_ticks1": [],
            "non_reversal_count1": 0,
            "is_sequence_starting_with_green1": False,
            "is_sequence_starting_with_red1": False,
            "trade_type1": "",
            "stake_amount1": 0,
            "previous_stake_amount1": 0,
            "skip_next_tick1": 0,
            "last_executed_non_reversal_count1": -1
        },
        "BOT2": {
            "last_candle_open2": None,
            "last_candle_close2": None,
            "current_candle_ticks2": [],
            "reversal_count2": 0,
            "is_sequence_starting_with_green2": False,
            "is_sequence_starting_with_red2": False,
            "trade_type2": "",
            "stake_amount2": 0,
            "previous_stake_amount2": 0,
            "skip_next_tick2": 0,
            "last_executed_reversal_count2": -1
        }
    }
    for symbol in CONFIG["SYMBOLS"]
}

SYMBOL_LOCKS = {symbol: asyncio.Lock() for symbol in CONFIG["SYMBOLS"]}

retry_attempts = 0
GLOBAL_SEQUENCE_ACTIVE = False
ACTIVE_SYMBOL = None
ACTIVE_BOT = None
INACTIVE_SYMBOL = None
INACTIVE_BOT = None
ACTIVATION_CANDIDATES = []
LAST_ACTIVATION_TIME = None
ACTIVATION_WINDOW = timedelta(seconds=0.1)

LAST_HEARTBEAT = datetime.now()
HEARTBEAT_TIMEOUT = timedelta(seconds=333)
RESTARTING = False
heartbeat_task = None 

# ====================
# Activation Control
# ====================
async def activate_symbol(symbol):
    global GLOBAL_SEQUENCE_ACTIVE, ACTIVE_SYMBOL, INACTIVE_SYMBOL, ACTIVATION_CANDIDATES, LAST_ACTIVATION_TIME    
    try:
        if not GLOBAL_SEQUENCE_ACTIVE:
            current_time = datetime.now()
            if LAST_ACTIVATION_TIME is None or (current_time - LAST_ACTIVATION_TIME) > ACTIVATION_WINDOW:
                ACTIVATION_CANDIDATES = []
            if symbol not in ACTIVATION_CANDIDATES:
                ACTIVATION_CANDIDATES.append(symbol)
                LAST_ACTIVATION_TIME = current_time
                print(f"{symbol} added to activation candidates: {ACTIVATION_CANDIDATES}")
            if len(ACTIVATION_CANDIDATES) > 0:
                GLOBAL_SEQUENCE_ACTIVE = True
                ACTIVE_SYMBOL = random.choice(ACTIVATION_CANDIDATES)
                INACTIVE_SYMBOL = [s for s in CONFIG["SYMBOLS"] if s != ACTIVE_SYMBOL]
                ACTIVATION_CANDIDATES = []
                print(f"{ACTIVE_SYMBOL} has been randomly selected as the active symbol.")
    except Exception as e:
        await reset_state()
        return False


# ====================
# Deactivation Control
# ====================
async def deactivate_symbol(symbol):
    global GLOBAL_SEQUENCE_ACTIVE, LAST_ACTIVATION_TIME
    current_time = datetime.now()
    if LAST_ACTIVATION_TIME is not None and GLOBAL_SEQUENCE_ACTIVE:
        elapsed_time = current_time - LAST_ACTIVATION_TIME
        if elapsed_time >= timedelta(seconds=333):        
            print(f"{symbol}: Active sequence compromised. Possible arbitrage...Pay your attention and start monitoring your data_flow in order to expose intentional data_integrity violation from your broker...Releasing global lock...restart in 3 seconds.")
            await reset_state() 
            await asyncio.sleep(3)  


# ====================
# HeartBeat Monitor
# ====================
async def heartbeat_monitor():
    """Monitor for missed heartbeats and restart the bot if needed."""
    global LAST_HEARTBEAT, RESTARTING
    while True:
        await asyncio.sleep(33)
        now = datetime.now()
        if now - LAST_HEARTBEAT > HEARTBEAT_TIMEOUT:
            print(f"No heartbeat received for over 333 seconds. Possible arbitrage...Pay your attention and start monitoring your data_flow in order to expose intentional data_integrity violation from your broker...Fresh restarting the bot after 3 seconds.")
            RESTARTING = True
            await reset_state()
            os.execl(sys.executable, sys.executable, *sys.argv)
            
 
# ====================
# Reset State Function
# ====================
async def reset_state():
    await reset_state1()
    await reset_state2()


# ====================
# Informational INGOMA1
# ====================

async def reset_state1():
    """Reset internal state for all symbols."""
    global GLOBAL_SEQUENCE_ACTIVE, ACTIVE_SYMBOL, INACTIVE_SYMBOL, ACTIVE_BOT, INACTIVE_BOT, ACTIVATION_CANDIDATES, LAST_ACTIVATION_TIME
    try:
        for symbol in SYMBOL_STATES:
            state = SYMBOL_STATES[symbol]["BOT1"]
            state["last_candle_open1"] = None
            state["last_candle_close1"] = None
            state["current_candle_ticks1"] = []
            state["non_reversal_count1"] = 0
            state["is_sequence_starting_with_green1"] = False
            state["is_sequence_starting_with_red1"] = False
            state["trade_type1"] = ""
            state["stake_amount1"] = 0
            state["previous_stake_amount1"] = 0
            state["skip_next_tick1"] = 0            
            state["last_executed_non_reversal_count1"] = -1
        GLOBAL_SEQUENCE_ACTIVE = False
        ACTIVE_SYMBOL = None
        ACTIVE_BOT = None
        INACTIVE_SYMBOL = None
        INACTIVE_BOT = None
        ACTIVATION_CANDIDATES = []
        LAST_ACTIVATION_TIME = None
        print("Bot1 state has been reset for all symbols.")
    except Exception as e:
        print(f"Error during reset_state1: {e}")


def create_subscription_callback1(symbol):
    def callback(data):
        global LAST_HEARTBEAT
        try:
            if "ping" in data:
                LAST_HEARTBEAT = datetime.now()
                print("Heartbeat received.")
            elif "tick" in data:
                asyncio.create_task(handle_tick1(symbol, data))
        except Exception as e:
            print(f"Error in subscription callback for {symbol}: {e}")
    return callback


async def handle_tick1(symbol, tick):
    """Handle incoming tick data for a specific symbol."""
    state = SYMBOL_STATES[symbol]["BOT1"]
    try:
        quote = tick["tick"]["quote"]

        # Handle tick skipping logic for one tick 
        if state["skip_next_tick1"] > 0:
            if state["skip_next_tick1"] == 1:
                # Skipped tick - store as first tick of next candle
                print(f"{symbol}: Skipped tick {quote} - stored as first tick of new candle")
                state["current_candle_ticks1"] = [quote]
                state["skip_next_tick1"] = 0  
            return
            
        # Normal tick processing
        if len(state["current_candle_ticks1"]) < CONFIG["CANDLE_DURATION1"] + 1:
            state["current_candle_ticks1"].append(quote)
            
        if len(state["current_candle_ticks1"]) == CONFIG["CANDLE_DURATION1"] + 1:
            print(f"{symbol}: Candle complete: {state['current_candle_ticks1']}")
            async with SYMBOL_LOCKS[symbol]:
                await process_candle1(symbol)
            # Set to skip one tick after candle completion
            state["skip_next_tick1"] = 1
            
    except Exception as e:
        print(f"Error handling tick data for {symbol}: {e}")


async def detect_non_reversals1(symbol, last_candle_color1, second_last_candle_color1):
    global GLOBAL_SEQUENCE_ACTIVE, ACTIVE_SYMBOL, INACTIVE_SYMBOL, ACTIVE_BOT, INACTIVE_BOT
    state = SYMBOL_STATES[symbol]["BOT1"]
    try:
        await deactivate_symbol(symbol)
        
        if GLOBAL_SEQUENCE_ACTIVE and (symbol != ACTIVE_SYMBOL or ACTIVE_BOT != "BOT1"):
            print(f"{symbol}: Global sequence active on {ACTIVE_SYMBOL}. Skipping further processing.")
            return
            
        if (
            second_last_candle_color1 is None
            or last_candle_color1 is None
            or last_candle_color1 != second_last_candle_color1
        ):
            prev_count1 = state["non_reversal_count1"]
            state["non_reversal_count1"] = 0
            state["is_sequence_starting_with_green1"] = False
            state["is_sequence_starting_with_red1"] = False
            print(f"Non_reversal count reset for {symbol}")
            if GLOBAL_SEQUENCE_ACTIVE and ACTIVE_SYMBOL == symbol and prev_count1 >= 1:  # The threshold can be increased to any odd number for safety
                print(f"{symbol}: Active sequence completed (had {prev_count1} non_reversals). Releasing global lock.")
                await reset_state1()
            return
        
        if not state["is_sequence_starting_with_green1"] and not state["is_sequence_starting_with_red1"]:
            if second_last_candle_color1 == 1:
                state["is_sequence_starting_with_green1"] = True
                print(f"{symbol}: Green flag triggered")
            elif second_last_candle_color1 == -1:
                state["is_sequence_starting_with_red1"] = True
                print(f"{symbol}: Red flag triggered")
       
        if last_candle_color1 == second_last_candle_color1:
            if state["is_sequence_starting_with_green1"] or state["is_sequence_starting_with_red1"]:
                state["non_reversal_count1"] += 1
                print(f"{symbol}: Non_reversal count increased to {state['non_reversal_count1']}")
                if state["non_reversal_count1"] >= 1:  # The threshold can be increased to any odd number for safety
                    ACTIVE_BOT = "BOT1"
                    INACTIVE_BOT = [b for b in CONFIG["BOTS"] if b != ACTIVE_BOT]
                    await activate_symbol(symbol)
    
    except Exception as e:
        print(f"Error detecting non_reversals for {symbol}: {e}")


async def process_candle1(symbol):
    """Process completed candlestick for a given symbol."""
    global INACTIVE_SYMBOL
    state = SYMBOL_STATES[symbol]["BOT1"]
    try:
        second_last_candle_color1 = (
            1 if state["last_candle_open1"] is not None and state["last_candle_close1"] is not None and state["last_candle_close1"] > state["last_candle_open1"] else
            (-1 if state["last_candle_open1"] is not None and state["last_candle_close1"] is not None and state["last_candle_close1"] < state["last_candle_open1"] else None)
        )
        last_candle_color1 = (
            1 if state["current_candle_ticks1"][0] is not None and state["current_candle_ticks1"][-1] > state["current_candle_ticks1"][0] else
            (-1 if state["current_candle_ticks1"][0] is not None and state["current_candle_ticks1"][-1] < state["current_candle_ticks1"][0] else None)
        )
      
        await detect_non_reversals1(symbol, last_candle_color1, second_last_candle_color1)
       
        if state["non_reversal_count1"] == 1:  # The threshold can be increased to any odd number for safety
            if state["is_sequence_starting_with_green1"]:
                state["trade_type1"] = "PUTE"
                state["stake_amount1"] = 1
                state["previous_stake_amount1"] = state["stake_amount1"]
            elif state["is_sequence_starting_with_red1"]:
                state["trade_type1"] = "CALLE"
                state["stake_amount1"] = 1
                state["previous_stake_amount1"] = state["stake_amount1"]
                
        elif state["non_reversal_count1"] > 1:  # The threshold can be increased to any odd number for safety
            if state["is_sequence_starting_with_green1"]:
                state["trade_type1"] = "PUTE"
                state["stake_amount1"] = state["previous_stake_amount1"] * 2.1
                state["previous_stake_amount1"] = state["stake_amount1"]
            elif state["is_sequence_starting_with_red1"]:
                state["trade_type1"] = "CALLE"
                state["stake_amount1"] = state["previous_stake_amount1"] * 2.1
                state["previous_stake_amount1"] = state["stake_amount1"]
                
        else:
            state["trade_type1"] = ""

        if (
            (INACTIVE_SYMBOL is not None and symbol not in INACTIVE_SYMBOL) and
            state["trade_type1"] in ["PUTE", "CALLE"] and
            state["stake_amount1"] > 0 and
            state["non_reversal_count1"] > state["last_executed_non_reversal_count1"]
        ):
            await place_trades1(symbol, state["trade_type1"], state["stake_amount1"])
            print(f"Placed {state['trade_type1']} trade for {symbol} with stake: {state['stake_amount1']}")
            state["last_executed_non_reversal_count1"] = state["non_reversal_count1"]
        else:
            print(f"No trade placed for {symbol} (duplicate or invalid non_reversal count)")

        state["last_candle_open1"] = state["current_candle_ticks1"][0]
        state["last_candle_close1"] = state["current_candle_ticks1"][-1]
        
    except Exception as e:
        print(f"Error processing candle for {symbol}: {e}")


async def place_trades1(symbol, trade_type1, stake_amount1):
    """Place trades based on detected trade type for a symbol."""
    try:
        proposal = await api.proposal({
            "proposal": 1,
            "amount": stake_amount1,
            "basis": "stake",
            "contract_type": trade_type1,
            "currency": "USD",
            "duration": 1,
            "duration_unit": "t",
            "symbol": symbol
        })
    except APIError as e:
        print(f"APIError while getting proposal for {symbol}: {e}. Skipping trade...")
        return
    except Exception as e:
        print(f"Unexpected error while getting proposal for {symbol}: {e}. Skipping trade...")
        return
        
    try:
        proposal_id = proposal.get("proposal", {}).get("id")
        if not proposal_id:
            print(f"No proposal ID found for {symbol}. Skipping trade...")
            return
        buy_response = await api.buy({
            "buy": proposal_id,
            "price": stake_amount1
        })
        print(f"Trade successfully placed for {symbol}")
    except APIError as e:
        print(f"APIError while buying contract for {symbol}: {e}. Skipping trade...")
    except Exception as e:
        print(f"Unexpected error while buying contract for {symbol}: {e}. Skipping trade...")


# ====================
# Informational INGOMA2
# ====================

async def reset_state2():
    """Reset internal state for all symbols."""
    global GLOBAL_SEQUENCE_ACTIVE, ACTIVE_SYMBOL, INACTIVE_SYMBOL, ACTIVE_BOT, INACTIVE_BOT, ACTIVATION_CANDIDATES, LAST_ACTIVATION_TIME
    try:
        for symbol in SYMBOL_STATES:
            state = SYMBOL_STATES[symbol]["BOT2"]
            state["last_candle_open2"] = None
            state["last_candle_close2"] = None
            state["current_candle_ticks2"] = []
            state["reversal_count2"] = 0
            state["is_sequence_starting_with_green2"] = False
            state["is_sequence_starting_with_red2"] = False
            state["trade_type2"] = ""
            state["stake_amount2"] = 0
            state["previous_stake_amount2"] = 0
            state["skip_next_tick2"] = 0              
            state["last_executed_reversal_count2"] = -1
        GLOBAL_SEQUENCE_ACTIVE = False
        ACTIVE_SYMBOL = None
        ACTIVE_BOT = None
        INACTIVE_SYMBOL = None
        INACTIVE_BOT = None
        ACTIVATION_CANDIDATES = []
        LAST_ACTIVATION_TIME = None
        print("Bot2 state has been reset for all symbols.")
    except Exception as e:
        print(f"Error during reset_state2: {e}")


def create_subscription_callback2(symbol):
    def callback(data):
        try:
            if "tick" in data:
                asyncio.create_task(handle_tick2(symbol, data))
        except Exception as e:
            print(f"Error in subscription callback for {symbol}: {e}")
    return callback


async def handle_tick2(symbol, tick):
    """Handle incoming tick data for a specific symbol."""
    state = SYMBOL_STATES[symbol]["BOT2"]
    try:
        quote = tick["tick"]["quote"]

        # Handle tick skipping logic for one tick
        if state["skip_next_tick2"] > 0:
            if state["skip_next_tick2"] == 1:
                # Skipped tick - store as first tick of next candle
                print(f"{symbol}: Skipped tick {quote} - stored as first tick of new candle")
                state["current_candle_ticks2"] = [quote]
                state["skip_next_tick2"] = 0  
            return
            
        # Normal tick processing
        if len(state["current_candle_ticks2"]) < CONFIG["CANDLE_DURATION2"] + 1:
            state["current_candle_ticks2"].append(quote)
            
        if len(state["current_candle_ticks2"]) == CONFIG["CANDLE_DURATION2"] + 1:
            print(f"{symbol}: Candle complete: {state['current_candle_ticks2']}")
            async with SYMBOL_LOCKS[symbol]:
                await process_candle2(symbol)
            # Set to skip one tick after candle completion
            state["skip_next_tick2"] = 1
            
    except Exception as e:
        print(f"Error handling tick data for {symbol}: {e}")


async def detect_reversals2(symbol, last_candle_color2, second_last_candle_color2):
    """Detect reversals and update reversal counts for a specific symbol."""
    global GLOBAL_SEQUENCE_ACTIVE, ACTIVE_SYMBOL, INACTIVE_SYMBOL, ACTIVE_BOT, INACTIVE_BOT
    state = SYMBOL_STATES[symbol]["BOT2"]
    try:
        if GLOBAL_SEQUENCE_ACTIVE and (symbol != ACTIVE_SYMBOL or ACTIVE_BOT != "BOT2"):
            print(f"{symbol}: Global sequence active on {ACTIVE_SYMBOL}. Skipping further processing.")
            return

        if (
            second_last_candle_color2 is None
            or last_candle_color2 is None
            or last_candle_color2 == second_last_candle_color2
        ):
            prev_count2 = state["reversal_count2"]
            state["reversal_count2"] = 0
            state["is_sequence_starting_with_green2"] = False
            state["is_sequence_starting_with_red2"] = False
            print(f"Reversal count reset for {symbol}")
            if GLOBAL_SEQUENCE_ACTIVE and ACTIVE_SYMBOL == symbol and prev_count2 >= 1:  # The threshold can be increased to any odd number for safety
                print(f"{symbol}: Active sequence completed (had {prev_count2} reversals). Releasing global lock.")
                await reset_state2()
            return

        if not state["is_sequence_starting_with_green2"] and not state["is_sequence_starting_with_red2"]:
            if second_last_candle_color2 == -1:
                state["is_sequence_starting_with_green2"] = True
                print(f"{symbol}: Green flag triggered")
            elif second_last_candle_color2 == 1:
                state["is_sequence_starting_with_red2"] = True
                print(f"{symbol}: Red flag triggered")

        if last_candle_color2 != second_last_candle_color2:
            if state["is_sequence_starting_with_green2"] or state["is_sequence_starting_with_red2"]:
                state["reversal_count2"] += 1
                print(f"{symbol}: Reversal count increased to {state['reversal_count2']}")
                if state["reversal_count2"] >= 1:  # The threshold can be increased to any odd number for safety
                    ACTIVE_BOT = "BOT2"
                    INACTIVE_BOT = [s for s in CONFIG["BOTS"] if s != ACTIVE_BOT]
                    await activate_symbol(symbol)

    except Exception as e:
        print(f"Error detecting reversals for {symbol}: {e}")


async def process_candle2(symbol):
    """Process completed candlestick for a given symbol."""
    global INACTIVE_SYMBOL 
    state = SYMBOL_STATES[symbol]["BOT2"]
    try:
        second_last_candle_color2 = (
            1 if state["last_candle_open2"] is not None and state["last_candle_close2"] is not None and state["last_candle_close2"] > state["last_candle_open2"] else
            (-1 if state["last_candle_open2"] is not None and state["last_candle_close2"] is not None and state["last_candle_close2"] < state["last_candle_open2"] else None)
        )
        last_candle_color2 = (
            1 if state["current_candle_ticks2"][0] is not None and state["current_candle_ticks2"][-1] > state["current_candle_ticks2"][0] else
            (-1 if state["current_candle_ticks2"][0] is not None and state["current_candle_ticks2"][-1] < state["current_candle_ticks2"][0] else None)
        )

        await detect_reversals2(symbol, last_candle_color2, second_last_candle_color2)

        if state["reversal_count2"] == 1:  # The threshold can be increased to any odd number for safety
            if state["is_sequence_starting_with_green2"]:
                state["trade_type2"] = "CALLE"
                state["stake_amount2"] = 1
                state["previous_stake_amount2"] = state["stake_amount2"]
            elif state["is_sequence_starting_with_red2"]:
                state["trade_type2"] = "PUTE"
                state["stake_amount2"] = 1
                state["previous_stake_amount2"] = state["stake_amount2"]
                
        elif state["reversal_count2"] > 1:  # The threshold can be increased to any odd number for safety
            if state["is_sequence_starting_with_green2"]:
                state["trade_type2"] = "CALLE" if state["reversal_count2"] % 2 == 1 else "PUTE"
                state["stake_amount2"] = state["previous_stake_amount2"] * 2.1
                state["previous_stake_amount2"] = state["stake_amount2"]
            elif state["is_sequence_starting_with_red2"]:
                state["trade_type2"] = "PUTE" if state["reversal_count2"] % 2 == 1 else "CALLE"
                state["stake_amount2"] = state["previous_stake_amount2"] * 2.1
                state["previous_stake_amount2"] = state["stake_amount2"]
                
        else:
            state["trade_type2"] = ""

        if (
            (INACTIVE_SYMBOL is not None and symbol not in INACTIVE_SYMBOL) and
            state["trade_type2"] in ["PUTE", "CALLE"] and
            state["stake_amount2"] > 0 and
            state["reversal_count2"] > state["last_executed_reversal_count2"]
        ):
            await place_trades2(symbol, state["trade_type2"], state["stake_amount2"])
            print(f"Placed {state['trade_type2']} trade for {symbol} with stake: {state['stake_amount2']}")
            state["last_executed_reversal_count2"] = state["reversal_count2"]
        else:
            print(f"No trade placed for {symbol} (duplicate or invalid reversal count)")

        state["last_candle_open2"] = state["current_candle_ticks2"][0]
        state["last_candle_close2"] = state["current_candle_ticks2"][-1]

    except Exception as e:
        print(f"Error processing candle for {symbol}: {e}")


async def place_trades2(symbol, trade_type2, stake_amount2):
    """Place trades based on detected trade type for a symbol."""
    try:
        proposal = await api.proposal({
            "proposal": 1,
            "amount": stake_amount2,
            "basis": "stake",
            "contract_type": trade_type2,
            "currency": "USD",
            "duration": 1,
            "duration_unit": "t",
            "symbol": symbol
        })
    except APIError as e:
        print(f"APIError while getting proposal for {symbol}: {e}. Skipping trade...")
        return
    except Exception as e:
        print(f"Unexpected error while getting proposal for {symbol}: {e}. Skipping trade...")
        return
        
    try:
        proposal_id = proposal.get("proposal", {}).get("id")
        if not proposal_id:
            print(f"No proposal ID found for {symbol}. Skipping trade...")
            return
        buy_response = await api.buy({
            "buy": proposal_id,
            "price": stake_amount2
        })
        print(f"Trade successfully placed for {symbol}")
    except APIError as e:
        print(f"APIError while buying contract for {symbol}: {e}. Skipping trade...")
    except Exception as e:
        print(f"Unexpected error while buying contract for {symbol}: {e}. Skipping trade...")


# ====================
# WebSocket Connection
# ====================
async def connect():
    """Establish a WebSocket connection."""
    global CONFIG
    url = CONFIG["WEBSOCKET_URL"]
    print(f"Connecting to WebSocket at {url}")
    try:
        connection = await websockets.connect(url)
        print("WebSocket connection established successfully")
        return connection
    except Exception as e:
        print(f"Error connecting to WebSocket: {e}")
        return None


# ====================
# Main Logic
# ====================
async def main():
    global api, retry_attempts, CONFIG, heartbeat_task
    while True:
        try:
            connection = await connect()
            if not connection:
                print("Failed to establish WebSocket connection. Retrying...")
                continue
            api = DerivAPI(connection=connection)
            try:
                await api.authorize(CONFIG["API_TOKEN"])
                print("Authorized successfully!")
            except APIError as e:
                print(f"APIError during authorization: {e}. Retrying...")
                continue
            except Exception as e:
                print(f"Unexpected error during authorization: {e}. Retrying...")
                continue
                
            if heartbeat_task:
                heartbeat_task.cancel()
                try:
                    await heartbeat_task
                except asyncio.CancelledError:
                    print("Previous heartbeat monitor task cancelled.")

            heartbeat_task = asyncio.create_task(heartbeat_monitor())    

            for symbol in CONFIG["SYMBOLS"]:
                try:
                    tick_source: Observable = await api.subscribe({"ticks": symbol})
                    
                    def create_combined_callback(symbol):
                        def callback(data):
                            create_subscription_callback1(symbol)(data)
                            create_subscription_callback2(symbol)(data)
                        return callback
                    tick_source.subscribe(create_combined_callback(symbol))
                    print(f"Subscribed to {symbol}")
                except Exception as e:
                    print(f"Error subscribing to {symbol}: {e}")

            while True:
                await asyncio.Future()

        except Exception as e:
            retry_attempts += 1
            print(f"Unexpected error occurred: {e}. Attempting auto-reconnection... Attempt {retry_attempts}/{CONFIG['MAX_RETRIES']}")
            if retry_attempts >= CONFIG["MAX_RETRIES"]:
                print("Maximum retries reached. Waiting 10 seconds before resetting state and restarting...")
                await asyncio.sleep(10)
                await reset_state()
                retry_attempts = 0
                break
            continue


# ====================
# Entry Point
# ====================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("CTRL+C detected. Shutting down gracefully...")
        asyncio.run(reset_state())
        sys.exit(0)
 
