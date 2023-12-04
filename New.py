import pyaudio
import websockets
import asyncio
import base64
import json
from playsound import playsound
import subprocess
import openai
import pyttsx3
import time

auth_key = 'XXXXXXXXXXXXXXXX'#assemblyai token
openai.api_key = 'XXXXXXXXXXXXXXXXXX'#openai-chatgpt3.5-token

WAKE_WORD = "Hey Rico"
L_STREAM = "launch stream"
S_STREAM = "stop stream"

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

engine = pyttsx3.init()
engine.setProperty('rate', 160)
messages = [ {"role": "system", "content": "You are an intelligent assistant."} ]

# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# the AssemblyAI endpoint we're aiming to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
# oo is my main function for chatgpt interaction, the message is what's going to be eventually speech transcribed into text, passed to chatgpt as an input
def oo(message):
    
    messages.append(
    {"role": "user", "content": message}, #appending new messages for added context
    )
    chat = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=messages
    )
    reply = chat.choices[0].message #Extracts the assistant's reply from the response received from the OpenAI API assuming the first choice in the response contains the generated message.
    print("Rico: ", reply.content)  #this is helpful to detect whether or not your script is running during your terminal view
    engine.say(reply.content) #audio output using pyttsx3
    engine.runAndWait() #This ensures that the speech output is completed before moving on.
    messages.append(reply)

async def send_receive():#establishes a WebSocket connection used for sending and receiving speech for real-time transcription.
   print(f'Connecting websocket to url ${URL}')
   async with websockets.connect( 
       URL,
       extra_headers=(("Authorization", auth_key),),
       ping_interval=5,
       ping_timeout=20
   ) as _ws:
       await asyncio.sleep(0.1)
       print("Receiving SessionBegins ...")
       session_begins = await _ws.recv()
       print(session_begins)
       print("Sending messages ...")
       async def send():
           while True:
               try:
                   data = stream.read(FRAMES_PER_BUFFER)
                   data = base64.b64encode(data).decode("utf-8")
                   json_data = json.dumps({"audio_data":str(data)})
                   await _ws.send(json_data)
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
               await asyncio.sleep(0.01)

           return True

       async def receive():
           while True:
               try:
                   result_str = await _ws.recv()
                   text = json.loads(result_str)['text']
                   
                   if json.loads(result_str)['message_type']=='FinalTranscript':
                      print(text)
                      if text == 'Rico.' and presult!='':
                        
                        oo(presult)
                      presult = text 
                        
                        
                   elif L_STREAM.lower() in text.lower():
                         terminal_process = subprocess.Popen(['lxterminal','-e','bash','-c', "python3 /home/ziggy/pi-camera-stream-flask/main.py"])
                         
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"

       send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())