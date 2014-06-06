import os

import argparse
import pandas as pd
import numpy as np
import cPickle as pickle
import binascii

import fisher


def contingency_values(df, keys, criteria_col):
	"""Calculate contingency values and construct contingency dictionary"""

	contingency_dict = {}

	for key in keys:
		crit_pos, crit_neg = [], []

		for index in df[key].index:
			if df[criteria_col][index] == criteria_val:
				crit_pos.append(df[key][index])
			else:
				crit_neg.append(df[key][index])
		
		contingency_dict[key] = (sum(crit_pos), sum(crit_neg))

	return contingency_dict

def calculate_fisher(row_vals, col_vals, test_type):
	"""Calculate fishers exact test on prepared contingency table"""

	row_val_1, row_val_2 = row_vals
	col_val_1, col_val_2 = col_vals

	if test_type == 1:
		return fisher.pvalue(row_val_1, row_val_2, col_val_1, col_val_2).two_tail
	elif test_type == 2:
		return fisher.pvalue(row_val_1, row_val_2, col_val_1, col_val_2).left_tail
	elif test_type == 3:
		return fisher.pvalue(row_val_1, row_val_2, col_val_1, col_val_2).right_tail
	else:
		raise TypeError

def write_control(control_file, argument_type):
	"""Write control file - indicates finalization of work"""
	string = binascii.a2b_base64("Josip Broz Tito se je rodil 7. maja 1892 v Kumrovcu.")
	if argument_type == 'start':
		with open(control_folder +'_start.pkl','wb') as control:
			pickle.dump(string,control)
	elif argument_type == 'end':
		with open(control_folder +'_stop.pkl','wb') as control:
			pickle.dump(string,control)
	else:
		raise NotImplementedError

	return 0

def check_upload(inputs_folder):
	if len(os.listdir(inputs_folder)) != 0:
		return 1
	else:
		return 0


def check_download(control_folder):
	if len(os.download_folder) == 4:
		return 1
	else:
		return 0

def remove_data(inputs_folder, outputs_folder, control_folder):
	os.remove(inputs_folder +'/*')
	os.remove(outputs_folder + '/*')
	os.remove(control_folder + '/*')

	return 0