"""
Abstract class to enforce 3T players to implement common operations
"""

from abc import ABC, abstractmethod

class PlayerBase(ABC):

	def __init__(self):
		super().__init__()

	@abstractmethod
	def make_move(self): # implementation would take a param: current "Board" instance
		pass




