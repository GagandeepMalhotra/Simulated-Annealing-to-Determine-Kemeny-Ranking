import sys
import time
#import numpy as np
import random
import copy
import math

#Task 2
#Command line input: "py task2.py 1994_Formula_One.wmg" will read specified file 

#Chooses an appropriate neighbouring solution by randomly switching two drivers rankings
def find_next_neighbour(rankings):
	#Chooses a random driver one and a different driver two
	numbers = list(range(0, len(rankings) - 1))
	driver_one = random.choice(numbers)
	numbers.remove(driver_one)
	driver_two = random.choice(numbers)
	#Swaps the rankings for the chosen drivers
	rankings = swap_items(rankings, driver_one, driver_two)
	#Store all the relevant values (new rankings, driver one, and driver two) in a dictionary to be returned
	ranking_values = {}
	ranking_values["new_rankings"] = rankings
	#Stores both driver one and driver two in the dictionary if driver one is worse ranked
	if driver_one > driver_two:
		ranking_values["worse_ranking"] = driver_one
		ranking_values["better_ranking"] = driver_two
	#Stores both driver one and driver two in the dictionary if driver one is better ranked
	elif driver_two >= driver_one:
		ranking_values["better_ranking"] = driver_one
		ranking_values["worse_ranking"] = driver_two
	#print("rank list :	", rankings)
	return ranking_values

#Calculate the increase or decrease in weight
def weight_change(initial_value, added_value):
	initial_value += added_value
	return initial_value

#Swap two items in a list
def swap_items(initial_list, item1, item2):
    temp = initial_list[item1]
    initial_list[item1] = initial_list[item2]
    initial_list[item2]=temp
    return initial_list
	
#Function to find Kemeny score of the current rankings
def kemeny_ranking(rankings):
	#Initialise Kemeny score
	kemeny_score = 0
	#Search through each loss of a driver and store the weight of that loss
	for x in (x for x in rankings if str(x) in losers):
		#Current driver (x) loses to a driver ranked below them then add the weight to the current Kemeny score
		for driver in (driver for driver in losers[str(x)] if rankings.index(int(driver[0])) > rankings.index(x)):
			weight = int(driver[1])
			kemeny_score += weight
	return kemeny_score

#Uses the previously calculated Kemeny score and finds the drivers that have changed rankings
def calculate_kemeny_ranking(first_driver, second_driver, rankings, initial_weight):
	#Calculate the number of drivers between the two swapped drivers
	difference = ((second_driver) - (first_driver)) + 1
	#Go through each rankings between the switched drivers
	for x in range(0, difference):
		#Increase Kemeny score according to the first or second drivers new position and if they won or lost more races than the other drivers (stored in winners/losers dictionary)
		if str(rankings[first_driver]) in losers.keys():
			for i in (i for i in losers[str(rankings[first_driver])] if str(i[0]) == str(rankings[first_driver + x])):
				initial_weight = weight_change(initial_weight, int(i[1]))
		if str(rankings[second_driver]) in winners.keys():
			for i in (i for i in winners[str(rankings[second_driver])] if str(i[0]) == str(rankings[first_driver + x])):
				initial_weight = weight_change(initial_weight, int(i[1]))
		#Decrease Kemeny score according to the first or second drivers new position and if they won or lost more races than the other drivers (stored in winners/losers dictionary)
		if str(rankings[first_driver]) in winners.keys():
			for i in (i for i in winners[str(rankings[first_driver])] if str(i[0]) == str(rankings[first_driver + x])):
				initial_weight = weight_change(initial_weight, -(int(i[1])))
		if str(rankings[second_driver]) in losers.keys():
			for i in (i for i in losers[str(rankings[second_driver])] if str(i[0]) == str(rankings[first_driver + x])):
				initial_weight = weight_change(initial_weight, -(int(i[1])))
	return initial_weight


#Implementation of the simulated annealing pseudocode (deals with the actual steps of the SA algorithm)
def sim_annealing(current_weight, current_ranking, current_temperature):
	#Initialise variable of worse moves (uphill moves on a graph) and dictionary to return multiple values
	worse_move_count = 0
	values_dictionary = {}
	#Stores the current ranking to be used later if a worse move is unwanted
	previous_ranking = copy.copy(current_ranking)
	#Calls the algorithm to find a suitable neighbour for the current ranking by switching two random drivers rankings
	neighbour_ranking = find_next_neighbour(current_ranking)
	#Stores the new ranking which is a neighbour of the current ranking, 
	#Stores the rankings which were switched so the kemeny score can be calculated using the previous ranking's kemeny score
	new_ranking = neighbour_ranking["new_rankings"]
	better_ranking = neighbour_ranking["better_ranking"]
	worse_ranking = neighbour_ranking["worse_ranking"]
	#Calculate the kemeny score of the new rankings using the previous ranking's kemeny score
	new_weight = calculate_kemeny_ranking(better_ranking, worse_ranking, new_ranking, current_weight)
	#Checks for if the new rankings have a lower kemeny score than the previous rankings
	if new_weight <= current_weight:
		#Store the new rankings, the new Kemeny score, and the number of worse moves (to leave local optima)
		values_dictionary["rankings"] = new_ranking
		values_dictionary["score"] = new_weight
		values_dictionary["worse_moves"] = worse_move_count
		return values_dictionary
	else:
		#Check if current temperature is 0 to avoid math errors when dividing by 0
		if current_temperature != 0:
			#Implementing simulated annealing formula with the new weight and the current weight and temperature (the random number chosen is between 0 and 1)
			x = random.uniform(0, 1)
			y = -(new_weight - current_weight) / current_temperature
			z = math.exp(y)
			#If x is below z (random number below calculated simulated annealing formula value) a worse move will be made as the new ranking will be saved (according to the Kemeny score)
			if x < z:
				#Store the new driver rankings, the new Kemeny score, and the incremented number of worse moves
				values_dictionary["rankings"] = new_ranking
				values_dictionary["score"] = new_weight
				worse_move_count += 1
				values_dictionary["worse_moves"] = worse_move_count
				return values_dictionary
		#Store the current driver rankings, the current Kemeny score, and the current number of worse moves
		values_dictionary["rankings"] = previous_ranking
		values_dictionary["score"] = current_weight
		values_dictionary["worse_moves"] = worse_move_count
		return values_dictionary

