def compare_annotations(filename_predicted,filename_gt, verbose=0):
	
	p = open(filename_predicted,"rt")  	
	gt = open(filename_gt,"rt")  	
	all_lines_p = p.readlines()
	all_lines_gt = gt.readlines()


	#positions and tiles	
	number_lines_p = len(all_lines_p)
	number_lines_gt = len(all_lines_gt)

	match_positions = 1
	match_tiles = 1
	match_score = 1

	for i in range(2):		
		current_pos_gt, current_tile_gt = all_lines_gt[i].split()
		
		if verbose:
			print(i)
			print(current_pos_gt,current_tile_gt)

		try:
			current_pos_p, current_tile_p = all_lines_p[i].split()
			
			if verbose:
				print(current_pos_p,current_tile_p)

			if(current_pos_p != current_pos_gt):
				match_positions = 0
			if(current_tile_p != current_tile_gt):
				match_tiles = 0	
		except:
			match_positions = 0
			match_tiles = 0		


	points_positions = 0.03 * match_positions
	points_tiles = 0.01 * match_tiles	

	#scores
	last_line_p = all_lines_p[2]
	score_p = last_line_p.split()
	last_line_gt= all_lines_gt[2]
	score_gt = last_line_gt.split()
	
	if verbose:
		print(score_p,score_gt)

	if(score_p != score_gt):
		match_score = 0

	points_score = 0.02 * match_score

	p.close()
	gt.close()

	return points_positions, points_tiles,points_score


def compare_annotations_table_scores(filename_table_score_predicted, filename_table_score_gt, verbose = 0):
	p = open(filename_table_score_predicted,"rt")
	gt = open(filename_table_score_gt,"rt")
	all_lines_p = p.readlines()
	all_lines_gt = gt.readlines()
	print(filename_table_score_predicted, filename_table_score_gt)

	matches_table_score = 20

	for i in range(20):	
		line_gt = all_lines_gt[i].split()
		line_p = all_lines_p[i].split()
		if verbose:
			print(line_gt, line_p)
		if (line_p != line_gt):
			matches_table_score = matches_table_score - 1

	p.close()
	gt.close()
	points_table_score = 0.02 * matches_table_score
	return points_table_score



#EVALUATION ON TEST TEST
print("EVALUATION ON TEST SET")

#change this on your machine pointing to your results (txt files)
predictions_path_root = "/home/cristian/and_/facultate/s5/cava/ComputerVisionGame/test_result"

#change this on your machine to point to the ground-truth test
gt_path_root = "/home/cristian/and_/facultate/s5/cava/ComputerVisionGame/antrenare/table-joc"

#change this to 1 if you want to print results at each move
verbose = 0
total_points = 0
for game in range(1,2):
	#change this to range (1,6) on the test set
	for move in range(1,21):
		
		name_move = str(move)
		if(move< 10):
			name_move = '0'+str(move)

		filename_predicted = predictions_path_root + str(game) + '_' + name_move + '.txt'
		filename_gt = gt_path_root + str(game) + '_' + name_move + '.txt'

		filename_table_score_predicted = predictions_path_root + str(game) + '_mapare_table_scor.txt'
		filename_table_score_gt = gt_path_root + str(game) + '_mapare_table_scor.txt'
 



		game_move = str(game) + '_' + name_move
		points_position = 0
		points_tiles = 0
		points_score = 0	

		try:
			points_position, points_tiles, points_score = compare_annotations(filename_predicted,filename_gt ,verbose)
		except:
			print("For image: ", game_move, " encountered an error")

		print("Image: ", game_move, "Points position: ", points_position, "Points tiles: ",points_tiles, "Points score: ", points_score)


		total_points = total_points + points_position + points_tiles + points_score

	points_table_score = 0
	verbose = 1

	try:
		points_table_score = compare_annotations_table_scores(filename_table_score_predicted,filename_table_score_gt, verbose)
	except:
		print("For game: ", game, " encountered an error when computing table scores")

	total_points = total_points + points_table_score	


print(total_points)