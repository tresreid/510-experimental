from numpy import *
from scipy import loadtxt, optimize
import matplotlib.pyplot as plt
import os
from ROOT import TH1F, gROOT, TCanvas, gPad
import warnings 

gROOT.Reset()
c1 = TCanvas('c1', 'test', 200, 10,700, 500)

Vd = .0538
#r1 = 100000.
#r2 = 1000.
#ra = 200000.
##ra = 100000.
#rf = 22000.
v_in = 5.45
r1= 97800.
r2 = 969.
ra = 196000.
rf = 22500.


times = []
volts1 =[]
purged = True
if purged:
	for filename in os.listdir("data_purged/full"):
		curfile = "data_purged/full/%s"%(filename)
	#	print curfile
		try:
			with warnings.catch_warnings():
				warnings.simplefilter("ignore")
				times, volt = loadtxt(curfile, unpack=True, skiprows=0)
			#	times.extend(time)
				volts1.extend(volt)
				print curfile
				#print volt
				#print volts1
		except ValueError:
			continue
else:
	for directory in os.listdir("data/used"):
		curdir = "data/used/%s"%(directory)
		for filename in os.listdir(curdir):
			curfile = "data/used/%s/%s"%(directory,filename)
			time, volt = loadtxt(curfile, unpack=True, skiprows=3)
			times.extend(time)
			volts1.extend(volt)
#v2 = []
#for v in volts:
#	if v > -2.:
#		v2.append(-v)
#volts = v2
volts = [v for v in volts1 if (v<-0.2 and v > -9)]

Gfactor =(1./(rf+ra))*((r1+r2)/(v_in*r2))
#RealGshit = [(v*Gfactor) for v in volts if v< -0.2]
G_0 = 7.748092*10**(-5)
low_volt = -9#-13.
high_volt = 0#0.0

bins = 100
hist = TH1F("h1","V",bins,low_volt,high_volt)
ghist = TH1F("conductance","G",bins,low_volt*Gfactor,high_volt*Gfactor)
g0hist = TH1F("ratio","G/G0",bins,-10,0)
for v in volts:
	hist.Fill(v)
	ghist.Fill(v*Gfactor)
	g0hist.Fill(v*Gfactor/G_0)
hist.Draw("E")
c1.SaveAs("volts.pdf")
#for g in RealGshit:
#	ghist.Fill(g)
#	g0hist.Fill(g/G_0)

ghist.Draw()
c1.SaveAs("conductance.pdf")
g0hist.Draw()
c1.SaveAs("ratio.pdf")

goodbins = []
for i in range(hist.GetSize()):
	content = hist.GetBinContent(i)
	if( content > 80000.0):
		#print i, (low_volt+i*((high_volt-low_volt)/bins)),hist.GetBinContent(i)
		goodbins.append(low_volt+i*((high_volt-low_volt)/bins))

distances = []
for i in range(len(goodbins)-1):
	distances.append(abs(goodbins[i]-goodbins[i+1]))

print distances
#g = [(dis/(ra+rf))/Vd for dis in distances]
#print g

g2 = [(dis*Gfactor) for dis in distances]
print g2
