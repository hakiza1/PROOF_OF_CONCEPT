(DRAFT)



# HAKIZA-1i (MMB-basic&lite)                                      




Section 0: General System Claim And Step-by-Step Algorithmic Diagram Descriptions 

(System Claim)

A computer-implemented trading system comprising:
- A data feed client configured to receive tick data from a financial market data API over a  WebSocket connection;
- A candle constructor configured to form artificial candles from sequences of tick data, each candle comprising a user-defined number of ticks;
- A synchronization engine configured to **skip randomly one or two or more incoming ticks after each completed candle**, thereby enforcing that any trading decision based on a completed candle is executed on a subsequent tick, aligning the system with real-world broker execution semantics;
- A state engine configured to monitor, for each of a plurality of financial assets, two or more independent trading strategies, including:
  - A non-reversal sequence detector that identifies a rare sequence (21 threshold or more consecutive candle directions is recommended),
  - A reversal sequence detector that identifies a rare sequence (21 threshold or more consecutive candle directions is recommended),
- A global activation controller configured to:
  - Set a global activation flag when one of the strategies detects a qualifying sequence (21 threshold can be recalibrated to lower or higher threshold),
  - Assign an active symbol and active strategy,
  - Prevent other strategies and symbols from executing trades while the global activation flag is set;
- A super-deterministic self-confirming trade-results via a win detector configured to determine a successful trade outcome based on the **break of the detected candle rare sequence**, without polling a trade result from the broker (suppressing any kind of latency);
- A martingale engine configured to apply a stake progression of `S *2.1^k` for `k = 0 to 6 from a 21 threshold`, where the progression is naturally self-limiting due to the statistical exhaustion of the sequence according to an exponential decay `II(n) = II(1) / 2^(n−1)`;
- A deactivation-control monitor configured to restart the syetem if the global lock is compromised;
- And a heartbeat monitor configured to fresh reboot the system if no tick data is received within a threshold period.





Informational INGOMA1
```
[Start]
   ↓
Receive Ticks
   ↓
Build Artificial Candles
   ↓
Detect Color Flip (Green ↔ Red)
   ↓
Increment Non-reversal Counter
   ↓
Is Non-reversal Count ≥ Threshold?
       ↘ No → Continue
         ↘ Yes → Add to Activation Pool
               ↘ Is Global Lock Active?
                     ↘ No → Random Selection
                           ↘ Activate Trade Engine
                                 ↘ keep up with the same Trade Type
                                       ↘ Increase Stake (×2.1)
                                             ↘ Execute Trade
                                                   ↘ Does Sequence Break?
                                                         ↘ Yes → Win + Reset
                                                         ↘ No → Continue
```






Informational INGOMA2  

Geometric e.g.: 
             
             /0\0/0\0/0\0/0\0/0\0/0\0/0\0/0\0/0\0/-1\+2.1 

```
[Start]
   ↓
Receive Ticks
   ↓
Build Artificial Candles
   ↓
Detect Color Flip (Green ↔ Red)
   ↓
Increment Reversal Counter
   ↓
Is Reversal Count ≥ Threshold?
       ↘ No → Continue
         ↘ Yes → Add to Activation Pool
               ↘ Is Global Lock Active?
                     ↘ No → Random Selection
                           ↘ Activate Trade Engine
                                 ↘ Alternate Trade Types
                                       ↘ Increase Stake (×2.1)
                                             ↘ Execute Trade
                                                   ↘ Does Sequence Break?
                                                         ↘ Yes → Win + Reset
                                                         ↘ No → Continue
```







Informational INGOMA3
```
[Start]
   ↓
Receive Ticks
   ↓
Build Artificial Candles
   ↓
Detect Color Flip (Green ↔ Red)
   ↓
Increment Non-reversal Counter
   ↓
Is Single-isolated-non-reversal-sequence Count ≥ Threshold?
       ↘ No → Continue
         ↘ Yes → Add to Activation Pool
               ↘ Is Global Lock Active?
                     ↘ No → Random Selection
                           ↘ Activate Trade Engine
                                 ↘ keep up with the same Trade Type
                                       ↘ Increase Stake (×2.1)
                                             ↘ Execute Trade
                                                   ↘ Does Sequence Break?
                                                         ↘ Yes → Win + Reset
                                                         ↘ No → Continue
```






Informational INGOMA4 

Geometric e.g: 

               /0    \0     /0    \0     /0    \0     /0    \0     /0    \0    /0       \0        /0   \0     /0     \0    /0     \0     /-1      \+2.1/...  

