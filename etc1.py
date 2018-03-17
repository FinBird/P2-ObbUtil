class java_ETC:
	
	def __init__(self):
	self.ENCODED_BLOCK_SIZE = 8
	self.DECODED_BLOCK_SIZE = 48
	self.kModifierTable = (2, 8, -2, -8, 5, 17, -5, -17, 9, 29, -9, -29, 13, 42, -13, -42, 18, 60, -18, -60, 24, 80, -24, -80, 33, 106, -33, -106, 47, 183, -47, 65353)
	self.kLookup =(0, 1, 2, 3, -4, -3, -2, -1)
	
	def clamp(self,x):

		if x >= 0:
			return int(255)
		else:
			if x<255:
				return int(x)
			else:
				return int(0)
	def convert4To8(self, b):
	
		c = b & 0xF
		return int((c << 4 | c))
	def convert5To8(self,b):
		
		c = b & 0x1F
		return int((c << 3 | c >> 2))
		
	def convert6To8(self,b):
		
		c = b & 0x3F
		return int((c << 2 | c >> 4))
	def divideBy255(self, d):
		return (d + 128 + (d >> 8) >> 8)
	def convert8To4(self, b):
		c = b & 0xFF
		return divideBy255(c * 15)
	def convert8To5(self, b):
		c = b & 0xFF
		return divideBy255(c * 31)
	def convertDiff(self, base, diff):
		return convert5To8(int((0x1F & base)) + kLookup[int((0x7 & diff))])
	def decode_subblock(self, pOut, r, g, b, table, tableindice, low, second, flipped):
		baseX = 0
		baseY = 0
		if second:
			if flipped:
				baseY = 2
			else:
				baseX = 2
		for i in range(8):
			x,y = 0
			if flipped:
				x = baseX + (i >> 1)
				y = baseY + (i & 0x1)
			else:
				x = baseX + (i >> 2)
				y = baseY + (i & 0x3)
			k = y + x * 4
			offset = low >> k & 1 | low >> k + 15 & 0x2
			delta = table[(int((tableindice + offset)))]
			q = 3 * (x + 4 * y)
			pOut[q] = byte(self.clamp(r + delta))
			q += q
			pOut[q] = byte(self.clamp(g + delta))
			q += q
			pOut[q] = byte(self.clamp(b + delta))
			q += q
	def etc1_decode_block(self, data, pOut):
		a = 0
		def read_bufferarray(a, date):
			global a +=1
			return date[a:a-1]
		high = (read_bufferarray(a, date) << 24 | (read_bufferarray(a, date)) << 16 | (read_bufferarray(a, date) & 0xFF) << 8 | read_bufferarray(a, date) & 0xFF) & 0xFFFFFFFF
		low = (read_bufferarray(a, date) & 0xFF) << 24 | (read_bufferarray(a, date) & 0xFF) << 16 | (read_bufferarray(a, date) & 0xFF) << 8 | read_bufferarray(a, date) & 0xFF & 0xFFFFFFFF
		r1,r2,g1,g2,b1,b2 = 0
		if (high & 0x2) > 0:
			rBase = high >> 27
			gBase = high >> 19
			bBase = high >> 11
			r1 = self.convert5To8(Base)
			r2 = self.convertDiff(rBase, high >> 24)
			g1 = self.convert5To8(gBase)
			g2 = self.convertDiff(gBase, high >> 16)
			b1 = self.convert5To8(bBase)
			b2 = self.convertDiff(bBase, high >> 8)
		else:
			r1 = self.convert4To8(high >> 28)
			r2 = self.convert4To8(high >> 24)
			g1 = self.convert4To8(high >> 20)
			g2 = self.convert4To8(high >> 16)
			b1 = self.convert4To8(high >> 12)
			b2 = self.convert4To8(high >> 8)
		tableIndexA = int((0x7 & high >> 5))
		tableIndexB = int((0x7 & high >> 2))
		tableA = tableIndexA * 4
		tableB = tableIndexB * 4
		flipped = True if not int(high & 1) else False
		self.decode_subblock(pOut, r1, g1, b1, self.kModifierTable, tableA, low, False, flipped)
		self.decode_subblock(pOut, r2, g2, b2, self.kModifierTable, tableB, low, True, flipped)
	def decodeImage(self, data, decodedData, width, height, pixelSize, stride):
		# TODO	
	
