import os
import uuid
import hashlib
import datetime
import threading
import time
import ast

import mariqt.variables as miqtv


def assertExists(path):
	""" Asserts that a file/folder exists and otherwise terminates the program"""
	if not os.path.exists(path):
		raise NameError("Could not find: " + path)


def assertSlash(path):
	""" Asserts that a path string to a directory ends with a slash"""
	#if not os.path.isdir(path):
	#	return path
	if not path[-1] == "/":
		return path + "/"
	else:
		return path

def toUnixPath(path):
	path = path.replace("\\","/").replace("\\\\","/").replace("\t","/t").replace("\f","/f").replace("\n","/n")
	return path


def humanReadable(val):
	""" Turns a number > 0 (int/float) into a shorter, human-readable string with a size character (k,M,G,...)"""

	sign = 1
	if val < 0:
		sign = -1
		val *= -1

	if val < 1:
		suffixes = ['m','µ','n','p','a','f']
		idx = -1
		while val < 0.001:
			val *= 1000
			idx += 1
		if idx >= 0:
			return str(sign*round(val))+suffixes[idx]
		else:
			return str(sign*val)
	else:
		suffixes=['k','M','G','T','P','E']
		idx = -1
		while val > 1000:
			val /= 1000
			idx += 1
		if idx >= 0:
			return str(sign*round(val))+suffixes[idx]
		else:
			return str(sign*val)

def uuid4():
	""" Returns a random UUID (i.e. a UUID version 4)"""
	return uuid.uuid4()


def is_valid_uuid(value):
	""" Retruns whether value is a valid UUIV version 4"""
	try:
		uuid.UUID(str(value), version=4)
		return True
	except ValueError:
		return False


def sha256HashFile(path):
	""" Returns the SHA256 hash of the file at path"""
	sha256_hash = hashlib.sha256()
	with open(path,"rb") as f:
		for byte_block in iter(lambda: f.read(4096),b""):
			sha256_hash.update(byte_block)
		return sha256_hash.hexdigest()

def md5HashFile(path):
	""" Returns the MD5 hash of the file at path"""
	md5_hash = hashlib.md5()
	with open(path, "rb") as f:
		for byte_block in iter(lambda: f.read(4096), b""):
			md5_hash.update(byte_block)
	return md5_hash.hexdigest()


