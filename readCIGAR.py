"""read CIGAR input"""

# Define exceptions
class ReadCIGARError(Exception):
    pass


class InvalidColumnCount(ReadCIGARError):
    pass


class InvalidStartingPosition(ReadCIGARError):
    pass


class InvalidInputFile(ReadCIGARError):
    pass


import re


def read(CIGARFile):
    """Read input file 1 and output CIGARObj
    CIGARObj := {'TR': {CHR: (startingPosition, CIGARString)}}'"""
    CIGARObj = {}
    try:
        with open(CIGARFile, "r") as f:
            for line in f:
                # check columns
                cols = re.split(r"\t+", line.rstrip("\n"))
                if len(cols) != 4:
                    raise InvalidColumnCount("Number of columns is invalid")
                # check starting position
                try:
                    startingPosition = int(cols[2])
                    if startingPosition < 0:
                        raise InvalidStartingPosition(
                            "Starting position should be a positive integer"
                        )
                except ValueError:
                    print("Starting position is not an integer, exiting")
                    exit()
                # all good, add item to CIGARObj
                if cols[0] in CIGARObj:
                    CIGARObj[cols[0]][cols[1]] = (startingPosition, cols[3])
                else:
                    CIGARObj[cols[0]] = {cols[1]: (startingPosition, cols[3])}
            if len(CIGARObj) == 0:
                raise InvalidInputFile("The input file is blank")
    except IOError:
        print("The file does not exist, exiting")
        exit()
    return CIGARObj
