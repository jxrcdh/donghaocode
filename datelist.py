#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
__author__='donghao'
def getDatelist(sourceFile,startdate,enddate,calendar_file):
	dateregex=r'(\d{4})-(\d{2})-(\d{2})'
	m=re.match(dateregex,startdate)
	if m is None:
		raise NameError('input wrong date')
	else:
	start_date=[m.group(1),m.group(2),m.group(2)]
	
	m=re.match(dateregex,enddate)
	if m is None:
		raise NameError('input wrong date')
	end_date=[m.group(1),m.group(2),m.group(2)]
	startYear=int(start_data[0])
	endYear=int(end_date[0])
	while startYear<=endYear:
if __name__=='__main__':
	mainfun()
