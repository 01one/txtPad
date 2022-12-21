#  Copyright 2022 Mahid
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY
import pickle
import pygame,sys,time
from pygame.locals import*
import render
pygame.init()
clock=pygame.time.Clock()
then=time.time()

pulse='|'
try:
	#Read Data
	with open('TextData.pickle', 'rb') as data:
		all_data= pickle.load(data)
		data.close()
except:
	#Write Data
	with open('TextData.pickle', 'wb') as data:
		txt=''
		font_size=30
		fullscreen=1
		w=1000
		h=650
		all_data=[]
		all_data.append(txt)
		all_data.append(font_size)
		all_data.append(fullscreen)
		pickle.dump(txt, data)
		data.close()



print(all_data)
txt=all_data[0]
font_size=all_data[1]
fullscreen=all_data[2]
w=1000
h=650
if fullscreen==0:
	screen=pygame.display.set_mode((w,h),RESIZABLE)
elif fullscreen==1:
	screen=pygame.display.set_mode((w,h),FULLSCREEN|HWSURFACE)
pygame.display.set_caption("txtPad")
#pygame.mouse.set_visible(1)
writing=True


TOTAL_PAGE_NUMBER=1
CURRENT_PAGE=TOTAL_PAGE_NUMBER
RENDER_LINE_HEIGHT=100
START_LINE=1
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
		self.text_lines=render.render_text_list(self.text,t_w,self.text_font)

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
		render.render_lines(self.screen,render_lines,self.text_font,self.t_x,self.t_y,self.text_color,all_select)
		

all_select=False
game_running=True
Next_line=False

while game_running:
	clock.tick(60)
	pygame.draw.rect(screen,"#000000",(0,0,w,RENDER_LINE_HEIGHT+100))
	for event in pygame.event.get():
		if event.type==QUIT:
			with open('UserData.pickle', 'wb') as data:
				updateData=[]
				updateData.append(txt)
				updateData.append(font_size)
				updateData.append(fullscreen)
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
			if event.key==pygame.K_ESCAPE:
				with open('UserData.pickle', 'wb') as data:
					updateData=[]
					updateData.append(txt)
					updateData.append(font_size)
					updateData.append(fullscreen)
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
							font_size+=10
						else:
							font_size=20	

			elif event.key==pygame.K_f:
				if event.mod == pygame.KMOD_NONE:
					continue
				else:
					if event.mod & pygame.KMOD_LCTRL:
						if fullscreen==0:
							fullscreen=1
							screen=pygame.display.set_mode((w,h),FULLSCREEN|HWSURFACE)
						else:
							screen=pygame.display.set_mode((w,h),RESIZABLE)
							fullscreen=0


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
	TextView(screen,text=txt,t_x=20,t_y=10,t_w=w-50,t_h=RENDER_LINE_HEIGHT+100,pulse=pulse,text_color='#696969')
	pygame.display.update()
