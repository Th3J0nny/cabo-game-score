from os import listdir, makedirs
from os.path import isfile, join, exists
import json

if __name__ == '__main__':
	print("\nWelcome to the score script for")
	print(" .----------------.  .----------------.  .----------------.  .----------------. ")
	print("| .--------------. || .--------------. || .--------------. || .--------------. |")
	print("| |     ______   | || |      __      | || |   ______     | || |     ____     | |")
	print("| |   .' ___  |  | || |     /  \\     | || |  |_   _ \\    | || |   .'    `.   | |")
	print("| |  / .'   \\_|  | || |    / /\\ \\    | || |    | |_) |   | || |  /  .--.  \\  | |")
	print("| |  | |         | || |   / ____ \\   | || |    |  __'.   | || |  | |    | |  | |")
	print("| |  \\ `.___.'\\  | || | _/ /    \\ \\_ | || |   _| |__) |  | || |  \\  `--'  /  | |")
	print("| |   `._____.'  | || ||____|  |____|| || |  |_______/   | || |   `.____.'   | |")
	print("| |              | || |              | || |              | || |              | |")
	print("| '--------------' || '--------------' || '--------------' || '--------------' |")
	print(" '----------------'  '----------------'  '----------------'  '----------------' ")

	data_path = './data'
	if not exists(data_path):
		makedirs(data_path)
	all_game_names = [f for f in listdir(data_path) if isfile(join(data_path, f))]
	game_name = None
	game = dict()
	rounds = dict()
	final_scores = dict()
	while not game_name:
		game_name = input("Please enter a game name:\n--> ")
		
	if game_name in all_game_names:
		print("Loading existing game...")
		with open('./data/' + game_name, 'r') as f:
			game = json.loads(f.read())
		rounds = game['rounds']
		round_number = len(rounds) + 1
		final_scores = game['final_scores']
		players_str = ""
		for i in range(game['player_count']):
			players_str += str(i+1) + ". " + game['players'][i] + "\n"
	else:
		print("\nStarting game '" + game_name + "'...")

		game['name'] = game_name

		player_count = 0
		while not player_count or player_count < 2:
			try:
				player_count = int(input("How many players?\n--> "))
			except:
				print("Please enter a valid number higher than 1!\n")
		game['player_count'] = player_count
		game['players'] = []
		players_str = ""
		
		for i in range(player_count):
			player_name = None
			while not player_name:
				player_name = input("Please enter a name for player #" + str(i+1) + ":\n--> ")
			game['players'].append(player_name)
			players_str += str(i+1) + ". " + player_name + "\n"

		game['rounds'] = rounds
		with open('./data/' + game_name, 'w') as f:
			f.write(json.dumps(game))
		round_number = 1
		for i in range(game['player_count']):
			final_scores[str(i)] = 0

	while True:
		rounds[round_number] = dict()
		print("\n+++ Round #" + str(round_number) + " +++")
		cabo_caller = 0
		while not cabo_caller or cabo_caller < 1 or cabo_caller > game['player_count']:
			try:
				cabo_caller = int(input("Who called \"Cabo\"? (enter number)\n" + players_str + "\n--> "))
			except:
				print("Please enter a valid number!\n")

		rounds[round_number]['cabo_caller'] = cabo_caller - 1
		rounds[round_number]['scores'] = dict()
		for i, player in enumerate(game['players']):
			p_score = None
			while p_score is None or p_score < 0 or p_score == 1:
				try:
					p_score = int(input("Whats the score for " + player + "? "))
				except:
					print("Please enter a valid number!\n")
			rounds[round_number]['scores'][i] = p_score
			final_scores[str(i)] += p_score

		game['rounds'] = rounds
		game['final_scores'] = final_scores
		with open('./data/' + game_name, 'w') as f:
			f.write(json.dumps(game))

		next_round = None
		while not next_round or next_round not in ['y', 'n']:
			next_round = input("Start next round? (y/n) ")
		if next_round == 'n':
			final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1]))
			place = 1
			for i in final_scores:
				print(str(place) + ". " + game['players'][int(i)] + " (" + str(final_scores[str(i)]) + " points)")
				place += 1
			break
		round_number += 1
	
