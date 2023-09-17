from app.conversion import convert_to_wav_working_format
from app.produceImage import generate_soundwave_image

import unittest
import ffmpeg

from PIL import Image

class TestClass(unittest.TestCase):
    def testingConversionOfAudio(self):
        state = convert_to_wav_working_format("./test/9 non c'e' male.m4a","./test/9 non c'e' male.wav")
        self.assertEqual(state,0)
    def testingProductionOfImage(self):
        generate_soundwave_image("./test/9 non c'e' male.wav","./test","9 non c'e' male.png")
        expected_image_filename = "./test/ideal.png"
        expected_image = Image.open(expected_image_filename)

        generated_image_filename = "./test/9 non c'e' male.png"
        generated_image = Image.open(generated_image_filename)

        self.assertEqual(generated_image.size, expected_image.size)
        self.assertEqual(list(generated_image.getdata()), list(expected_image.getdata()))


if __name__ == "__main__":
    unittest.main()