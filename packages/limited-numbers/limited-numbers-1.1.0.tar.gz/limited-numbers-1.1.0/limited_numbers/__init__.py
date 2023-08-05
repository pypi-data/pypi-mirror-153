class Int:
	def __init__(self, limit: int, number: int=0, begin_from: int=0) -> None:
		self.number = number
		self.limit = limit
		self.begin_from = begin_from
		#also, check if number is overflowed
		self._handle_update()

	def _handle_update(self, input_number=None):
		'''Handles any number updates'''
		#save number as a local variable
		if input_number:
			local_number = input_number
		else:
			local_number = self.number
		
		#get the difference
		difference = self.limit-self.begin_from
		#divide to see how many times our number fits in difference
		fits = local_number//difference
		#update the number
		if local_number < self.begin_from:
			local_number -= fits*difference
		elif local_number > self.limit:
			local_number += fits*difference

		#check whether to save the non-overflowed number to self.number or just return it
		if not input_number:
			self.number = local_number
		else:
			return local_number

	#define a get function to return self.number (although user can just use Int.number instead)
	def get(self):
		'''You can use Int.number instead'''
		return self.number

	#Some functions to make addition and subtraction possible
	def __add__(self, other:int) -> int:
		return self._handle_update(self.number + other)

	def __radd__(self, other:int) -> int:
		return self._handle_update(self.number + other)
	
	def __iadd__(self, other:int) -> None:
		self.number += other
		self._handle_update()


	def __sub__(self, other:int) -> int:
		return self._handle_update(self.number - other)

	def __rsub__(self, other:int) -> int:
		return self._handle_update(self.number - other)
	
	def __isub__(self, other:int) -> None:
		self.number -= other
		self._handle_update()