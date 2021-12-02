import board
import audiocore
import audiopwmio
import digitalio

from audiomp3 import MP3Decoder

audio = audiopwmio.PWMAudioOut(board.GP18)
mp3 = open("digivolve.mp3", "rb")
decoder = MP3Decoder(mp3)
decoder.file = open("digivolve.mp3", "rb")

i = 0

while True:
        # Updating the .file property of the existing decoder
        # helps avoid running out of memory (MemoryError exception)
        if !audio.playing(){
        	audio.play(decoder)
        }
        print("playing" + str(i))

        # This allows you to do other things while the audio plays!
        while audio.playing:
            print("still goin")
            pass


