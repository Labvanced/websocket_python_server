#!/usr/bin/python   
# Labvanced External Device Synchronization Example.

# This server waits to receive a "hello" message from a running experiment.
# After receiving a "hello" it sends back a "world" message to the running experiment.
# The received payload variable is bounced back to the running experiment.

# The following packages must be installed on your system
import asyncio
import json
import websockets

async def on_connect(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
            # data has two fields 'msg' and 'data'. msg is the trigger / message, value is the variable value, both
            # defined in the 'send external trigger action' in your Labvanced experiment.
            received_value = data['value']
            received_msg = data['msg']

            # here you can make an if-elif for each of your triggers and depending on the type execute different code
            if received_msg == 'hello':
                # at this location you could add some code to send a trigger to an external device
                print("msg = {}, received_value = {}".format(received_msg, received_value))

                # this is how you send messages back to the Labvanced player. Specify a 'msg' field, which can be used
                # as a trigger and optionally send some data in the 'value' field. Depending on your application this
                # code can / should be placed at a different location.
                send_value = received_value
                await websocket.send(json.dumps({'msg': 'world', 'value': send_value}))
            elif received_msg == 'anotherTrigger':
                # do something else here
                print("another trigger was received")
            else:
                # unsupported trigger
                print("unsupported event: {}".format(data))
    finally:
        print("connection lost")

# Make sure that the IP address and port match with the Labvanced study settings.
asyncio.get_event_loop().run_until_complete(websockets.serve(on_connect, 'localhost', 8081))
asyncio.get_event_loop().run_forever()