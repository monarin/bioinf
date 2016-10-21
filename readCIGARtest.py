"""Unit test for readCIGAR.py"""
import readCIGAR
import unittest

class readCIGARBadInput(unittest.TestCase):
	def testBadColumn(self):
		"""read should fail with incorrect column count"""
		self.assertRaises(readCIGAR.InvalidColumnCount, readCIGAR.read, 'test/test_bad_column_input1.txt')

	def testBadStartingPosition(self):
		"""read should fail with invalid starting position"""
		self.assertRaises(readCIGAR.InvalidStartingPosition, readCIGAR.read, 'test/test_bad_startingposition_input1.txt')

	def testEmptyInput(self):
		"""read should fail if the input file is empty"""
		self.assertRaises(readCIGAR.InvalidInputFile, readCIGAR.read, 'test/test_empty_input.txt')

if __name__ == "__main__":
		unittest.main()
