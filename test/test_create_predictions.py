import unittest
import shutil
import sys
import  os
import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict
import filecmp



# Allow us to import files from "train'

train_dir = str(Path.cwd().parent / "train")
if train_dir not in sys.path:
    sys.path.append(train_dir)
from create_predictions import get_suggestions, make_csv_output

class CreatePredictionsTestCase(unittest.TestCase):
    def setUp(self):
       print("Test setup")

    def tearDown(self):
        if os.path.exists("untagged.csv"):
            os.remove("untagged.csv")
        if os.path.exists("tagged_preds.csv"):
            os.remove("tagged_preds.csv")

    def test_make_csv_output(self):
        all_predictions = np.load('all_predictions.npy')
        basedir = Path("board_images_png")
        N_IMAGES = 4
        CV2_COLOR_LOAD_FLAG = 1
        all_image_files = list(basedir.rglob("*.png"))[0:N_IMAGES]
        all_names = []
        all_names += [("board_images_png", filename.name) for filename in all_image_files ]

        all_sizes = [cv2.imread(str(image), CV2_COLOR_LOAD_FLAG).shape[:2] for image in all_image_files]
        untagged_output = 'untagged.csv'
        tagged_output = 'tagged_preds.csv'
        already_tagged = defaultdict(set)
        make_csv_output(all_predictions, all_names, all_sizes, untagged_output, tagged_output, already_tagged,
                        user_folders = True)

        self.assertEqual(filecmp.cmp('untagged.csv', 'untagged_source.csv'), True, "generated untagged.csv is correct")

if __name__ == '__main__':
    unittest.main()
