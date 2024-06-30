#!/python311/python

import random
import sys
import subprocess, json
import argparse
from time import time


def extract_section(invideo, outvideo, starting, ending):

	cut_string = 'ffmpeg.exe -loglevel quiet -i  %s  -ss %s -to %s %s' %(invideo, starting,ending,outvideo)

	print(cut_string)
	result = subprocess.check_output(cut_string,shell=True).decode()
	return outvideo

def with_ffprobe(filename):
    import subprocess, json

    result = subprocess.check_output(
    	f'ffprobe.exe   -i {filename} -show_entries format=duration -v quiet -of csv="p=0"', shell=True).decode()
    return json.loads(result)

if __name__ == "__main__":

	time_dict = {
		1:['00:00','00:59'],
		2:['01:00','01:46'],
		3:['01:47','03:30'],
		4:['03:31','04:57'],
		5:['04:58','05:18'],
		6:['05:19','05:32'],
		7:['05:33','06:08'],
		8:['06:09','07:09'],
		9:['07:10','07:29'],
		10:['07:30','08:02'],
		11:['08:03','09:21'],
		12:['09:22','10:03'],
		13:['10:04','10:30'],
		14:['10:31','11:10'],
		15:['11:11','11:37'],
		16:['11:38','13:59'],
		17:['14:00','15:09'],
		18:['15:10','16:36'],
		19:['16:37','18:07'],
		20:['18:08','18:43'],
		21:['18:44','20:17'],
		22:['20:18','21:22'],
		23:['21:23','21:31'],
		24:['21:32','22:03'],
		25:['22:04','22:43'],
		26:['22:44','23:34'],
		27:['23:35','24:05'],
		28:['24:06','26:33'],
		29:['26:34','27:24'],
		30:['27:25','27:59'],
		31:['28:00','28:47'],
		32:['28:48','29:19'],
		33:['29:20','30:00'],
		34:['30:01','31:24'],
		35:['31:25','32:49'],
		36:['32:50','34:17'],
		37:['34:18','34:44'],
		38:['34:45','35:18'],
		39:['35:19','35:35'],
		40:['35:36','36:42'],
		41:['36:43','37:03'],
		42:['37:04','38:08'],
		43:['38:09','40:10'],
		44:['40:11','40:40'],
		45:['40:41','42:04'],
		46:['42:05','43:16'],
		47:['43:17','44:01'],
		48:['44:02','45:09'],
		49:['45:10','45:59'],
		}
	
	import datetime
	now = datetime.datetime.now()	
	print(now)
	for foo in time_dict.keys():
		print (f" Q {foo}  start {time_dict[foo][0]}   end {time_dict[foo][1]}")

		fname = "Question_%02d.mp4" %(foo)
		print(fname)
		extract_section('alteryx_advanced_desktop.mp4', fname, time_dict[foo][0], time_dict[foo][1])

	now = datetime.datetime.now()	
	print(now)
	
	print("Done")
			
		
	


