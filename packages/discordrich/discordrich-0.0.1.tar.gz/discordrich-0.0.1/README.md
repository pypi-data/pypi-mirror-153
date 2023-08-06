# About   
Discord Rich is a Discord RPC library.   
   
# Installation   
`pip install discordrich`

# Examples   
```
# Import DiscordRich
from discordrpc import *
import time

RPC = Presence('clientid')

# Start RPC Client
RPC.connect()

# Update RPC
RPC.update(state="Rich Presence using DiscordRich!")

while True:  # The presence will stay on as long as the program is running
    time.sleep(15) # Can only update rich presence every 15 seconds
```

# Syntax
## Presence
Update:
```
RPC.update(state)
RPC.update(start) 
RPC.update(large_image)   
RPC.update(small_image)   
RPC.update(party_id)   
RPC.update(join)   
RPC.update(match)
RPC.update(instance)
```

Connect:
```
RPC.connect()
```

Close:
```
RPC.close()
```
Clear:
```
RPC.clear()
```