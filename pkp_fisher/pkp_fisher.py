#!/usr/bin/env python

import os

import argparse
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser(description='Run Fisher Test.')

parser.add_argument('-s', dest='s', type=int, default=4, help='col names from start')
parser.add_argument('-e', dest='e', type=int, default=2, help='col names from end')
parser.add_argument('-c', dest='c', type=int, default=4, help='col of criteria variables')
parser.add_argument('-crit', dest='crit', type=str, default='A', help='col criteria value')
parser.add_argument('-t', dest='t', type=int, default=1, help='1 = two_tailed, 2 = left_tail, 3 = right_tail fisher test')
parser.add_argument('-ip', dest='ip', type=str, default='./inputs/', help='inputs path')
parser.add_argument('-op', dest='op', type=str, default='./outputs/', help='outputs path')
parser.add_argument('-cp', dest='cp', type=str, default='./control/', help='control path')
# parser.add_argument('-pp', dest='pp', type=str, default='./project', help='project path')


args = parser.parse_args()
start_col, end_col, criteria_col_nr  = args.s, args.e, args.c-1
criteria_val = args.crit
test_type = args.t
input_path, output_path, control_path = args.ip, args.op, args.cp

while True:
	if scripts.check_upload(input_path) == 1:
		break

inputs = os.listdir(input_path)
outputs = [output_path + input1.split('.')[0] + '_fisher.xls' for input1 in inputs]
inputs = [input1 for input1 in inputs]

scripts.write_control(control_path, 'start')

for i, filename in enumerate(inputs):
	xl = pd.ExcelFile(filename)
	writer = pd.ExcelWriter(outputs[i])
	for sheet in xl.sheet_names:
		df = xl.parse(sheet)

		keys = df.keys()[start_col:-end_col]
		criteria_col = df.keys()[criteria_col_nr]
		rows, cols = keys, keys

		scripts.contingency_dict = contingency_values(df, keys, criteria_col)
		result_matrix = [[scripts.calculate_fisher(contingency_dict[row], contingency_dict[col], test_type) for row in rows] for col in cols]
		result_matrix = np.array(result_matrix)

		df1 = pd.DataFrame(data = result_matrix, index = rows, columns = cols)
		df1.to_excel(writer, sheet)
	writer.save()

scripts.write_control(control_path, 'stop')

while True:
	if scripts.check_download(control_path) == 1:
		break

scripts.remove_data(input_path, output_path, control_path)

