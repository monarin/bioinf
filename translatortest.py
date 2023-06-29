"""Unit test for translator.py"""
import translator
import unittest


class KnownValues(unittest.TestCase):
    CIGARObj = {"TR1": {"CHR1": (3, "8M7D6M2I2M11D7M")}, "TR2": {"CHR2": (10, "20M")}}
    knownTranslateTbl_TR2CHR = {
        "TR1": {
            "CHR1": [
                (0, 3),
                (8, 11),
                (8, 18),
                (14, 24),
                (16, 24),
                (18, 26),
                (18, 37),
                (25, 44),
            ]
        },
        "TR2": {"CHR2": [(0, 10), (20, 30)]},
    }
    knownTranslateTbl_CHR2TR = {
        "CHR1": {
            "TR1": [
                (3, 0),
                (11, 8),
                (18, 8),
                (24, 14),
                (24, 16),
                (26, 18),
                (37, 18),
                (44, 25),
            ]
        },
        "CHR2": {"TR2": [(10, 0), (30, 20)]},
    }
    knownValuesToCHR = (
        ("TR1", 4, "CHR1", 7),
        ("TR1", 14, "CHR1", "I24"),
        ("TR1", 0, "CHR1", 3),
        ("TR1", 24, "CHR1", 43),
        ("TR2", 0, "CHR2", 10),
        ("TR1", 13, "CHR1", 23),
        ("TR2", 10, "CHR2", 20),
    )
    knownValuesToTR = (
        ("CHR1", 7, "TR1", 4),
        ("CHR1", 12, "TR1", "D8"),
        ("CHR2", 10, "TR2", 0),
        ("CHR1", 23, "TR1", 13),
        ("CHR2", 20, "TR2", 10),
    )

    def testCreateTranslateTbl(self):
        """createTranslateTbl should give known result"""
        result_TR2CHR = translator.createTranslateTbl(self.CIGARObj)
        self.assertEqual(self.knownTranslateTbl_TR2CHR, result_TR2CHR)
        result_CHR2TR = translator.createTranslateTbl(self.CIGARObj, mode="CHR2TR")
        self.assertEqual(self.knownTranslateTbl_CHR2TR, result_CHR2TR)

    def testToCHRKnownValues(self):
        """toCHR should give known result with known input"""
        translateTbl = translator.createTranslateTbl(self.CIGARObj)
        for item in self.knownValuesToCHR:
            TRName, TR, CHRName, CHR = item
            result, _ = translator.toCHR(translateTbl, TRName, TR)
            self.assertEqual([item], result)

    def testToTRKnownValue(self):
        """toTR should give known result with known input"""
        translateTbl = translator.createTranslateTbl(self.CIGARObj, mode="CHR2TR")
        for item in self.knownValuesToTR:
            CHRName, CHR, TRName, TR = item
            result, _ = translator.toTR(translateTbl, CHRName, CHR)
            self.assertEqual([item], result)


if __name__ == "__main__":
    unittest.main()