```
[Start]
   ↓
Receive Ticks
   ↓
Build Artificial Candles
   ↓
Detect Color Flip (Green ↔ Red)
   ↓
Increment Reversal Counter
   ↓
Is Single-isolated-reversal-sequence Count ≥ Threshold?
       ↘ No → Continue
         ↘ Yes → Add to Activation Pool
               ↘ Is Global Lock Active?
                     ↘ No → Random Selection
                           ↘ Activate Trade Engine
                                 ↘ Alternate Trade Types
                                       ↘ Increase Stake (×2.1)
                                             ↘ Execute Trade
                                                   ↘ Does Sequence Break?
                                                         ↘ Yes → Win + Reset
                                                         ↘ No → Continue
```






Informational INGOMA11
```
[Start]
   ↓
Receive Ticks
   ↓
Build Artificial Candles
   ↓
Detect Color Flip (Green ↔ Red)
   ↓
Increment Non-reversal Counter
   ↓
Is Multiple-isolate-non-reversal-sequence Count ≥ Threshold?
       ↘ No → Continue
         ↘ Yes → Add to Activation Pool
               ↘ Is Global Lock Active?
                     ↘ No → Random Selection
                           ↘ Activate Trade Engine
                                 ↘ Update Trade Type Accordingly
                                       ↘ Increase Stake (×2.1)
                                             ↘ Execute Trade
                                                   ↘ Does Sequence Break?
                                                         ↘ Yes → Win + Reset
                                                         ↘ No → Continue
```





Informational INGOMA12 

Geometric e.g.:

                \0/    \0/\/   \0/\   /0\    /0\/\   /0\/\/  /0\  /0\  /0\/   \0/\/  \0/  \0/\   /0\/  \0/\/\/\   /0\   /0\/\/   \0/\  /0\/  \-1/\/    \+2.1 


```
[Start]
   ↓
Receive Ticks
   ↓
Build Artificial Candles
   ↓
Detect Color Flip (Green ↔ Red)
   ↓
Increment Reversal Counter
   ↓
Is Multiple-isolated-reversal-sequence Count ≥ Threshold?
       ↘ No → Continue
         ↘ Yes → Add to Activation Pool
               ↘ Is Global Lock Active?
                     ↘ No → Random Selection
                           ↘ Activate Trade Engine
                                 ↘ Update Trade Type Accordingly
                                       ↘ Increase Stake (×2.1)
                                             ↘ Execute Trade
                                                   ↘ Does Sequence Break?
                                                         ↘ Yes → Win + Reset
                                                         ↘ No → Continue
```
---
 






# Line-by-Line Code Explanation for the the MMB-basic (the below explanation is almost the same as for the entire MMB-lite with some miner differences)


N.B.: FOR THE MMB-BASIC&LITE, THE DRY PRINCIPLE IS NOT TAKEN INTO CONSIDERATION ON PURPOSE (JUST FOR TESTING). 



Section 1: Secure Configuration and Imports

```python
import asyncio
from deriv_api import DerivAPI
from deriv_api import APIError
from rx import Observable
import os
import sys
import websockets
import random
from datetime import datetime, timedelta
```

> These imports provide:
> - `asyncio`: asynchronous execution for real-time market data
> - `DerivAPI`: connection to Deriv platform
> - `Observable`: reactive programming model for tick streams
> - `os`, `sys`: environment variable handling and process control
> - `websockets`: low-level WebSocket support
> - `random`: for selecting active symbol when multiple qualify
> - `datetime`, `timedelta`: for tracking activation windows

---

```python
DERIV_API_TOKEN = os.getenv('DERIV_TOKEN', '')
DERIV_WEBSOCKET_URL = os.getenv('WEBSOCKET_UR', '')
```

> These are secure credentials:
> - `DERIV_API_TOKEN`: fetched from environment variables for security
> - `DERIV_WEBSOCKET_URL`: connects to Deriv’s live market feed

---

```python
if len(DERIV_API_TOKEN) == 0:
    print("DERIV_API_TOKEN environment variable is not set. Exiting...")
    sys.exit(1)
```

> Ensures the bot fails safely if no token is provided

---

```python
CONFIG = {
    "SYMBOLS": ["1HZ10V", "1HZ25V", ..., "JD100"],  
    "CANDLE_DURATION": 4,
    "MAX_RETRIES": 3,
    "API_TOKEN": DERIV_API_TOKEN,
    "WEBSOCKET_URL": DERIV_WEBSOCKET_URL
}
```

