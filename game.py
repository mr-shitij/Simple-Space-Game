import pygame
import random
from time import sleep
pygame.init()

display_width = 1280
display_height = 720

border_startX = 20
border_startY = 20

border_width = display_width - (border_startX *2)
border_height = display_height - (border_startY*2)


screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A Space Game By Shitij Shailendra Agrawal')
background = pygame.transform.scale(pygame.image.load('./asset/background.jpg'), (display_width, display_height))


hero = pygame.image.load('./asset/spaceship.png')
wilan = pygame.image.load('./asset/evilShip.png')
blast = pygame.image.load('./asset/blast.png')

score = 0

bullet_width = 2
bullet_height = 20
bullet_speed = 20
bullets = []




total_wilan = 20
wilan_minimum_speed = 1
wilan_maximum_speed = 2
wilans_speed = [random.randint(wilan_minimum_speed, wilan_maximum_speed) for _ in range(total_wilan)]
wilans_positions = [[], [random.randint(-10, border_startY) for _ in range(total_wilan)]]


incrment_x = (border_width - wilan.get_rect().size[0] ) / total_wilan
temp = border_startX
for ele in range(len(wilans_positions[1])):
	wilans_positions[0].append(random.randint(temp, int(temp + incrment_x)))
	temp = int(temp + incrment_x)


hero_positionX = (border_startX + border_width)/2
hero_positionY = (border_startY+border_height)-hero.get_rect().size[1]




game_over = False



def play_blast_audio():
	pygame.mixer.music.load("./audio/blast.mp3")
	pygame.mixer.music.set_volume(0.7)
	pygame.mixer.music.play()

def play_fire_audio():
	pygame.mixer.music.load("./audio/fire.mp3")
	pygame.mixer.music.set_volume(0.7)
	pygame.mixer.music.play()

def display_score():
	myfont = pygame.font.SysFont('Comic Sans MS', 50)
	textsurface = myfont.render('Score : ' + str(score), False, (255, 255, 255))
	screen.blit(textsurface,(0, 0))


def draw_border():
	pygame.draw.rect(screen, (255, 0, 0), [border_startX, border_startY, border_width, border_height], 2)

def mov_hero_to_left():
	displacement = 15
	global hero_positionX
	global border_startX
	if not (hero_positionX - displacement) < border_startX:
		hero_positionX = hero_positionX - displacement

def mov_hero_to_right():
	displacement = 15
	global hero_positionX
	global border_startX
	if not ((hero_positionX + hero.get_rect().size[0]) + displacement) > (border_startX + border_width):
		hero_positionX = hero_positionX + displacement


def fire():
	play_fire_audio()
	centerX = int(hero_positionX + (hero.get_rect().size[0] / 2))
	pygame.draw.rect(screen, (255, 0, 255), [centerX, hero_positionY - bullet_height, bullet_width, bullet_height])
	bullets.append([centerX, hero_positionY - bullet_height, bullet_width, bullet_height])

def add_new_wilan():
	wilans_positions[0].append(random.randint(border_startX, border_width - wilan.get_rect().size[0]))
	wilans_positions[1].append(random.randint(-10, border_startY))

	wilans_speed.append(random.randint(wilan_minimum_speed, wilan_maximum_speed))

def destory_old_wilans():
	for position in range(len(wilans_positions[1])):
		try:	
			if wilans_positions[1][position] > (border_startY + border_height):
				del wilans_positions[0][position]
				del wilans_positions[1][position]
				del wilans_speed[position]
		except:
			pass

def display_wilans():
	destory_old_wilans()	
	while len(wilans_positions[0]) < total_wilan:
		add_new_wilan()
		
	for pos in range(len(wilans_positions[0])):
		wilans_positions[1][pos] += wilans_speed[pos]
		screen.blit(wilan, (wilans_positions[0][pos], wilans_positions[1][pos]))

def show_animation(x_position, y_position):
	screen.blit(blast, (x_position, y_position))

def process_bullets():
	global score
	for bullet in bullets:
		for position in range(len(wilans_positions[0])):
			try:
				if wilans_positions[0][position] <= bullet[0] and wilans_positions[0][position] + wilan.get_rect().size[0] >= bullet[0]:
					if (wilans_positions[1][position] <= bullet[1] and wilans_positions[1][position] + wilan.get_rect().size[1] >= bullet[1]):
						show_animation(wilans_positions[0][position], wilans_positions[1][position])
						score = score + 1
						play_blast_audio()
						bullets.remove(bullet)
						del wilans_positions[0][position]
						del wilans_positions[1][position]
						del wilans_speed[position]
						continue
			except:
				pass
			
		if bullet[1] <= border_startY:
			try:
				bullets.remove(bullet)
			except:
				pass
		else:
			bullet[1] = bullet[1] - bullet_speed
			pygame.draw.rect(screen, (255, 0, 255), [bullet[0], bullet[1] - bullet_speed,
									bullet[2], bullet[3]])

def update():
	screen.blit(background, (0, 0))
	process_bullets()
	display_wilans()
	draw_border()
	display_score()
	screen.blit(hero, (hero_positionX, hero_positionY))

def init():
	pygame.mixer.init()
	pygame.font.init()
	score = 0
	screen.blit(background, (0, 0))
	screen.blit(hero, (hero_positionX, hero_positionY))
	screen.blit(wilan, (100, 10))
	draw_border()


init()

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_over = True
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				mov_hero_to_left()
			if event.key == pygame.K_RIGHT:
				mov_hero_to_right()
			if event.key == pygame.K_SPACE:
				fire()
	sleep(0.02)
	update()
	pygame.display.update()

pygame.quit()
