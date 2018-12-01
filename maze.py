#!/usr/bin/env python3

import requests
import json

#make a POST call with Student ID
baseUrl = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/"
data = {"uid": "804993030"}
headers = {"content-type": "application/x-www-form-urlencoded"}
r = requests.post(url = baseUrl + "session", data = data, headers = headers)
token = json.loads(r.text)["token"]

UNDISCOVERED = 0
DISCOVERED = 1

def mazeSize(state):
	size = json.loads(state.text)['maze_size']
	return size

def startLocation(state):
	startLoc = json.loads(state.text)['current_location']
	return startLoc

def makeMove(dir):
	data = {"action": dir}
	r = requests.post(url = gameUrl, data = data, headers = headers)
	return json.loads(r.text)["result"]


def inBounds(x, y, width, height):
	return (x >= 0) and (x < width) and (y >= 0) and (y < height)

def solveMaze(x, y, discovered, width, height):

	if (discovered[x][y] == DISCOVERED):
		return False

	discovered[x][y] = DISCOVERED

	#check up
	if (inBounds(x, y - 1, width, height) and discovered[x][y - 1] == UNDISCOVERED):
		moveResult = makeMove("UP")

		if (moveResult == "END"):
			return True

		if (moveResult == "WALL" or moveResult == "OUT_OF_BOUNDS"):
			discovered[x][y - 1] = DISCOVERED

		if (moveResult == "SUCCESS"):
			if (solveMaze(x, y - 1, discovered, width, height) == True):
				return True

			else:
				makeMove("DOWN")


	#check down
	if (inBounds(x, y + 1, width, height) and discovered[x][y + 1] == UNDISCOVERED):
		moveResult = makeMove("DOWN")

		if (moveResult == "END"):
			return True

		if (moveResult == "WALL" or moveResult == "OUT_OF_BOUNDS"):
			discovered[x][y + 1] = DISCOVERED

		if (moveResult == "SUCCESS"):
			if (solveMaze(x, y + 1, discovered, width, height) == True):
				return True
			else:
				makeMove("UP")


	#check left
	if (inBounds(x - 1, y, width, height) and discovered[x - 1][y] == UNDISCOVERED):
		moveResult = makeMove("LEFT")

		if (moveResult == "END"):
			return True

		if (moveResult == "WALL" or moveResult == "OUT_OF_BOUNDS"):
			discovered[x - 1][y] = DISCOVERED

		if (moveResult == "SUCCESS"):
			if (solveMaze(x - 1, y, discovered, width, height) == True):
				return True
			else:
				makeMove("RIGHT")

	#check right
	if (inBounds(x + 1, y, width, height) and discovered[x + 1][y] == UNDISCOVERED):
		moveResult = makeMove("RIGHT")

		if (moveResult == "END"):
			return True

		if (moveResult == "WALL" or moveResult == "OUT_OF_BOUNDS"):
			discovered[x + 1][y] = DISCOVERED

		if (moveResult == "SUCCESS"):
			if (solveMaze(x + 1, y, discovered, width, height) == True):
				return True
			else:
				makeMove("LEFT")		

	return False


#get initial mazeStatus
gameUrl = baseUrl + "game?token=" + token
gameState = requests.get(gameUrl, headers=headers)
gameStatus = json.loads(gameState.text)['status']

mazeNumber = 1;
while (gameStatus != "FINISHED"):
	print("Starting maze #" + str(mazeNumber))

	gameState = requests.get(gameUrl, headers=headers)

	(width, height) = mazeSize(gameState)
	(startX, startY) = startLocation(gameState)
	discovered = [ [UNDISCOVERED for y in range(height)] for x in range(width)]

	if (solveMaze(startX, startY, discovered, width, height)):
		print("Finished maze #"  + str(mazeNumber))

	gameStatus = json.loads(gameState.text)['status']

	if (gameStatus == "GAME_OVER" or gameStatus == "NONE"):
		print("Failed to solve maze #" + str(mazeNumber))
		break

	mazeNumber += 1
	
if (gameStatus == "FINISHED"):
	print("All mazes completed.")
