import pygame
pygame.init()
text_font=pygame.font.Font(pygame.font.get_default_font(),30)
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


def render_lines(screen,render_lines,text_font,t_x,t_y,text_color,all_select):
	for line in render_lines:
		if line != "":
			text_surface = text_font.render(line, 1, text_color)
			if all_select==True:
				txt_rect=text_surface.get_rect()
				txt_rect=(t_x,t_y,txt_rect[2],txt_rect[3])
				pygame.draw.rect(screen,"#ccffcc",txt_rect)
			screen.blit(text_surface, (t_x, t_y))
		t_y +=text_font.size(line)[1]