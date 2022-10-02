# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
"""Example tests used to generate screenshots."""

import pytest

def test_one_plus_one_is_two():
    pass

def test_two_plus_two_is_four():
    pass

def test_one_plus_two_is_five():
    assert 1 == 3

def test_two_times_two_is_four():
    pass

@pytest.mark.skip
def test_will_be_skipped():
    assert 0 == 1