> Central configuration block:
> - List of symbols traded (synthetic indices)
> - Candle duration in ticks
> - Max retry attempts on connection loss
> - Token and URL reused from earlier

---

```python
SYMBOL_STATES = {
    symbol: {
        "last_candle_open": None,
        "last_candle_close": None,
        "current_candle_ticks": [],
        "reversal_count": 0, # non-reversal_count for informational INGOMA1
        ...
    }
    for symbol in CONFIG["SYMBOLS"]
}
```

> State tracking per symbol:
> - Tracks open/close prices
> - Stores ticks for building candles
> - Tracks reversal or non-reversal count
> - Flags for sequence start (green/red)
> - Martingale logic state

---

```python
retry_attempts = 0
GLOBAL_SEQUENCE_ACTIVE = False
ACTIVE_SYMBOL = None 
INACTIVE_SYMBOL = None
ACTIVATION_CANDIDATES = []
LAST_ACTIVATION_TIME = None
ACTIVATION_WINDOW = timedelta(seconds=2)
```

> Global flags:
> - Prevents overlapping trades
> - Tracks which symbol is currently active
> - Manages activation window (prevents race conditions)
> - Limits trade to one symbol at a time

---






Section 2: Helper Functions

```python
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
```

> Resets all state variables across symbols.
> - Called after a sequence ends or on error
> - Ensures clean state before new reversal detection for informational INGOMA2 or new non-reversal detection for informational INGOMA1

---

```python
def create_subscription_callback2(symbol):
    def callback(data):
        try:
            if "tick" in data:
                asyncio.create_task(handle_tick2(symbol, data))
        except Exception as e:
            print(f"Error in subscription callback for {symbol}: {e}")
    return callback
```

> Creates a unique tick handler per symbol.
> - Wraps async function inside sync context
> - Routes incoming ticks to correct symbol processing

---

```python
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
```

> Core tick-handling logic:
> - Skips next tick after completing a candle (to avoid overlap and ensure synchronization for  deterministic  self-confirming trade results without unnecessary additional latency caused by API calls while polling the result from brokers)
> - Builds artificial candles from raw ticks
> - The last skipped tick becomes first tick of new candle
> - When candle is full → it locks each symbol to avoid any kind of interference between their incoming ticks → triggers `process_candle()`
> - Sets skip flag for next tick

---








Section 3: Reversal Detection Logic

```python
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
            if GLOBAL_SEQUENCE_ACTIVE and ACTIVE_SYMBOL == symbol and prev_count2 >= 19:  # The threshold can be increased to any odd number for safety
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
                if state["reversal_count2"] >= 19:  # The threshold can be increased to any odd number for safety
                    ACTIVE_BOT = "BOT2"
                    INACTIVE_BOT = [s for s in CONFIG["BOTS"] if s != ACTIVE_BOT]
                    await activate_symbol(symbol)

    except Exception as e:
        print(f"Error detecting reversals for {symbol}: {e}")
```

> This is where the **pattern recognition magic happens**:
> - Detects color flips (green ↔ red)
> - Increments reversal counter only on alternating colors, in case of informational INGOMA2
> - Increments non-reversal counter only on same consecutive colors, in case of informational INGOMA1
> - Resets reversal counter on same-color streak (meaning the sequence breaks, the trade was a winning final step of the martingale, reset and wait...)
> - Resets non-reversal counter on different-color streak (meaning the sequence breaks, the trade was a winning final step of the martingale, reset and wait...)
> - Once count ≥ 19 (can be recalibrated to a higher very secure or a lower less secure threshold, and must be the same as the threshold in section 4, for testing just set the threshold to ≥ 1):
>   - Adds symbol to activation pool
>   - Random selection among qualifying symbols
>   - Enforces activation window to prevent conflicts
> - Ensures only one symbol is active at a time

---








Section 4: Candle Processing

```python
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

        if state["reversal_count2"] == 19:  # The threshold can be increased to any odd number for safety
            if state["is_sequence_starting_with_green2"]:
                state["trade_type2"] = "CALLE"
                state["stake_amount2"] = 1
                state["previous_stake_amount2"] = state["stake_amount2"]
            elif state["is_sequence_starting_with_red2"]:
                state["trade_type2"] = "PUTE"
                state["stake_amount2"] = 1
                state["previous_stake_amount2"] = state["stake_amount2"]
                
        elif state["reversal_count2"] > 19:  # The threshold can be increased to any odd number for safety
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
```