#Command line input: "python3 task2.py 1994_Formula_One.wmg" will read specified file 

file = open(str(sys.argv[1]))
read_file = file.read().split("\n")
#Removing empty lines front list
read_file = list(filter(None, read_file))
#Get the number of racers from first line of file
number_of_racers = int(read_file[0])
#Set an initial solution for number of racers in race
current_ranking = []

for x in range(1,number_of_racers+1):
	current_ranking.append(x)
#Create an empty racers, winners, and losers dictionary
racers = {}
winners = {}
losers = {}
#Initialise variables and set Stopping Criterion
worse_moves = 0
num_non_improve_count = 0
num_non_improve_limit = 75
#Set a starting and cooling temperature values
temperature = 1
#Set a temperature length
temperature_length = 75
#Set Cooling Ratio
cooling_ratio = 0.65

for x in range(len(read_file)):
	#Store the racers' names with their corresponding ID in a dictionary
	if x < number_of_racers:
		#Stores the racers name (after comma in wmg file)
		racer_name = read_file[x+1][(read_file[x+1].find(",")) + 1:]
		#Stores the racers number (before comma in wmg file)
		racer_num = read_file[x+1][:(read_file[x+1]).find(",")]
		#Store these corresponding values in a dictionary
		racers[str(racer_num)] = racer_name
	#Record the wins/losses
	if x > number_of_racers+2:
		#Split each result into weight, winner, and loser
		result = read_file[x]
		result = list(result.split(","))
		#Store the weight, winner, and loser for each edge 
		weight = result[0]
		winner = result[1]
		loser = result[2]
		#Append the winner and weight values to loser if loser is in losers
		if loser in losers:
			losers[loser].append((winner, weight))
			#print("losers[loser];	", losers[loser])
		#Otherwise create an index at loser to add the winner and weight values
		else:
			losers[loser] = [(winner, weight)]
		#Append the loser and weight values to winner if winner is in winners
		if winner in winners:
			winners[winner].append((loser, weight))
		#Otherwise create an index at winner to add the loser and weight values
		else:
			winners[winner] = [(loser, weight)]
		#print(read_file[x]

time_1 = time.time_ns() // 1_000_000
#Run the Cost Function
initial_score = kemeny_ranking(current_ranking)
#Run the Simulated Annealing function
current_ranking = sim_annealing(initial_score, current_ranking, temperature)["rankings"]
#Until the stopping criterion is met

#total_sim = 0

#Record the initial time before the full algorithm starts
time_1 = time.time_ns() // 1_000_000

while num_non_improve_count < num_non_improve_limit:
	#Repeat from 0 to temp length
	for x in range(0,temperature_length):
		#Copy the ranking to check if ranking was changed in the sim annealing function
		previous_ranking = copy.copy(current_ranking)
		#Store the returned values of the sim annealing in a dictionary

		sim_annealing_dictionary = sim_annealing(initial_score, current_ranking, temperature)

		current_ranking = sim_annealing_dictionary["rankings"]
		initial_score = sim_annealing_dictionary["score"]
		if previous_ranking != current_ranking:
			#Reset current count
			num_non_improve_count = 0
		else:
			#Increment current count if both rankings are the same
			num_non_improve_count += 1
		#Increment current worse move count
		worse_moves += sim_annealing_dictionary["worse_moves"]
	#print("temp:	" , temperature)
	#Cooling Schedule
	temperature = cooling_ratio * temperature
#Compute time taken for algorithm
time_2 = time.time_ns() // 1_000_000
time_difference = time_2 - time_1

#Print the results in a table format
print("\n")
print("Ranking\t Driver")
print(u'\u2500' * 30)

#Print out each driver and their rank
for x in range(len(current_ranking)):
	print(str(x+1), "\t" , racers[str(current_ranking[x])])
#Print the best Kemeny score found
print("\nKemeny score of best ranking: " + str(kemeny_ranking(current_ranking)))
#Print time taken for algorithm to run in milliseconds
print("Algorithm's runtime in milliseconds: " + str(time_difference) + " milliseconds")
