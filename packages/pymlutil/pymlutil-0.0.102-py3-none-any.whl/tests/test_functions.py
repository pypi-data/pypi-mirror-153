import sys
import os
import numpy as np
import cv2
import json
from collections import defaultdict
import unittest
import torch

sys.path.insert(0, os.path.abspath('')) # Test files from current path rather than installed module
from pymlutil.functions import *



class Test(unittest.TestCase):
    def test_GaussianBasis(self):
        self.assertEqual(GaussianBasis(torch.tensor(0.0), zero=0.0, sigma=0.33), 1.0)

    def test_GaussianExponential(self):
        vx = 1
        vy = 2
        px = 3
        py = 4
        power = 2
        expf =  Exponential(vx=vx, vy=vy, px=px, py=py, power=power)
        x = np.arange(vx-1, px+1, 0.1)  
        y = expf.f(x)
        assert(y[0] == vy)
        assert(y[-1] == py)



if __name__ == '__main__':
    unittest.main()