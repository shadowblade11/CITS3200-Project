from app.conversion import convert_to_wav_working_format
from app.produceImage import generate_soundwave_image

import unittest
import ffmpeg

class TestClass(unittest.TestCase):
    def testingConversionOfAudio(self):
        state = convert_to_wav_working_format("./test/9 non c'e' male.m4a","./test/9 non c'e' male.wav")
        self.assertEqual(state,0)
    def testingProductionOfImage(self):
        pass
        # generate_soundwave_image("./test/9 non c'e' male.wav","./test","9 non c'e' male.png")




if __name__ == "__main__":
    unittest.main()