import argparse

from helper_functions import *
from hmm_functions import *
from bcf_vcf import *

import numpy as np
import json
from collections import defaultdict
import os
import itertools
import difflib
import sys 
from glob import glob


def test_Maketestdata():
    assert len(np.zeros(10)) == 10


def test_something():
    assert 0 == 0

def test_convert_to_bases():
    genotype1 = convert_to_bases('0/1', 'A', 'T')
    assert genotype1 == 'AT'

def test_get_consensus():
    prefix, postfix, values = get_consensus(['chr1.vcf', 'chr2.vcf', 'chr3.vcf'])
    assert prefix == 'chr'
    assert postfix == '.vcf'
    assert values == set(['1', '2', '3'])