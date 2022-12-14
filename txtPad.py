#  Copyright 2022 Mahid
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY
import pickle
import pygame,sys,time
from pygame.locals import*
pygame.init()
clock=pygame.time.Clock()
w=1000
h=600


screen=pygame.display.set_mode((w,h),FULLSCREEN|HWSURFACE)
#screen=pygame.display.set_mode((w,h),pygame.NOFRAME)
#screen=pygame.display.set_mode((w,h),RESIZABLE)
pygame.display.set_caption("txtPad")

then=time.time()

pulse='|'
try:
	#Read Data
	with open('UserData.pickle', 'rb') as data:
		all_data= pickle.load(data)
		data.close()
except:
	#Write Data
	with open('UserData.pickle', 'wb') as data:
		txt=''
		font_size=32
		all_data=[]
		all_data.append(txt)
		all_data.append(font_size)
		pickle.dump(txt, data)
		data.close()


txt=all_data[0]
font_size=all_data[1]
text_line_height=0
total_text_line_height=0

total_page=0
n=0
pygame.mouse.set_visible(1)
writing=True



class TextView():
	def __init__(self,screen,text='',t_x=0,t_y=0,t_w=200,t_h=400,text_color="#666666",pulse=''):
		self.screen=screen
		self.t_x=t_x
		self.t_y=t_y
		self.t_w=t_w
		self.t_h=t_h
		self.text_color=text_color 
		self.text=text+pulse
		self.text_font=pygame.font.Font('Prata-Regular.ttf',font_size)
		self.text_lines=[]
		self.splitted_lines=self.text.splitlines()
		for splitted_line in self.splitted_lines:
			if self.text_font.size(splitted_line)[0] > self.t_w:
				words = splitted_line.split(' ')
				fitted_line=""
				for word in words:
					test_line = fitted_line + word + " "
					if self.text_font.size(test_line)[0] < self.t_w:
						fitted_line = test_line
					else:
						self.text_lines.append(fitted_line)
						fitted_line = word + " "
				self.text_lines.append(fitted_line)
			else:
				self.text_lines.append(splitted_line)
		
		text_row=self.t_y
		try:
			global text_line_height
			text_line_height=(self.text_font.size("")[1])
			global total_text_line_height
			total_text_line_height=text_line_height*(len(self.text_lines)-1)
		except:
			pass


		for line in self.text_lines:
			if line != "":
				text_surface = self.text_font.render(line, 1, self.text_color)
				if all_select==True:
					first_line=(self.text_font.render(self.text_lines[0], 1, self.text_color)).get_rect()
					txt_rect=text_surface.get_rect()
					txt_rect=(self.t_x,self.t_y,txt_rect[2],txt_rect[3])
					pygame.draw.rect(screen,"#ccffcc",txt_rect)
				self.screen.blit(text_surface, (self.t_x, self.t_y))
			self.t_y +=self.text_font.size(line)[1]

			
all_select=False
game_running=True
Next_line=False

page=1

constant_h=text_line_height
while game_running:
	clock.tick(60)
	txt_surface=pygame.Surface((w,total_text_line_height+100))
	for event in pygame.event.get():
		if event.type==QUIT:
			with open('UserData.pickle', 'wb') as data:
				updateData=[]
				updateData.append(txt)
				updateData.append(font_size)
				pickle.dump(updateData, data)
				data.close()
			time.sleep(.2)
			pygame.display.iconify()
			time.sleep(.5)
			pygame.quit()
			sys.exit()
		if event.type==pygame.VIDEORESIZE:
			w,h=event.size
		if event.type==pygame.TEXTINPUT:
			txt+=event.text
			all_select=False
			
			
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_BACKSPACE:
				pygame.key.set_repeat(200,5)
				if len(txt)==0:
					pass
				else:
					txt=txt[:-1]
				if all_select==True:
					txt=''
					all_select=False
			if event.key==pygame.K_ESCAPE:
				with open('UserData.pickle', 'wb') as data:
					updateData=[]
					updateData.append(txt)
					updateData.append(font_size)
					pickle.dump(updateData, data)
					data.close()
				pygame.display.iconify()
				pygame.quit()
				sys.exit()
				
					
			if event.key==pygame.K_a:
				if event.mod == pygame.KMOD_NONE:
					continue
				else:
					if event.mod & pygame.KMOD_LCTRL:
						all_select=True
			if event.key==pygame.K_z:
				if event.mod == pygame.KMOD_NONE:
					continue
				else:
					if event.mod & pygame.KMOD_LCTRL:
						if font_size<70:
							font_size+=5
						else:
							font_size=22	
			elif event.key==pygame.K_v:
				if event.mod == pygame.KMOD_NONE:
					continue
				else:
					if event.mod & pygame.KMOD_LCTRL:
						pygame.scrap.init()
						text=pygame.scrap.get("text/plain")
						if text:
							text=(text.decode('ascii', 'ignore'))
							text=text[:-1]
							txt=txt+text

							
			elif event.key==pygame.K_c:
				if event.mod == pygame.KMOD_NONE:
					continue
				else:
					if event.mod & pygame.KMOD_LCTRL:
						pygame.scrap.init()
						txt_clipboard=bytes(txt, 'utf-8')
						pygame.scrap.put(pygame.SCRAP_TEXT, txt_clipboard)
						
						
			elif event.key==pygame.K_RETURN:
				Next_line=True
				
			elif event.key==pygame.K_HOME:
				writing=False
				page=1
				n=0
			elif event.key==pygame.K_PAGEUP:
				writing=False
				if 0<page<=total_page:
					page-=1
					n=-(page*(h))
					
			elif event.key==pygame.K_PAGEDOWN:
				writing=False
				if page<total_page:
					page+=1
					n=-(page*(h))
					
			elif event.key==pygame.K_END:
				writing=False
				page=total_page
				n=-(page*(h))
				
	
	now=time.time()
	d=now-then
	if d>=1 and d<=2:
		then=now
		pulse=''
	else:
		pulse='|'
	if Next_line==True:
		txt=txt+'\n'
		Next_line=False
	screen.fill('#242424')
	TextView(txt_surface,text=txt,t_x=20,t_y=10,t_w=w-50,t_h=total_text_line_height+100,pulse=pulse,text_color='#696969')

	t_h=total_text_line_height
	n_p=t_h//h
	total_page=n_p
	if writing==True:	
		if n_p>page:
			page+=1
			n=-(page*(h))
		elif n_p<page:
			page=n_p
			n=-(page*(h))
	screen.blit(txt_surface,(0,n))
	pygame.display.update()
