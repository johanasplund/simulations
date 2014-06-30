#!/usr/bin/env
from pylab import *
import random
import os
import pygame
import sys
import math
import numpy
import matplotlib.pyplot as plt
from threading import Thread


def main(size):
	def create_map(size, screen):
		tree_color = (104, 171, 104)
		jack_color = (237, 46, 56)
		bear_color = (230, 219, 209)
		map = []
		for i in range(size):
			map .append([])
			for k in range(size):
				map[-1].append(['', ''])
		trees = [(random.randint(0, size-1), random.randint(0, size-1)) for k in range(int((size**2)*0.5))]
		lumberjacks = [(random.randint(0, size-1), random.randint(0, size-1)) for k in range(int((size**2)*0.1))]
		bears = [(random.randint(0, size-1), random.randint(0, size-1)) for k in range(int((size**2)*0.02))]
		print(len(trees), len(lumberjacks), len(bears))
		for tree in trees:
			map[tree[0]][tree[1]][0] = 'T'
			pygame.draw.circle(screen, tree_color, (tree[1]*board_scale + sprite_scale, tree[0]*board_scale + sprite_scale), sprite_scale, 0)
		for lumberjack in lumberjacks:
			map[lumberjack[0]][lumberjack[1]][1] = 'L'
			pygame.draw.circle(screen, jack_color, (lumberjack[1]*board_scale + sprite_scale, lumberjack[0]*board_scale + sprite_scale), sprite_scale, 0)
		for bear in bears:
			map[bear[0]][bear[1]][1] = 'B'
			pygame.draw.circle(screen, bear_color, (bear[1]*board_scale + sprite_scale, bear[0]*board_scale + sprite_scale), sprite_scale, 0)
		return (map, len(lumberjacks), len(bears))

	def make_time_map(size):
		time_map = []
		for i in range(size):
			time_map .append([])
			for k in range(size):
				time_map[-1].append(0)
		return time_map

	def random_move():
		moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
		return random.choice(moves)

	def plant_sapling(map, row, place):
		available = []
		for i in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
			if not map[(row + i[0]) % len(map)][(place + i[1]) % len(map)][0]:
				available.append(i)
		if len(available) != 0:
			return(random.choice(available))
		else:
			return False

	def grow_trees(map, time_map, screen):
		tree_color = (104, 171, 104)
		elder_color = (64, 79, 36)
		sapling_color = (155, 255, 48)
		earth_color = (133, 87, 35)
		for row in range(len(map)):
			for place in range(len(map)):
				tree = map[row][place][0]
				if not tree:
					continue
				elif tree == 'T':
					if time_map[row][place] >= 120:
						map[row][place][0] = 'E'
						pygame.draw.circle(screen, elder_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					else:
						time_map[row][place] += 1
					if random.randint(1, 15) == 5: # 1/15 chance to spawn a sapling
						#new sapling
						sap = plant_sapling(map, row, place)
						if sap:
							map[(row + sap[0]) % len(map)][(place + sap[1]) % len(map)][0] = 'S'
							pygame.draw.circle(screen, sapling_color, (((place + sap[0]) % len(map))*board_scale + sprite_scale, ((row + sap[1]) % len(map))*board_scale + sprite_scale), sprite_scale, 0)
				elif tree == 'S':
					if time_map[row][place] >= 12:
						time_map[row][place] = 0
						map[row][place][0] = 'T'
						pygame.draw.circle(screen, tree_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					else:
						time_map[row][place] += 1
				elif tree == 'A':
					if time_map[row][place] >= 60:
						time_map[row][place] = 0
						map[row][place][0] = ''
					else:
						time_map[row][place] += 1

				elif tree == 'E' and random.randint(1, 5) == 3:  # 1/5 chance to spawn a sapling
					#new sapling
					sap = plant_sapling(map, row, place)
					if sap:
						map[(row + sap[0]) % len(map)][(place + sap[1]) % len(map)][0] = 'S'
						pygame.draw.circle(screen, sapling_color, (((place + sap[0]) % len(map))*board_scale + sprite_scale, ((row + sap[1]) % len(map))*board_scale + sprite_scale), sprite_scale, 0)
		return (map, time_map)

	def lumbers_and_bears(map, lumber, screen):
		tree_color = (104, 171, 104)
		elder_color = (64, 79, 36)
		sapling_color = (155, 255, 48)
		jack_color = (237, 46, 56)
		bear_color = (230, 219, 209)
		earth_color = (133, 87, 35)
		ash_color = (0, 0, 0)
		maw = False
		for row in range(len(map)):
			for place in range(len(map)):
				life = map[row][place][1]
				if not life:
					continue
				elif life == 'L':
					#Lumberjack time
					if map[row][place][0] == 'S':
						pygame.draw.circle(screen, sapling_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					elif map[row][place][0] == 'A':
						pygame.draw.circle(screen, ash_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					else:
						pygame.draw.circle(screen, earth_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					map[row][place][1] = ''
					(lati, longi) = 0, 0
					for i in range(3):
						# pygame.display.update()
						move = random_move()
						row = (row + move[0]) % len(map)
						place = (place + move[1]) % len(map)
						if map[row][place][0] == 'T':
							lumber += 1
							map[row][place][0] = ''
							map[row][place][1] = 'L'
							pygame.draw.circle(screen, jack_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
							break
						elif map[row][place][0] == 'E':
							lumber += 2
							map[row][place][0] = ''
							map[row][place][1] = 'L'
							pygame.draw.circle(screen, jack_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
							break
						elif i == 2:
							map[row][place][1] = 'L'
							pygame.draw.circle(screen, jack_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
				elif life == 'B':
					#Bear time
					number_of_maws = 0
					map[row][place][1] = ''
					if not map[row][place][0]:
						pygame.draw.circle(screen, earth_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					else:
						tree = map[row][place][0]
						if tree == 'T':
							pygame.draw.circle(screen, tree_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
						elif tree == 'E':
							pygame.draw.circle(screen, elder_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
						elif tree == 'S':
							pygame.draw.circle(screen, sapling_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
						elif tree == 'A':
							pygame.draw.circle(screen, ash_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					(lati, longi) = 0, 0
					for i in range(5):
						move = random_move()
						row = (row + move[0]) % len(map)
						place = (place + move[1]) % len(map)
						if map[row][place][1] == 'L':
							number_of_maws += 1
							if number_of_maws > 5:
								maw = True
							else:
								maw = False
							map[row][place][1] = 'B'
							pygame.draw.circle(screen, bear_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
							break
						elif i == 4:
							map[row][place][1] = 'B'
							pygame.draw.circle(screen, bear_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
		return(map, lumber, maw)

	def add_lumberjack(map, screen):
		jack_color = (237, 46, 56)
		while True:
			placement = (random.randint(0, len(map) - 1), random.randint(0, len(map) - 1))
			if not map[placement[0]][placement[1]][1]:
				map[placement[0]][placement[1]][1] = 'L'
				pygame.draw.circle(screen, jack_color, (placement[1]*board_scale + sprite_scale, placement[0]*board_scale + sprite_scale), sprite_scale, 0)
				return map

	def remove_lumberjack(map, amount, screen):
		earth_color = (133, 87, 35)
		for row in range(len(map)):
			for place in range(len(map)):
				if map[row][place][1] == 'L':
					amount -= 1
					map[row][place][1] = ''
					pygame.draw.circle(screen, earth_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					if amount == 0:
						return(map)

	def remove_bear(map, screen):
		earth_color = (133, 87, 35)
		for row in range(len(map)):
			for place in range(len(map)):
				if map[row][place][1] == 'B':
					map[row][place][1] = ''
					pygame.draw.circle(screen, earth_color, (place*board_scale + sprite_scale, row*board_scale + sprite_scale), sprite_scale, 0)
					return(map)

	def add_bear(map, screen):
		bear_color = (230, 219, 209)
		while True:
			placement = (random.randint(0, len(map) - 1), random.randint(0, len(map) - 1))
			if not map[placement[0]][placement[1]][1]:
				map[placement[0]][placement[1]][1] = 'B'
				pygame.draw.circle(screen, bear_color, (placement[1]*board_scale + sprite_scale, placement[0]*board_scale + sprite_scale), sprite_scale, 0)
				return map

	def forest_fire(map, time_map, placement, screen):
		fire_color = (255, 239, 0)
		ash_color = (0, 0, 0)
		fire_places = []
		if not placement:
			placement = (random.randint(0, len(map) - 1), random.randint(0, len(map) - 1))
		while not map[placement[0]][placement[1]][0]:
			placement = (random.randint(0, len(map) - 1), random.randint(0, len(map) - 1))
		fire_places.append(placement)
		time_map[placement[0]][placement[1]] = 0
		map[placement[0]][placement[1]][0] = 'A'
		is_fire = True
		pygame.draw.circle(screen, fire_color, (placement[1]*board_scale + sprite_scale, placement[0]*board_scale + sprite_scale), sprite_scale, 0)
		pygame.display.update()
		while is_fire:
			is_fire = False  # Innocent until proven otherwise
			for fire in fire_places:
				if time_map[fire[0]][fire[1]] >= 2:
					fire_places.remove(fire)
					time_map[fire[0]][fire[1]] = 0
					pygame.draw.circle(screen, ash_color, (fire[1]*board_scale + sprite_scale, fire[0]*board_scale + sprite_scale), sprite_scale, 0)
					if len(fire_places) == 0:
						return(map, time_map)
				else:
					is_fire = True  # Guilty!
					time_map[fire[0]][fire[1]] += 1
					for move in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
						new_fire = ((fire[0] + move[0]) % len(map), (fire[1] + move[1]) % len(map))
						if map[new_fire[0]][new_fire[1]][0] and map[new_fire[0]][new_fire[1]][0] != 'A':
							tree = map[new_fire[0]][new_fire[1]][0]
							if tree == 'T':
								roof = 4
								time_map[new_fire[0]][new_fire[1]] = 1 
							elif tree == 'S':
								roof = 8  # Hard to catch fire
								time_map[new_fire[0]][new_fire[1]] = 2
							elif tree == 'E':
								roof = 2  # Easy to catch fire
								time_map[new_fire[0]][new_fire[1]] = 0
							if random.randint(1, roof) == 1:
								fire_places.append(new_fire)
								map[new_fire[0]][new_fire[1]][0] = 'A'
								pygame.draw.circle(screen, fire_color, (new_fire[1]*board_scale + sprite_scale, new_fire[0]*board_scale + sprite_scale), sprite_scale, 0)
								pygame.display.update()
								if map[new_fire[0]][new_fire[1]][1]:
									map[new_fire[0]][new_fire[1]][1] = ''
		return(map, time_map)

	global board_scale
	global sprite_scale
	sprite_scale = 5
	board_scale = sprite_scale * 2
	screen = pygame.display.set_mode((board_scale * size, board_scale * size))
	screen.fill((133, 87, 35))
	(map, lumberjacks, bears) = create_map(size, screen)
	time_map = make_time_map(size)
	os.system('clear')
	lumber = 0
	months = 0
	years = 0
	tot_lumber = 0
	print('Key commands:')
	print('F = Fire, B = Spawn bears, L = Spawn Lumberjacks, K = Kill lumberjacks')
	print('Click the map to start a fire in that location, (if there is a tree there')

	while True:
		pygame.display.set_caption('Years: ' + str(years) + ', Months: ' + str(months))
		pygame.display.update()
		(map, time_map) = grow_trees(map, time_map, screen)
		pygame.display.update()
		(map, lumber, maw) = lumbers_and_bears(map, lumber, screen)
		tot_lumber += lumber
		if months == 12:
			years += 1
			amount = int(math.floor(tot_lumber/250))
			lumberjacks += (amount - lumberjacks)
			# if maw:
			# 	map = remove_bear(map, screen)
			# else:
			# 	map = add_bear(map, screen)
			if lumberjacks > 0:
				for i in range(amount):
					map = add_lumberjack(map, screen)
			else:
				map = remove_lumberjack(map, amount, screen)
			if random.randint(1, 100) == 5:
				(map, time_map) = forest_fire(map, time_map, None, screen)

			lumber = 0
			months = 0
			tot_lumber = 0
		months += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_k:
					print("Killed fifty random lumberjacks")
					map = remove_lumberjack(map, 50, screen)
				elif event.key == pygame.K_f:
					print('FIRE!!!!')
					(map, time_map) = forest_fire(map, time_map, None, screen)
				elif event.key == pygame.K_b:
					print('Spawned one houndred bears!')
					for i in range(100):
						map = add_bear(map, screen)
				elif event.key == pygame.K_l:
					print('Spawned fifty lumberjacks, you monster')
					for i in range(50):
						map = add_lumberjack(map, screen)
				elif event.key == pygame.K_ESCAPE:
					return
				elif pygame.mouse.get_pressed()[0]:
					print('lol')
			elif event.type == pygame.MOUSEBUTTONDOWN:
				x, y = event.pos
				x = int(x/board_scale)
				y = int(y/board_scale)
				if map[y][x][0] and map[y][x][0] != 'A':
					(map, time_map) = forest_fire(map, time_map, (y, x), screen)
if __name__ == '__main__':
	#size = int(input("Specify size: "))
	main(75)