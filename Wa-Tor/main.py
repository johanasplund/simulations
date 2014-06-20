import random
import os
import pygame
import sys
import math
from time import sleep


def main(size):
	def create_map(size, screen):
		fish_color = (255, 255, 72)
		shark_color = (125, 125, 125)
		map = []
		for i in range(size):
			map.append([])
			for k in range(size):
				map[-1].append(['', 0, 0])
		fishes = [(random.randint(0, size-1), random.randint(0, size-1)) for k in range(int((size**2)*0.5))]
		sharks = [(random.randint(0, size-1), random.randint(0, size-1)) for k in range(int((size**2)*0.05))]
		for fish in fishes:
			map[fish[0]][fish[1]][0] = 'F'
			pygame.draw.circle(screen, fish_color, (fish[1]*board_scale + sprite_scale, fish[0]*board_scale + sprite_scale), sprite_scale, 0)
		for shark in sharks:
			map[shark[0]][shark[1]][0] = 'S'
			pygame.draw.circle(screen, shark_color, (shark[1]*board_scale + sprite_scale, shark[0]*board_scale + sprite_scale), sprite_scale, 0)
		return (map, len(sharks), len(fish))

	def random_move():
		moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
		return random.choice(moves)

	def new_position_fish(map, row, place):
		available = []
		for i in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
			if not map[(row + i[0]) % size][(place + i[1]) % size][0]:
				available.append(i)
		try:
			return(random.choice(available))
		except:
			return False

	def new_position_shark(map, row, place):
		available_fish = []
		available_pos = []
		for i in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
			if map[(row + i[0]) % size][(place + i[1]) % size][0] == 'F':
				available_fish.append(i)
			elif not map[(row + i[0]) % size][(place + i[1]) % size][0]:
				available_pos.append(i)
		if available_fish:
			return[True, random.choice(available_fish)]
		elif available_pos:
			return[False, random.choice(available_pos)]
		else:
			return False

	def move(map, screen):
		fish_color = (255, 255, 72)
		shark_color = (125, 125, 125)
		sea_color = (72, 150, 255)
		for row in range(size):
			for place in range(size):
				creature = map[row][place][0]
				if not creature:
					pygame.draw.circle(screen, sea_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					continue
				elif creature == 'F':
					if map[row][place][1] == 5:
						move = new_position_fish(map, row, place)
						if move:
							map[(row + move[0]) % size][(place + move[1]) % size][0] = 'F'
							map[(row + move[0]) % size][(place + move[1]) % size][1] = 0
							map[row][place][1] = 0
							pygame.draw.circle(screen, fish_color, (((place + move[0]) % size)*board_scale + sprite_scale, ((row + move[1]) % size)*board_scale + sprite_scale), sprite_scale, 0)
					else:
						move = new_position_fish(map, row, place)
						if move:
							map[(row + move[0]) % size][(place + move[1]) % size][0] = 'F'
							map[row][place][0] = ''
							map[(row + move[0]) % size][(place + move[1]) % size][1] = map[row][place][1] + 1
							map[row][place][1] = 0
							pygame.draw.circle(screen, fish_color, (((place + move[0]) % size)*board_scale + sprite_scale, ((row + move[1]) % size)*board_scale + sprite_scale), sprite_scale, 0)
							pygame.draw.circle(screen, sea_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)

				elif creature == 'S':
					if map[row][place][1] == 3:
						map[row][place][0] = ''
						map[row][place][1] = 0
						map[row][place][2] = 0
						pygame.draw.circle(screen, sea_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					else:
						#hunt
						result = new_position_shark(map, row, place)
						if result:
							move = result.pop(1)
							if result[0] is True:
								map[(row + move[0]) % size][(place + move[1]) % size][0] = 'S'
								map[(row + move[0]) % size][(place + move[1]) % size][1] = 0
								map[(row + move[0]) % size][(place + move[1]) % size][2] = map[row][place][2] + 1
								pygame.draw.circle(screen, shark_color, (((place + move[0]) % size)*board_scale + sprite_scale, ((row + move[1]) % size)*board_scale + sprite_scale), sprite_scale, 0)
								if map[row][place][2] != 5:
									map[row][place][0] = ''
									map[row][place][1] = 0
									map[row][place][2] = 0
									pygame.draw.circle(screen, sea_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
								else:
									map[(row + move[0]) % size][(place + move[1]) % size][2] = 0
									map[row][place][1] = 0
									map[row][place][2] = 0
							else:
								map[(row + move[0]) % size][(place + move[1]) % size][0] = 'S'
								map[(row + move[0]) % size][(place + move[1]) % size][1] = map[row][place][1] + 1
								map[(row + move[0]) % size][(place + move[1]) % size][2] = map[row][place][2] + 1
								pygame.draw.circle(screen, shark_color, (((place + move[0]) % size)*board_scale + sprite_scale, ((row + move[1]) % size)*board_scale + sprite_scale), sprite_scale, 0)
								if map[row][place][2] != 5:
									map[row][place][0] = ''
									map[row][place][1] = 0
									map[row][place][2] = 0
									pygame.draw.circle(screen, sea_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
								else:
									map[(row + move[0]) % size][(place + move[1]) % size][2] = 0
									map[row][place][1] = 0
									map[row][place][2] = 0
		return(map)

	global board_scale
	global sprite_scale
	sprite_scale = 5
	board_scale = sprite_scale * 2
	screen = pygame.display.set_mode((board_scale * size, board_scale * size))
	screen.fill((72, 150, 255))
	(map, sharks, fish) = create_map(size, screen)
	pygame.display.set_caption('Wa-Tor')
	while True:
		# sleep(0.1)
		# map = move_fish(map, screen)
		# map = move_shark(map, screen)
		map = move(map, screen)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

if __name__ == '__main__':
	main(75)
