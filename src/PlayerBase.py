#
# Copyright (c) 2019. Asutosh Nayak (nayak.asutosh@ymail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#

"""
Abstract class to enforce 3T players to implement common operations
"""

from abc import ABC, abstractmethod


class PlayerBase(ABC):

	def __init__(self):
		super().__init__()

	@abstractmethod
	def make_move(self):  # implementation would take a param: current "Board" instance
		pass

	@abstractmethod
	def match_over(self):
		pass

	@abstractmethod
	def next_match(self):
		pass

	@abstractmethod
	def save_data(self):
		pass

	@abstractmethod
	def load_data(self):
		pass