> Full candle analysis:
> - Determines candle color (green = up, red = down)
> - Calls reversal counter using `detect_reversals()` for informational INGOMA2 or Calls non-reversal using `detect_non_reversals()` for INGOMA1
> - At count ≥ 19 (can be recalibrated to a higher very secure or a lower less secure threshold, and must be the same as the threshold in section 3; if a chosen threshold is an even number then interchange trade_types to allow the breaking sequence to remain a winning final step of the martingale, the interchange may not be necessary for other different patterns like in the non-reversal sequences case; for testing just set the threshold to ≥ 1):
> - Starts placing trades
> - Alternates trade types for the informational ingoma2
> - Keep up with the same trade type for the informational ingoma1
> - Increases stake ×2.1 per step
> - Win occurs **only when reversal or non-reversal sequence breaks**
> - Losses happen **while reversal  or non-reversal sequence continues**
> - Store trade info for execution during first skipped tick (if more than 1 tick is to be skipped)
> - But long sequences are rare and always end up breaking (in real world, the longest sequence are about mostly 21-25, which means 7-9 steps max are secure from a threshold of 19) → losses are theoretically improbable and practically rare unless there is either a bug or data integrity violation (very easy to detect)... Note that any other kind of system failure may occur (while using an EC2 private server from amzonAWS, such kind of failure unlikely happens)

---
 






Section 5: Trade Execution

```python
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
```

> Places binary options via Deriv API:
> - Proposes trade
> - Extracts proposal ID
> - Executes trade with increasing stake
> - Logs success/failure

---





Section 6: WebSocket Connection and Main Loop

```python
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
```

> Establishes live connection to Deriv WebSocket endpoint

---

```python
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
```

> Main loop:
> - Handles reconnection logic
> - Authorizes and subscribes to tick data
> - Processes ticks indefinitely
> - Gracefully resets on failure

---

```python
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("CTRL+C detected. Shutting down gracefully...")
        asyncio.run(reset_state())
        sys.exit(0) 
```

> Entry point:
> - Starts the bot
> - Handles keyboard interrupt for graceful shutdown

---






# WARNING: 

Retail Brokers sometimes won't even shy from messing up with demo accounts just for anticipation...Imagine a second what they can do with your real account (real trading with retail brokers is not recommended):

For instance, the MMB-lite with 19 as a threshold will yield more than 10 trades per day requiring enough initial portfolio to withstand 9 martingale steps for the MMB to remain unbeatable... Depending on the available initial portfolio, one can lower the threshold to even 1, sure for test.
But bear in your mind that "increasing the threshold means a decrease of trades per day and a small initial portfolio to withstand decreased martingale steps, very safe and recommended"; on contrary, "decreasing the threshold means an increase of trades per day and a huge initial portfolio to withstand increased martingale steps, less safe and not recommended" (that is the reason why the MMB isn't a get-rich-overnight).

But here is the trick, the MMB-lite will perform well for few days on platforms like Deriv and suddenly out of nowhere it might start misbehaving (its built-in heartbeat or lock-control may even start to be triggered constantly after few minutes); it just means your retail broker has realized your strategy is unbeatable which is enough for your account to be flagged ... I'm not making this up or trying to denigrate anyone, it is beyond any doubt that if you pay a little bite of your attention to the flow of ticks and trade executions, you will start witnessing interruptions and manipulative actions from your retail broker disrupting and violating data-integrity & trade-executions... So, unless you have enough paranoia  and know what the hell you're up to and the risk you're taking, please make sure you are using a demo account or use any other kind of simulator just for educational purpose (this is for educators and regulatory entities).

That said, for risk takers, you can have the ready to go MMB-extra and its user-guide, improved enough to challenge retail brokers'paranoia and take the win for a short period of time... Can only be accessed via an invitation (if you are willing to pay for an access, reach us via the email mentioned below).



# N.B.:

# The redundancy within the present MMB python scripts is simply by design to favor robust precision and easier logging_debugging for educational purpose
# While the MMB  (basic & lite) scripts are running especially for the 1 tick skipping scenario, after each placed trade one may notice a "CurrentTime or pending future error", although it causes no harm it has to be addressed for real trading (the DRY-PRINCIPLE must be taken into consideration).
# For more details, see the theory for both the informational and mechanical versions of the Universal-Mutation.




# RUN YOUR OWN TEST AND EMBRACE THE FACTS                                       hakiza1@proton.me

