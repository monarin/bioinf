""" translates transcript coordinates to genomic coordinates
or vise versa"""

#Define exceptions
class TranslatorError(Exception): pass
class InvalidTranscriptName(TranslatorError): pass
class InvalidTranscriptCoordinate(TranslatorError): pass
class InvalidChromosomeName(TranslatorError): pass
class InvalidChromosomeCoordinate(TranslatorError): pass

import re, argparse
import readCIGAR
import readQuery

def createTranslateTbl(CIGARObj, mode='TR2CHR'):
	"""create a table of matching starting positions for
	transcript and genomic coordinates"""
	translateTbl = {}
	for TRName, TRVal in CIGARObj.items():
		for CHRName, CHRVal in TRVal.items():
			startingPosition, CIGARStr = CHRVal
			#convert to starting value of each section
			CIGARMatch = re.findall(r'(\d+)(\w)', CIGARStr)
			try:
				CIGARValTR = [int(pair[0]) * int(pair[1] in ('M','I')) for pair in CIGARMatch] + [0]
				CIGARValCHR = [int(pair[0]) * int(pair[1] in ('M','D')) for pair in CIGARMatch] + [0]
				if mode == 'TR2CHR':
					CIGARList = [(sum(CIGARValTR[:i]), sum(CIGARValCHR[:i])+startingPosition) \
							for i in range(len(CIGARMatch)+1)]
				else:
					CIGARList = [(sum(CIGARValCHR[:i])+startingPosition, sum(CIGARValTR[:i])) \
							for i in range(len(CIGARMatch)+1)]
			except ValueError:
				print("Error calculating CIGAR value, exiting")
				exit()
			if mode == 'TR2CHR':
				if TRName in translateTbl:
					translateTbl[TRName][CHRName] = CIGARList
				else:
					translateTbl[TRName] = {CHRName: CIGARList}
			else:
				#assume mode = 'CHR2TR'
				if CHRName in translateTbl:
					translateTbl[CHRName][TRName] = CIGARList
				else:
					translateTbl[CHRName] = {TRName: CIGARList}
	return translateTbl

def toCHR(translateTbl, TRName, TR):
	"""Input: translate table, transcript name, and transcript coordinate
	Use translateTbl to convert from transcript coordinate to
	genomic coordinate"""
	if TR < 0:
		raise InvalidTranscriptCoordinate("Transcript coodinate is invalid")
	output = []
	txt = ''
	if TRName in translateTbl:
		for CHRName, translateTR in translateTbl[TRName].items():
			for i in range(len(translateTR)):
				TRCoord, CHRCoord = translateTR[i]
				prevCHRCoord = 0 if i == 0 else translateTR[i-1][1]
				if TRCoord > TR: break
			CHRMap = CHRCoord-(TRCoord-TR)
			if CHRMap > CHRCoord:
				raise InvalidTranscriptCoordinate("Transcript coodinate does not exist")
			elif CHRMap < prevCHRCoord:
				CHRMap = 'I'+str(CHRCoord)
			output += [(TRName, TR, CHRName, CHRMap)]
			txt += TRName+'\t'+str(TR)+'\t'+CHRName+'\t'+str(CHRMap)+'\n'
	else:
		raise InvalidTranscriptName("Transcript name not found in input 1")
	return output, txt

def toTR(translateTbl, CHRName, CHR):
	"""Input: translate table, chromosome name, and chromosome coordinate
	Use translateTbl to convert from chromosome coordinate to
	transcript coordinate"""
	if CHR < 0:
		raise InvalidChromosomeCoordinate("Chromosome coodinate is invalid")
	output = []
	txt = ''
	if CHRName in translateTbl:
		for TRName, translateTR in translateTbl[CHRName].items():
			for i in range(len(translateTR)):
				CHRCoord, TRCoord = translateTR[i]
				prevTRCoord = 0 if i == 0 else translateTR[i-1][1]
				if CHRCoord > CHR: break
			TRMap = TRCoord-(CHRCoord-CHR)
			if TRMap > TRCoord:
				raise InvalidChromosomeCoordinate("Chromosome coodinate does not exist")
			elif TRMap < prevTRCoord:
				TRMap = 'D'+str(TRCoord)
			output += [(CHRName, CHR, TRName, TRMap)]
			txt += CHRName+'\t'+str(CHR)+'\t'+TRName+'\t'+str(TRMap)+'\n'
	else:
		raise InvalidChromosomeName("Chromosome name not found in input 1")
	return output, txt

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
			description="Translator between transcript and genomic coordinates")
	parser.add_argument(
			'input1',
			metavar='INPUT1',
			help = 'A four column (tab-separated) file containing the transcripts')
	parser.add_argument(
			'input2',
			metavar='INPUT2',
			help = 'A two column (tab-separated) file indicating a set of queries')
	args = parser.parse_args()
	CIGARObj = readCIGAR.read(args.input1)
	query = readQuery.read(args.input2)
	translateTbl = createTranslateTbl(CIGARObj)
	txt = ''.join([toCHR(translateTbl, TRPair[0], TRPair[1])[1] for TRPair in query])
	print('Transcript to genmoic coordinate translator\nOUTPUT:')
	print(txt)


