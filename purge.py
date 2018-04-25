from numpy import *
from scipy import loadtxt, optimize
import matplotlib.pyplot as plt
import os
from ROOT import TH1F, gROOT, TCanvas, gPad
from shutil import copyfile
#gROOT.Reset()
#c1 = TCanvas('c1', 'test', 200, 10,700, 500)
#
#Vd = .0538
#r1 = 100000.
#r2 = 1000.
#ra = 200000.
##ra = 100000.
#rf = 22000.
#v_in = 5.45

times = []
volts1 =[]
prepurged = []
for filename in os.listdir("data_purged"):
	prepurged.append(filename)
print "prepurged: ", prepurged

for directory in os.listdir("data/used"):
	curdir = "data/used/%s"%(directory)
	for filename in os.listdir(curdir):
		if "purged_"+filename not in prepurged:
			print "purging file %s" %(filename)
			curfile = "data/used/%s/%s"%(directory,filename)
			time, volt = loadtxt(curfile, unpack=True, skiprows=3)
			new_purgename = "data_purged/purged_%s"%(filename)
			f = open(new_purgename,'w')
			nonempty = False
			for v,t in zip(volt,time):
				if v<-0.2 and v> -9:
					times.append(t)
					volts1.append(v)
					line = "%s \n"%(v)
					f.write(line)
					nonempty = True
			
			if nonempty:
				f.write("0 \n")
				f.close()
				fullname = "data_purged/full/purged_%s"%(filename)
				copyfile(new_purgename,fullname)
			else:
				f.close()
			print "complete purge of file %s" %(filename)
					
#v2 = []
#for v in volts:
#	if v > -2.:
#		v2.append(-v)
##volts = v2
#volts = [v for v in volts1 if (v<-0.2 and v > -9)]
#f = open('purged.txt','w')
#for v in volts:
#	f.write(v)
#	f.write('\n')
#
#f.close()



