import random
from time import sleep
import pygame

# pygame.mixer.pre_init(frequency=45100)
pygame.init()
# pygame.mixer.init(frequency=45100)

# os.system('python3 /home/shitij/Desktop/game/controller.py')

clock = pygame.time.Clock()

display_width = 1280
display_height = 920

border_startX = 20
border_startY = 20

border_width = display_width - (border_startX * 2)
border_height = display_height - (border_startY * 2)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A Space Game By Shitij Shailendra Agrawal')
background = pygame.transform.scale(pygame.image.load('./asset/background.jpeg'), (display_width, display_height))

hero_left_images = [
	pygame.image.load('./asset/hero-left1.png'),
	pygame.image.load('./asset/hero-left2.png'),
	pygame.image.load('./asset/hero-left3.png'),
	pygame.image.load('./asset/hero-left4.png'),
	pygame.image.load('./asset/hero-left5.png')
]

hero_right_images = [
	pygame.image.load('./asset/hero-right1.png'),
	pygame.image.load('./asset/hero-right2.png'),
	pygame.image.load('./asset/hero-right3.png'),
	pygame.image.load('./asset/hero-right4.png'),
	pygame.image.load('./asset/hero-right5.png')
]


hero_center_image = [
	pygame.image.load('./asset/hero-stand1.png'),
	pygame.image.load('./asset/hero-stand2.png'),
	pygame.image.load('./asset/hero-stand3.png'),
	pygame.image.load('./asset/hero-stand2.png'),
	pygame.image.load('./asset/hero-stand3.png')
]

hero = hero_center_image[0]

wilan = pygame.image.load('./asset/vilian.png')
blast = pygame.image.load('./asset/blast.png')

score = 0
hero_life = 100

bullet_width = 1
bullet_height = 10
bullet_speed = 10
bullet_color = (0, 0, 0)
bullets = []

total_wilan = 20
wilan_minimum_speed = 1
wilan_maximum_speed = 3
wilans_speed = [random.randint(wilan_minimum_speed, wilan_maximum_speed) for _ in range(total_wilan)]
wilans_positions = [[], [random.randint(-10, border_startY) for _ in range(total_wilan)]]

incrment_x = (border_width - wilan.get_rect().size[0]) / total_wilan
temp = border_startX
for ele in range(len(wilans_positions[1])):
	wilans_positions[0].append(random.randint(temp, int(temp + incrment_x)))
	temp = int(temp + incrment_x)

hero_positionX = (border_startX + border_width) / 2
hero_positionY = (border_startY + border_height) - hero.get_rect().size[1]

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
	screen.blit(textsurface, (0, 0))


def display_hero_life():
	myfont = pygame.font.SysFont('Comic Sans MS', 50)
	textsurface = myfont.render('Life : ' + str(hero_life), False, (255, 255, 255))
	screen.blit(textsurface, (int(display_width / 2), 0))


def draw_border():
	# noinspection PyArgumentList
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


def mov_hero_to_up():
	displacement = 15
	global hero_positionY
	global border_startY
	if not (hero_positionY - displacement) < border_startX:
		hero_positionY = hero_positionY - displacement


def mov_hero_to_down():
	displacement = 15
	global hero_positionY
	global border_startY
	if not ((hero_positionY + hero.get_rect().size[1]) + displacement) > (border_startY + border_height):
		hero_positionY = hero_positionY + displacement


def fire():
	play_fire_audio()
	center_x = int(hero_positionX + (hero.get_rect().size[0] / 2))
	pygame.draw.rect(screen, bullet_color, [center_x, hero_positionY - bullet_height, bullet_width, bullet_height])
	bullets.append([center_x, hero_positionY - bullet_height, bullet_width, bullet_height])


def add_new_wilan():
	wilans_positions[0].append(random.randint(border_startX, border_width - wilan.get_rect().size[0]))
	wilans_positions[1].append(random.randint(-10, border_startY))

	wilans_speed.append(random.randint(wilan_minimum_speed, wilan_maximum_speed))


def destroy_old_villains():
	for position in range(len(wilans_positions[1])):
		try:
			if wilans_positions[1][position] > (border_startY + border_height):
				del wilans_positions[0][position]
				del wilans_positions[1][position]
				del wilans_speed[position]
		except Exception as ex:
			print("destroy villains exception")
			print(ex)


def game_Over():
	for img in range(1, 9, 1):
		screen.blit(pygame.image.load('./asset/blast' + str(img) + '.png'), (int(hero_positionX), int(hero_positionY)))
		pygame.display.update()
		play_blast_audio()
		sleep(1)

	screen.blit(
		pygame.transform.scale(pygame.image.load('./asset/gameOver.png'), (int(border_width), int(border_height / 2))),
		(border_startX, border_startY / 2))
	pygame.display.update()
	sleep(5)


