Translator.py

DESCRIPTION:

		Transcript to/from transcript coordinate to genomic coodinates
		- Reads in input1.txt (see below) and create a translation table
			that store matching starting coordinates between transcript and
			genomic sequences. Currently support CIGAR formats are 'M', 'I',
			and 'D'
		- The coordinates can be mapped to/from transcript and genomic
			coordinate using this formula:
			mappedCoordinate = toCooridnate - (fromCoordinate - queryCoordinate) 
		- Boudary condition is tested. For insertion, 'I' will be output
			as a prefix of the beginning coordinate of the next section.
			(for deletion, 'D')
		- The algorithm requires minimal space for the conversion. 
			Only two arrays of size N-pair CIGAR string are used for the
			calculation.

USAGE: 

		python translator.py test/input1.txt test/input2.txt

INPUT:

		input1.txt
		A four column (tab-separated) file containing the transcripts
		- Column 1: Transcript Name
		- Column 2: Chromosome Name
		- Column 3: Starting Position
		- Column 4: CIGAR string
		
		input2.txt
		A two column (tab-separated) file indicating a set of queries
		- Column 1: Transcript Name
		- Column 2: Transcript Coordinate

UNIT TEST:
	
	python translatortest.py -v
	python readCIGARtest.py -v
	python readQuerytest.py

FUTURE DEVELOPMENT:
	
	- Reverse orientation from 5' to 3' can be done by modifying 
		translate table and coordinate mapping equations.
	- Translator engine has a conversion module for translating genomic 
		coordinate to transcript coordinate (toTR). Refactor works include 
		modification of readQuery.py to read in different query format.
	- A range mapping can be done by extending the translation table.
	- To support online/external transcripts, consider using APIs from
		NCBI. 
	