def rgb2hex(r,g,b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def parseFileDateTimeAsUTC(fileName:str):
	""" Parses datetime from from file name according to file naming convention <event>_<sensor>_<date>_<time>.<ext>
	with date fromat yyyymmdd and time format HHMMSS[.f] with [] being optional. Throws exception if unsuccessfull"""

	split = fileName.split("_")
	try:
		pos = split[-1].rfind(".")
		dt_str = split[-2]+"_"+split[-1][0:pos] + "+0000"
	except:
		raise Exception("can not parse time from file name " + fileName)
	
	try:
		dt = datetime.datetime.strptime(dt_str,miqtv.date_formats['mariqt_files']+".%f%z")
	except:
		try:
			dt = datetime.datetime.strptime(dt_str,miqtv.date_formats['mariqt_files']+"%z")
		except:
			raise Exception("can not parse time from file name " + fileName)
	return dt


def recursivelyUpdateDicts(oldDict:dict, newDict:dict, mutuallyExclusives:list=[]):
	""" Recursively updates oldDict with newDict """
	log = []
	for newItem in newDict:
		# special case for updating video items which may contain of a list of dicts, each with a different timestamp which have to be checked and them get updated
		try:
			# both items are not lists
			if newDict[newItem]['image-datetime'] != oldDict[newItem]['image-datetime']:
				oldDict[newItem] = [oldDict[newItem]] # will be handled in bellow
		except:
			# TODO write to log?
			pass
		try:
			# at least one is a list
			if isinstance(newDict[newItem],list) or isinstance(oldDict[newItem],list):
				if not isinstance(newDict[newItem],list):
					# override (delete) if new item is empty
					if newDict[newItem] == "":
						oldDict[newItem] = newDict[newItem]
						continue
					newDictNewItemList = [newDict[newItem]]
					oldDictNewItemList = oldDict[newItem]
				elif not isinstance(oldDict[newItem],list):
					newDictNewItemList = newDict[newItem]
					oldDictNewItemList = [oldDict[newItem]]
				else:
					newDictNewItemList = newDict[newItem]
					oldDictNewItemList = oldDict[newItem]

				for newDictItem in newDictNewItemList:
					if not 'image-datetime' in newDictItem:
						# try to parste datetime from file name and add it to new data
						try:
							dt = parseFileDateTimeAsUTC(newItem)
							newDictItem['image-datetime'] = dt.strftime(miqtv.date_formats['mariqt'])
						except:
							log += [str(newDictItem) + " does not contain \'image-datetime\', is ignored"]
							continue

					matchFound = False
					i = 0
					for oldDictItem in oldDictNewItemList:
						#print("oldDictItem",oldDictItem)
						if not 'image-datetime' in oldDictItem:
							log += [str(newDictItem) + " does not contain \'image-datetime\', is removed"]
							del oldDictNewItemList[i]
							continue

						i += 1 
						if newDictItem['image-datetime'] == oldDictItem['image-datetime']:
							log += recursivelyUpdateDicts(oldDictItem,newDictItem,mutuallyExclusives)
							matchFound = True
							break

					if not matchFound:
						oldDictNewItemList.append(newDictItem) # TODO checkMutuallyExclusive wouldnt work, theoretically one could write altitude at timestamp 1 and depth at timestamp 2
				# sort by date time
				oldDictNewItemList = sorted(oldDictNewItemList, key=lambda d: d['image-datetime']) 
				oldDict[newItem] = oldDictNewItemList
				continue
		except Exception as ex:
			#print("Ex",str(ex))
			pass

		# default case
		if (not newItem in oldDict) or (not isinstance(newDict[newItem],dict) or (not isinstance(oldDict[newItem],dict))): # was mit liste?
			oldDict[newItem] = newDict[newItem]
			log += checkMutuallyExclusive(mutuallyExclusives,oldDict,newDict,newItem)
		else:
			log += recursivelyUpdateDicts(oldDict[newItem],newDict[newItem],mutuallyExclusives)
	return log

def checkMutuallyExclusive(mutuallyExclusives:list,oldDict:dict,newDict:dict,newItem:str):
	""" expects a list of lists with mutually exclusive field names """
	log = []
	for mutuallyExclusive in mutuallyExclusives:
		if len(mutuallyExclusive) != 0:
			if newItem in mutuallyExclusive and newDict[newItem] != "":
				toExclude = [e for e in mutuallyExclusive if e != newItem]
				for exclude in toExclude:
					if exclude in oldDict:
						oldDict[exclude] = ""
						log.append("Removed field " + exclude + " since mutually exclusive to added field " + newItem)
	return log

def recursivelyRemoveEmptyFields(oldObj):
	""" Return a dict/list in which all fields in all levels of oldObj that have empty string values are removed """

	if isinstance(oldObj,dict):
		newDict =  {k: v for k, v in oldObj.items() if v != "" and __isNotEmptyDict(v)}
		newEmptyDicts = []
		for item in newDict:
			if isinstance(newDict[item],dict) or isinstance(newDict[item],list):
				newDict[item] = recursivelyRemoveEmptyFields(newDict[item])
				if newDict[item] == {} or newDict[item] == []:
					newEmptyDicts.append(item)
		for item in newEmptyDicts:
			del newDict[item]
		return newDict

	elif isinstance(oldObj,list):
		newList =  [v for v in oldObj if v != "" and __isNotEmptyDict(v)]
		newEmptyList = []
		for i in range(len(newList)):
			if isinstance(newList[i],list) or isinstance(newList[i],dict):
				newList[i] = recursivelyRemoveEmptyFields(newList[i])
				if newList[i] == [] or newList[i] == {}:
					newEmptyList.append(newList[i])
		for item in newEmptyList:
			newList.remove(item)
		return newList
	else:
		raise Exception("Must be dict or list",oldObj)


def recursiveEval(obj):
	""" runs ast.literal_eval on all string elements in obj (list or dict) """
	if isinstance(obj,dict):
		for k,v in obj.items():
			if isinstance(v,str):
				try:
					val = ast.literal_eval(v)
					obj[k] = val
				except Exception:
					pass
			elif isinstance(v,list) or isinstance(v,dict):
				recursiveEval(obj[k])
	elif isinstance(obj,list):
		for i in range(len(obj)):
			if isinstance(obj[i],str):
				try:
					val = ast.literal_eval(obj[i])
					obj[i] = val
				except Exception:
					pass
			elif isinstance(obj[i],list) or isinstance(obj[i],dict):
				recursiveEval(obj[i])
	else:
		raise Exception("Must be dict or list ",obj)

def __isNotEmptyDict(obj):
	if isinstance(obj,dict) and not obj:
		return False 
	if isinstance(obj,list) and obj == []:
		return False
	return True

def reformatImageDateTimeStr(data,format=miqtv.date_formats["mariqt"]):
	""" reformats data or any field 'image-datetime' within data to MarIQT standard time string format. Throws exception if unsuccessfull """
	if isinstance(data,list):
		for item in data:
			if isinstance(item,dict) or isinstance(item,list):
				reformatImageDateTimeStr(item,format)
	elif isinstance(data,dict):
		for item in data:
			if isinstance(data[item],dict) or isinstance(data[item],list):
				reformatImageDateTimeStr(data[item],format)
			elif item == 'image-datetime':
				dt = datetime.datetime.strptime(str(data[item]),format)
				data[item] = dt.strftime(miqtv.date_formats["mariqt"])
	else:
		dt = datetime.datetime.strptime(data,format)
		data = dt.strftime(miqtv.date_formats["mariqt"])
		

def runningOnWindows():
	return os.name == 'nt'

class PrintLoadingMsg:
	""" prints and overwrites msg followed by moving dots """
	def __init__(self,msg:str,dotsInteval:float = 0.5):
		""" prints and overwrites msg followed by moving dots """

		if msg[-1] != " ":
			msg += " "
		self.msg = msg
		self.myThread = threading.Thread(target=self.printLine, args=(msg,dotsInteval))
		self.myThread.start()

	def printLine(self,msg,dotsInteval):
		t = threading.currentThread()
		dots = ""
		while getattr(t, "do_run", True):
			if len(dots) != 3:
				dots +=  "."
			else:
				dots = ""
			print(msg + dots + "   ", end="\r", flush=True)
			time.sleep(dotsInteval)

	def stop(self):
		if not self.myThread.is_alive():
			return
		self.myThread.do_run = False
		self.myThread.join()
		print("".join([" "]*(len(self.msg)+4)), end="\r", flush=True) 
		time.sleep(0.5)
		print("".join([" "]*(len(self.msg)+4)), end="\r", flush=True)


class PrintKnownProgressMsg:
	""" prints and overwrites msg followed by progress status i/N """
	def __init__(self,msg:str,N:int,modulo:int = 2):
		if msg[-1] != " ":
			msg += " "
		self.msg = msg
		self.N = N
		self.modulo = modulo
		self.i = 0

	def progress(self):
		""" increment progress by one and print """
		self.i += 1
		if self.i%self.modulo == 0:
			print(self.msg + str(self.i) + "/" + str(self.N), end="\r", flush=True)

	def clear(self):
		""" clear last output """
		print("".join([" "]*(len(self.msg)+ 2*len(str(self.N)) + 10 )), end="\r", flush=True) # clear line
		time.sleep(0.5)
		print("".join([" "]*(len(self.msg)+ 2*len(str(self.N)) + 10 )), end="\r", flush=True) # clear line


class IfdoException(Exception):
	""" Exception type purely related to iFDO issues """
	pass

