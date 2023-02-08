#  Copyright 2022-2023 Mahid
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY
import pickle
import os
import pygame,sys,time
from pygame.locals import*
pygame.init()
clock=pygame.time.Clock()
then=time.time()

pulse='|'


path = os.path.expanduser('~\Documents\\01one\ txtPad\TaskData.pickle')


try:
	with open(path, 'rb') as data:
		all_data= pickle.load(data)
		data.close()
except:
	text_data=os.path.expanduser('~\Documents\\01one\ txtPad')
	if not os.path.exists(text_data):
		os.makedirs(text_data)
	with open(path, 'wb') as data:
		txt=''
		font_size=30
		all_data=[]
		all_data.append(txt)
		all_data.append(font_size)
		pickle.dump(txt, data)
		data.close()


txt=all_data[0]
font_size=all_data[1]
w=1000
h=650
screen=pygame.display.set_mode((w,h),FULLSCREEN|HWSURFACE)
pygame.display.set_caption("txtPad")
icon=pygame.image.load('txtPad.png')
pygame.display.set_icon(icon)
writing=True


TOTAL_PAGE_NUMBER=1
CURRENT_PAGE=TOTAL_PAGE_NUMBER
RENDER_LINE_HEIGHT=100
START_LINE=1

text_font=pygame.font.Font('Prata-Regular.ttf',font_size)
pygame.mouse.set_visible(False)

def render_text_list(text,t_w,text_font):
	text_lines=[]
	splitted_lines=text.splitlines()
	for splitted_line in splitted_lines:
		if text_font.size(splitted_line)[0] >t_w:
			words = splitted_line.split(' ')
			fitted_line=""
			for word in words:
				test_line = fitted_line + word + " "
				if text_font.size(test_line)[0] <t_w:
					fitted_line = test_line
				else:
					text_lines.append(fitted_line)
					fitted_line = word + " "
			text_lines.append(fitted_line)
		else:
			text_lines.append(splitted_line)
	return text_lines


def render(screen,render_lines,text_font,t_x,t_y,text_color,all_select):
	for line in render_lines:
		if line != "":
			text_surface = text_font.render(line, 1, text_color)
			if all_select==True:
				txt_rect=text_surface.get_rect()
				txt_rect=(t_x,t_y,txt_rect[2],txt_rect[3])
				pygame.draw.rect(screen,"#ccffcc",txt_rect)
			screen.blit(text_surface, (t_x, t_y))
		t_y +=text_font.size(line)[1]


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
		self.text_lines=render_text_list(self.text,t_w,self.text_font)

		global CURRENT_PAGE,TOTAL_PAGE_NUMBER,RENDER_LINE_HEIGHT,START_LINE
			
		text_line_height=(self.text_font.size("")[1])
		total_text_line_height=text_line_height*(len(self.text_lines))	
		
		t_h=total_text_line_height
		EACH_PAGE_CAPACITY=h//text_line_height
		TOTAL_LINE_NUMBER=len(self.text_lines)
		TOTAL_PAGE_NUMBER=(TOTAL_LINE_NUMBER//EACH_PAGE_CAPACITY)+1
		
		if writing:
			CURRENT_PAGE=TOTAL_PAGE_NUMBER
			
		else:
			CURRENT_PAGE=CURRENT_PAGE
		if CURRENT_PAGE==1:
			START_LINE=1
		elif TOTAL_PAGE_NUMBER-1>0:
			START_LINE=(CURRENT_PAGE-1)*EACH_PAGE_CAPACITY

		END_LINE=CURRENT_PAGE*EACH_PAGE_CAPACITY
		render_lines=self.text_lines[START_LINE-1:END_LINE]
		RENDER_LINE_HEIGHT=text_line_height*len(render_lines)
		render(self.screen,render_lines,self.text_font,self.t_x,self.t_y,self.text_color,all_select)
		

all_select=False
Next_line=False

while 1:
	clock.tick(60)
	pygame.draw.rect(screen,"#000000",(0,0,w,RENDER_LINE_HEIGHT+100))
	for event in pygame.event.get():
		if event.type==QUIT:
			with open(path, 'wb') as data:
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
			CURRENT_PAGE=TOTAL_PAGE_NUMBER
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
				CURRENT_PAGE=TOTAL_PAGE_NUMBER
			if event.key==pygame.K_ESCAPE:
				with open(path, 'wb') as data:
					updateData=[]
					updateData.append(txt)
					updateData.append(font_size)
					pickle.dump(updateData, data)
					data.close()
				pygame.display.iconify()
				pygame.quit()
				sys.exit()
				
					
			if event.key==pygame.K_a:
				if event.mod & pygame.KMOD_LCTRL:
					all_select=True
			if event.key==pygame.K_z:
				if event.mod & pygame.KMOD_LCTRL:
					if font_size<70:
						font_size+=10
					else:
						font_size=20	


			elif event.key==pygame.K_v:
				if event.mod & pygame.KMOD_LCTRL:
					pygame.scrap.init()
					text=pygame.scrap.get("text/plain")
					if text:
						text=(text.decode('ascii', 'ignore'))
						text=text[:-1]
						txt=txt+text

							
			elif event.key==pygame.K_c:
				if event.mod & pygame.KMOD_LCTRL:
					pygame.scrap.init()
					txt_clipboard=bytes(txt+' ', 'utf-8')
					pygame.scrap.put(pygame.SCRAP_TEXT, txt_clipboard)
						
						
			elif event.key==pygame.K_RETURN:
				Next_line=True
			elif event.key==pygame.K_HOME:
				writing=False
				CURRENT_PAGE=1
			elif event.key==pygame.K_PAGEUP:
				writing=False
				if 1<CURRENT_PAGE<=TOTAL_PAGE_NUMBER:
					CURRENT_PAGE-=1

					
			elif event.key==pygame.K_PAGEDOWN:
				writing=False
				if CURRENT_PAGE<TOTAL_PAGE_NUMBER:
					CURRENT_PAGE+=1

			elif event.key==pygame.K_END:
				writing=False
				CURRENT_PAGE=TOTAL_PAGE_NUMBER
	
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
	pygame.draw.rect(screen,"#000000",(0,0,w,RENDER_LINE_HEIGHT+100))
	TextView(screen,txt,t_x=20,t_y=10,t_w=w-50,t_h=RENDER_LINE_HEIGHT+100,pulse=pulse,text_color='#696969')
	pygame.display.update()
