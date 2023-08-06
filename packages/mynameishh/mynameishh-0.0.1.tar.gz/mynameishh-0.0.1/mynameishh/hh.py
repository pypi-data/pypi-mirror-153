# hh.py

class HH:
	'''
	คลาส HH คือ
	ข้อมูลที่เกี่ยวข้องกับ hh
	ประกอบด้วย
	ชื่อ
	อายุ
	'''
	def __init__(self):
		self.name = 'hh'
		self.age = '10000 yrs'

	def show_name(self):
		print('สวัสดี เราชื่อ {}'.format(self.name))

	def show_age(self):
		print('เราอายุ {}'.format(self.age))

	def about (self):
		text = '''
		--------------------------------
		สวัสดีงับ เราชื่อ hh เป็นคนเขียนไลบรารี่นี้เอง
		คนที่เห็นข้อความเป็นคนรู้เรื่องคอมดีแน่ ๆ เลย
		มาเขียนโปรแกรมไปด้วยกันนะงับ
		--------------------------------
		'''
		print(text)

	def show_art(self):
		text = '''
                  .----.
      .---------. | == |
      |.-"""""-.| |----|
      ||       || | == |
      ||       || |----|
      |'-.....-'| |::::|
      `"")---(""` |___.|
     /:::::::::::\" _  "
    /:::=======:::\`\`\n
jgs `"""""""""""""`  '-'
		'''
		print(text)

if __name__ == '__main__':
	friend = HH()
	friend.show_name()
	friend.show_age()
	friend.about()
	friend.show_art()






