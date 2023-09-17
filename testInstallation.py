from app.conversion import convert_to_wav_working_format
from app.produceImage import generate_soundwave_image

import unittest
import os
from PIL import Image

class TestClass(unittest.TestCase):
    def testingConversionOfAudio(self):
        state = convert_to_wav_working_format("./test/9 non c'e' male.m4a","./test/9 non c'e' male.wav")
        self.assertEqual(state,0)

    def testingProductionOfImage(self):
        #making the image
        generate_soundwave_image("./test/9 non c'e' male.wav","./test","9 non c'e' male.png")
        generated_image_filename = "./test/9 non c'e' male.png"
        file_exists = os.path.isfile(generated_image_filename)
        self.assertTrue(file_exists, f"Image file not found: {generated_image_filename}")

    def testingImage(self):        
        # making the image
        generate_soundwave_image("./test/9 non c'e' male.wav","./test","9 non c'e' male.png")

        expected_image_filename = "./test/ideal.png"
        expected_image = Image.open(expected_image_filename)

        generated_image_filename = "./test/9 non c'e' male.png"
        generated_image = Image.open(generated_image_filename)

        self.assertEqual(generated_image.size, expected_image.size)
        self.assertEqual(list(generated_image.getdata()), list(expected_image.getdata()))

    @classmethod
    def tearDownClass(cls):
        generated_image_filename = "./test/9 non c'e' male.png"
        if os.path.exists(generated_image_filename):
            os.remove(generated_image_filename)
        generated_wav_filename = "./test/9 non c'e' male.wav"
        if os.path.exists(generated_wav_filename):
            os.remove(generated_wav_filename)

if __name__ == "__main__":
    unittest.main()