def display_wilans():
	global game_over
	destroy_old_villains()
	while len(wilans_positions[0]) < total_wilan:
		add_new_wilan()

	for pos in range(len(wilans_positions[0])):
		if (hero_positionY <= wilans_positions[1][pos] <= hero_positionY +
			hero.get_rect().size[1]) or (
				wilans_positions[1][pos] + wilan.get_rect().size[1] >= hero_positionY and wilans_positions[1][pos] +
				wilan.get_rect().size[1] <= hero_positionY + hero.get_rect().size[1]) and not game_over:
			if ((hero_positionX + 10) <= wilans_positions[0][pos] <= (
					hero_positionX + hero.get_rect().size[0]) - 10) or (
					(hero_positionX + 10) <= wilans_positions[0][pos] + wilan.get_rect().size[0] <= (
					hero_positionX + hero.get_rect().size[0]) - 10):
				global hero_life
				if hero_life == 0:
					game_over = True
					break
				else:
					hero_life -= 1
		if game_over:
			break
		wilans_positions[1][pos] += wilans_speed[pos]
		screen.blit(wilan, (wilans_positions[0][pos], wilans_positions[1][pos]))


def show_animation(x_position, y_position):
	screen.blit(blast, (x_position, y_position))


def process_bullets():
	global score
	for bullet in bullets:
		for position in range(len(wilans_positions[0])):
			try:
				if wilans_positions[0][position] <= bullet[0] <= wilans_positions[0][position] + wilan.get_rect().size[
					0]:
					if wilans_positions[1][position] <= bullet[1] <= wilans_positions[1][position] + \
							wilan.get_rect().size[1]:
						play_blast_audio()
						show_animation(wilans_positions[0][position], wilans_positions[1][position])
						score = score + 1
						bullets.remove(bullet)
						del wilans_positions[0][position]
						del wilans_positions[1][position]
						del wilans_speed[position]
						continue
			except Exception as ex:
				print("process bullets 1")
				print(ex)
				pass

		if bullet[1] <= border_startY:
			try:
				bullets.remove(bullet)
			except Exception as ex:
				print("process bullets 2")
				print(ex)
		else:
			bullet[1] = bullet[1] - bullet_speed
			pygame.draw.rect(screen, (255, 0, 255), [bullet[0], bullet[1] - bullet_speed, bullet[2], bullet[3]])


def update():
	screen.blit(background, (0, 0))
	process_bullets()
	screen.blit(hero, (hero_positionX, hero_positionY))
	display_wilans()
	draw_border()
	display_score()
	display_hero_life()


def init():
	pygame.mixer.init()
	pygame.font.init()
	screen.blit(background, (0, 0))
	screen.blit(hero, (hero_positionX, hero_positionY))
	screen.blit(wilan, (100, 10))
	draw_border()


init()

current_events = {pygame.K_UP: pygame.KEYUP, pygame.K_DOWN: pygame.KEYUP, pygame.K_RIGHT: pygame.KEYUP, pygame.K_LEFT: pygame.KEYUP, pygame.K_SPACE: pygame.KEYUP}
image_count = 0

# pygame.mixer.pre_init(frequency=45100)
pygame.init()
# pygame.mixer.init(frequency=45100)

# os.system('python3 /home/shitij/Desktop/game/controller.py')

clock = pygame.time.Clock()

display_width = 1280
display_height = 920

border_startX = 20
border_startY = 20

border_width = display_width - (border_startX * 2)
border_height = display_height - (border_startY * 2)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A Space Game By Shitij Shailendra Agrawal')
background = pygame.transform.scale(pygame.image.load('./asset/background.jpeg'), (display_width, display_height))

hero_left_images = [
	pygame.image.load('./asset/hero-left1.png'),
	pygame.image.load('./asset/hero-left2.png'),
	pygame.image.load('./asset/hero-left3.png'),
	pygame.image.load('./asset/hero-left4.png'),
	pygame.image.load('./asset/hero-left5.png')
]

hero_right_images = [
	pygame.image.load('./asset/hero-right1.png'),
	pygame.image.load('./asset/hero-right2.png'),
	pygame.image.load('./asset/hero-right3.png'),
	pygame.image.load('./asset/hero-right4.png'),
	pygame.image.load('./asset/hero-right5.png')
]
while not game_over:
	try:
		if image_count > len(hero_right_images) - 1:
			image_count = 0

		for event in pygame.event.get():
			print(event.type)
			if event.key in current_events:  # If any key pressed which match to our dictionary
				current_events[event.key] = event.type  # Then Change The State of that key
			if event.type == pygame.KEYUP:
				image_count = 0
				hero = hero_center_image[0]
			if event.type == pygame.QUIT:
				game_over = True
				pygame.quit()

		print(image_count)

		if current_events[pygame.K_UP] == pygame.KEYDOWN:
			if image_count % 5 == 0:
				hero = hero_center_image[image_count]
			mov_hero_to_up()
			image_count += 1

		if current_events[pygame.K_DOWN] == pygame.KEYDOWN:
			if image_count % 5 == 0:
				hero = hero_center_image[image_count]
			mov_hero_to_down()
			image_count += 1

		if current_events[pygame.K_RIGHT] == pygame.KEYDOWN:
			if image_count % 5 == 0:
				hero = hero_right_images[image_count]
			mov_hero_to_right()
			image_count += 1

		if current_events[pygame.K_LEFT] == pygame.KEYDOWN:
			if image_count % 5 == 0:
				hero = hero_left_images[image_count]
			mov_hero_to_left()
			image_count += 1

		if current_events[pygame.K_SPACE] == pygame.KEYDOWN:
			hero = hero_center_image[0]
			image_count = 0
			fire()

		sleep(0.001)

	except Exception as e:
		print("main loop ")
		print(e)
	update()
	pygame.display.update()

game_Over()
pygame.quit()
