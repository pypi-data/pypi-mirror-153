

def iFDOFieldDefinitionFromMarkdownTableToDictStr(mdFile:str, altFields:dict={'image-depth':['image-altitude'],'image-altitude':['image-depth']}):
	""" reads field defintions from tables in markdown files and return str to create dict in variables.py"""
	retStrs = []
	retDict ={}
	with open(mdFile,'r') as f:
		content = f.readlines()
	for line in content:
		fields = line.split('|')
		if len(fields) >= 3:
			fields = [field.strip() for field in fields if field.strip() != ""]
			if fields[0][0:len("image")] == "image":
				name = fields[0]
				format = fields[1]
				comment = fields[2]
				allowedValues = None
				# data type
				if format.lower() == 'string':
					format = None # is default
				elif format.lower() == "float":
					format = "dataTypes.float"
				elif format.lower() == "int":
					format = "dataTypes.int"
				elif format.lower() == 'text':
					format = "dataTypes.text"
				elif format.lower() == 'list':
					format = "dataTypes.list"
				elif format.lower() == 'uuid':
					format = "dataTypes.uuid"
				elif format.lower() == 'dict':
					format = "dataTypes.dict"
				# list of allowed values
				elif format[0] != '[' and format[-1] != ']' and len(format.split(',')) > 1:
					allowedValues = format.split(',')
					format = None
				else:
					print("Unhandled format: " + format + " added to comment")
					comment += "\nFormat: " + format
					format = None
				
				tmpDict = {'comment':comment}
				if not format is None:
					tmpDict['dataType'] = format
				if not allowedValues is None:
					tmpDict['valid'] = [e.strip() for e in allowedValues]
				if name in altFields:
					tmpDict['alt-fields'] = altFields[name]
				
				parentDict = retDict
				# check for sub-fields
				if len(name.split(":")) > 1:
					orig_name = name
					for field in orig_name.split(":")[:-1]:
						if not field in parentDict:
							parentDict[field] = {'subFields':{}}
						elif not 'subFields' in parentDict[field]:
							parentDict[field]['subFields'] = {}
						parentDict = parentDict[field]['subFields']
					name = orig_name.split(":")[-1]
				parentDict[name] = tmpDict
				
	# create pastable string to create dict
	for field in retDict:
		line = str("'"+field+"'" + ":")
		if 'subFields' in retDict[field]:
			line += str({k:v for k,v in retDict[field].items() if k != 'subFields'})[:-1]+ ","
			line += "\n"
			line += "\t\'subFields\':{"
			for subField in retDict[field]['subFields']:
				line+="\n\t\t\'"+subField+"\':" + str( retDict[field]['subFields'][subField]) + ","
			line += "},},"
			#line+= pprint.pformat(retDict[field], indent=4)
		else:
			line+= str(retDict[field]).replace("\\'","\'") + ","
		# remove quites from dataType
		start = 0
		while line.find('dataType',start) != -1:
			dataTypeStartIndex = line.find('dataType',start) + len('dataType')+1
			dataTypeEndIndex = line.find(',',dataTypeStartIndex)
			line = line[0:dataTypeStartIndex] + line[dataTypeStartIndex:dataTypeEndIndex].replace('\'','') + line[dataTypeEndIndex::]
			start = dataTypeEndIndex
		retStrs.append(line)

	return "\n".join(retStrs)