#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import calendar
import re
__author__='donghao'
def printdate():
	args=sys.argv
	if len(args) == 2:
		print 'need more argvments'
		exit()
	elif len(args)==3:
		datestr=args[1]
		datetype=args[2]
	else:
		print 'too many argvments'
		exit()
	dates=[]
	if datetype=='2':
		dateregex=r'(\d{4})-(\d{2})'
		m=re.match(dateregex,datestr)
		days=calendar.monthrange(int(m.group(1)),int(m.group(2)))
		i=1;
		print days
		while i<=days[1]:
			dates.append(''.join([m.group(1),m.group(2),'%02d'%i]))
			i=i+1
		print dates
	else:
		pass
if __name__=='__main__':
	printdate()
