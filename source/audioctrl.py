# Write your code here :-)

import board
import audiocore
import audiopwmio
import digitalio

from audiomp3 import MP3Decoder

class AudioCtrl:

	def __init__(self, sample):
		self.audio = audiopwmio.PWMAudioOut(board.GP18)
		self.sample = open(sample, "rb")
		self.decoder = MP3Decoder(self.sample)

	def playTrack(self):
		if not self.audio.playing:
			self.audio.play(self.decoder)
