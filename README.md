# gag
voice assistant using chatgpt + assemblyai speech recognition on raspberry pi 

the reason i chose not to work with google speech recognition, for some reason it was harder to implement on the pi 3 b. assemblyai proved to be way easier to use. granted both APIs (chagtgpt & assemblyai speech-to-text) are paid for but no crazy ammount, 10$ should be enough if you just wanna do your demo for a school project.


what you first need is to configure your hardware, Raspbian sometimes doesn't detect the usb microphone so you need to manually add it to the .asoundrc file:
first start with updating your OS

   sudo apt update
   sudo apt upgrade

run the following command to list all of the recording devices:
   arecord -l
this will output the recording device number and card number, remember these values

now modify the alsa config file
   nano /home/pi/.asoundrc
   
and add the following lines

pcm.!default {
  type asym
  capture.pcm "mic"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:[card number],[device number]"
  }
}
save the configuration by clicking CTRL+X, Y, then ENTER.
what this does is configure the default PCM (Pulse Code Modulation) device. The type asym indicates asymmetric operation, and capture.pcm "mic" specifies that the default capture device is named "mic."
additionally you are defining a PCM named "mic." It uses the type plug configuration, which is a plugin that can be used to adapt one PCM interface to another. The slave block specifies the actual hardware configuration with pcm "hw:[card number],[device number]". You need to replace [card number] and [device number] with the appropriate values for your sound card and device.

now head over to the official assemblyai website in order to generate your token key. sign up and choose a payment plan starting as low as 5$ (come on its worth it lol) BUT if memory serves well i think assembly ai does offer a trial or a specific ammount of words that api will transcribe using input speech before you have to actually pay for anything... i think.

same thing for chatgpt, get your token key for the api.

to output the sound you can use whatever screen you have your pi plugged up into through hdmi display but for the purposes of my project (which was a four wheel mobile robot) i had to use a bluetooth module, i had a speaker laying around that i dismantled. but thats for later.

