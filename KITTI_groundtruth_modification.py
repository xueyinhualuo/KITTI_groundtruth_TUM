# KITTI groundtruth trajectory modification for TUM evaluation

import pandas as pd
import numpy
import os
import sys
import math


time_df = pd.read_csv(sys.argv[1])
pose_df = pd.read_csv(sys.argv[2])

time = time_df.time

pos_x = pose_df.field3
pos_y = pose_df.field7
pos_z = pose_df.field11

m11 = pose_df.field0
m12 = pose_df.field1
m13 = pose_df.field2
m21 = pose_df.field4
m22 = pose_df.field5
m23 = pose_df.field6
m31 = pose_df.field8
m32 = pose_df.field9
m33 = pose_df.field10

q_x = pose_df.field0
q_y = pose_df.field1
q_z = pose_df.field2
q_w = pose_df.field4

i = 0

for (linenum, line) in pose_df.iterrows():
		
	fourWSquaredMinus1 = m11[i] + m22[i] + m33[i]
	fourXSquaredMinus1 = m11[i] - m22[i] - m33[i]
	fourYSquaredMinus1 = m22[i] - m11[i] - m33[i]
	fourZSquaredMinus1 = m33[i] - m11[i] - m22[i]
	biggestIndex = 0
	fourBiggestSquareMinus1 = fourWSquaredMinus1

	if fourXSquaredMinus1 > fourBiggestSquareMinus1:
		fourBiggestSquareMinus1 = fourXSquaredMinus1
		biggestIndex = 1

	if fourYSquaredMinus1 > fourBiggestSquareMinus1:
		fourBiggestSquareMinus1 = fourYSquaredMinus1
		biggestIndex = 2

	if fourZSquaredMinus1 > fourBiggestSquareMinus1:
		fourBiggestSquareMinus1 = fourZSquaredMinus1
		biggestIndex = 3
	
	biggestVal = math.sqrt(fourBiggestSquareMinus1 + 1.0) * 0.5
	mult = 0.25 / biggestVal
	
	if biggestIndex==0:
		q_w[i] = biggestVal;
		q_x[i] = (m23[i] - m32[i]) * mult
		q_y[i] = (m31[i] - m13[i]) * mult
		q_z[i] = (m12[i] - m21[i]) * mult

	elif biggestIndex==1:
		q_x[i] = biggestVal;
		q_w[i] = (m23[i] - m32[i]) * mult
		q_y[i] = (m12[i] + m21[i]) * mult
		q_z[i] = (m31[i] + m13[i]) * mult

	elif biggestIndex==2:
		q_y[i] = biggestVal;
		q_w[i] = (m31[i] - m13[i]) * mult
		q_x[i] = (m12[i] + m21[i]) * mult
		q_z[i] = (m23[i] + m32[i]) * mult

	elif biggestIndex==3:
		q_z[i] = biggestVal;
		q_w[i] = (m12[i] - m21[i]) * mult
		q_x[i] = (m31[i] + m13[i]) * mult
		q_y[i] = (m23[i] + m32[i]) * mult
	
	i = i + 1;

formatted_out = pd.concat((time,pos_x,pos_y,pos_z,q_x,q_y,q_z,q_w),1)

formatted_out.to_csv(sys.argv[3],index = False, header = False)
