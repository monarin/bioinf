"""Unit test for readquery.py"""
import readQuery
import unittest

class readQueryBadInput(unittest.TestCase):
	def testBadColumn(self):
		"""read should fail with incorrect column count"""
		self.assertRaises(readQuery.InvalidColumnCount, readQuery.read, 'test/test_bad_column_input2.txt')

	def testBadTR(self):
		"""read should fail with invalid transcript coordinate"""
		self.assertRaises(readQuery.InvalidTR, readQuery.read, 'test/test_bad_TR_input2.txt')

	def testEmptyInput(self):
		"""read should fail if the input file is empty"""
		self.assertRaises(readQuery.InvalidInputFile, readQuery.read, 'test/test_empty_input.txt')

if __name__ == "__main__":
		unittest.main()
