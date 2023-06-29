"""read query input"""

# Define exceptions
class ReadQueryError(Exception):
    pass


class InvalidColumnCount(ReadQueryError):
    pass


class InvalidTR(ReadQueryError):
    pass


class InvalidInputFile(ReadQueryError):
    pass


import re


def read(QueryFile):
    """Read input file 2 and output query
    query = [('TR1', transcriptCoordinate)]"""
    query = []
    try:
        with open(QueryFile, "r") as f:
            for line in f:
                # check columns
                cols = re.split(r"\t+", line.rstrip("\n"))
                if len(cols) != 2:
                    raise InvalidColumnCount("Number of columns is invalid")
                # check transcript coordinate
                try:
                    TR = int(cols[1])
                    if TR < 0:
                        raise InvalidTR(
                            "Transcipt coordinate should be a positive integer"
                        )
                except ValueError:
                    print("Transcript coordinate is not an integer, exiting")
                    exit()
                # all good, add item to query
                query += [(cols[0], TR)]
            if len(query) == 0:
                raise InvalidInputFile("The input file is blank")
    except IOError:
        print("The file does not exist, exiting")
        exit()
    return query
