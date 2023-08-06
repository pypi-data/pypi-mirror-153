class MySmoll:
	"""
	คลาส MySmoll คือ
	การเก็บข้อมูลของMySmoll

	Example
	#-------------------#
	MySmoll = MySmoll()
	MySmoll.show_name()
	MySmoll.show_art()
	#-------------------#
	"""
	def __in__(self):
		self.name = 'MySmoll'
		
	def show_name(self):
		print('สวัดฉันMySmoll {}'.format(self.name))

		def adout(self):
			text = """
			สวัดดีจ้าาผมMySmollยินดีที่ได้รู้จักผมชอบ
			เขียนโปรแกรมPython"""
			print(text)

def show_art(self):
	text = """
          ________  
      (( /========\
      __/__________\\____________n_
  (( /              \\_____________]
    /  =(*)=          \
    |_._._._._._._._._.|         !
(( / __________________ \\       =o
  | OOOOOOOOOOOOOOOOOOO0 |   = 
     __________________
  	"""
	print(text)


if __name__ == '__main__':
 	MySmoll = MySmoll()
	MySmoll.show_name()
	MySmoll.show_art()