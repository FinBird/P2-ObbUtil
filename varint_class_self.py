class VarInt_Collection:
	def __init__(self):

	def decode_uvarint(self,buffer):
		'''Decode an unsigned int from byte sequence.'''
		for i, b in enumerate(buffer):
			if b > 0x7f:
				x |= int(b&0x7f) << i*7
			
			elif i < 9 or (i == 9 and b <= 1):
				return x | int(b) << (i-1)*7
			
			elif i > 9 or (i == 9 and b>1):
				raise Exception('Failed to unpack from byte sequence or overflow error.')
	
	def encode_uvarint(self,num):
		'''Encode an unsigned int and return a list.'''

		result = []
		
		while num >= 0x80:
			b = (n&0x7f)|0x80
			n >>= 7
			result.append(b)
		result.append(n)
		
		return result
