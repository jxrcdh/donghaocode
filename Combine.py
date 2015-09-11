#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__='donghao'

import os
import sys
import re
import numpy as np

def mainfun():
	args = sys.argv
	if len(args)<6:
		print 'please input more arguments'
		print 'usage: python Combine.py [path] [YYYYMM/YYYY] [fillstr] [savepath] [savetype]'
		exit()
	elif len(args)>6:
		print 'input too many arguments'
		print 'usage: python Combine.py [path] [YYYYMM/YYYY] [fillstr] [savepath] [savetype]'
		exit()
	else:
		rootPath=args[1]											#datapath
		combinedate=args[2]										#need to comb
		fillstr=args[3]
		savepath=args[4]
		savetype=args[5]
	substrs=rootPath.split('/')

	pathinfo=substrs[len(substrs)-1]
	if pathinfo=='' and len(substrs)>1:
		pathinfo=substrs[len(substrs)-2]
	pathregex=r'\d{1,2}:\d{1,2}_(\d+)_(\d+\w+)_\w+$'
	m=re.match(pathregex,pathinfo)
	if m is None:
		print 'wrong format of the path'
		exit()
	else:
		fillsize=int(m.group(1))
	
	datedirs=[]
	contract_set=set([])
	savePath=os.path.join(savepath,combinedate)
	if not os.path.exists(savePath):
		os.mkdir(savePath)
	if len(combinedate) == 4:
		onePath=readYearContract(rootPath,combinedate,contract_set,datedirs)
	elif len(combinedata) == 6:
		onePath=readMonthContract(rootPath,combinedate,contract_set,datedirs)
	else:
		exit()
#	print len(contract_set)
#	print datedirs
	Indicators=getIndicators(onePath)
	print Indicators
	filldata=np.empty(fillsize)
	filldata[:]=np.nan

	process_log=[]

	for contract in contract_set:
		Indicators_dict={}
		for indi in Indicators:
			Indicators_dict[indi]=np.empty(0)
		for datedir in datedirs:
			combineOneDay(datedir,contract,Indicators_dict,filldata,fillsize,process_log)		
			write_combine_contract(contract,Indicators_dict,savePath,savetype)
	write_log(os.path.join(savepath,'combine.log'),process_log)

def combineOneDay(datedir,contract,Indicators,filldata,fillsize,process_log):
	count=0
	for indicator in Indicators:
		indicator_file=os.path.join(datedir,contract)
		indicator_file=os.path.join(indicator_file,indicator)
		if os.path.exists(''.join([indicator_file,'.csv'])):
			data=readCsvIndicator(''.join([indicator_file,'.csv']))
			Indicators[indicator]=np.append(Indicators[indicator],data)
			if len(data)<fillsize:
				process_log.append(''.join([contract,'|',datedir,'|',indicator,'lossdata\n']))
			else:
				pass
		elif os.path.exists(''.join([indicator_file,'.bin'])):
			data=readBinIndicator(''.join([indicator_file,'.bin']))
			Indicators[indicator]=np.append(Indicators[indicator],data)
			if len(data)<fillsize:
				process_log.append(''.join([contract,'|',datedir,'|',indicator,'lossdata\n']))
			else:
				pass
		else:
			Indicators[indicator]=np.append(Indicators[indicator],filldata)
			count=count+1
		
#	if count != 0:
#		print contract
	if count != len(Indicators):
		process_log.append(''.join([contract,'|',datedir,'|','lossIndicators\n']))

def readCsvIndicator(filepath):
	return np.loadtxt(filepath)

def readBinIndicator(filepath):
	return np.fromfile(filepath)
def readYearContract(rootPath,combineYear,contract_set,datedirs):
	onePath=''
	month=1
	while month<=12:
		day=1
		while day<=31:
			datedir=os.path.join(rootPath,''.join([combineYear,'%02d'%month,'%02d'%day]))
			if os.path.exists(datedir):
				datedirs.append(datedir)
				dirs=os.listdir(datedir)
				for d in dirs:
					if d[0]=='.':
						pass
					else:
						if onePath=='':
							onePath=os.path.join(datedir,d)
						contract_set.add(d)
			else:
				pass
			day=day+1
		month=month+1
	return onePath
def readMonthContract(rootPath,combineMonth,contract_set,datedirs):
	onePath=''
	day=1
	dayCount=0
	while day<=31:
		datedir=os.path.join(rootPath,''.join([combineMonth,'%02d'%day]))
		if os.path.exists(datedir):
			datedirs.append(datedir)
			dirs=os.listdir(datedir)
			for d in dirs:
				if d[0]=='.':
					pass
				else:
					if onePath=='':
							onePath=os.path.join(datedir,d)
					contract_set.add(d)
		else:
			pass
		day=day+1
	return onePath

def write_combine_contract(contract,Indicators,savepath,savetype):
	savedir=os.path.join(savepath,contract)
	if not os.path.exists(savedir):
		os.mkdir(savedir)
	for indicator in Indicators:
		if savetype == 'csv':
			np.savetxt(os.path.join(savedir,''.join([indicator,'.csv'])),Indicators[indicator])
		elif savetype == 'bin':
			Indicators[indicator].tofile(os.path.join(savedir,''.join([indicator,'.bin'])))
		else:
			pass
def getIndicators(path):
	indicators=[]	
	dirs=os.listdir(path)
	for f in dirs:
		if f[0]=='.':
			pass
		else:
			indicators.append(f.split('.')[0])
	return indicators
def write_log(path,process_log):
	with open(path,'w+') as f:
		f.writelines(process_log)

if __name__=='__main__':
	mainfun()
