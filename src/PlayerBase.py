#
# Copyright 2019 Asutosh Nayak. All rights reserved.
#

"""
Abstract class to enforce 3T players to implement common operations
"""

from abc import ABC, abstractmethod


class PlayerBase(ABC):

	def __init__(self):
		super().__init__()

	@abstractmethod
	def make_move(self) -> int: # implementation would take a param: current "Board" instance
		pass

	@abstractmethod
	def match_over(self):
		pass

	@abstractmethod
	def next_match(self):
		pass




