#!/usr/bin/env python
# coding=utf-8

"""
unit tests
"""

from __future__ import print_function, unicode_literals


from main import gen_obj


def test_gen_obj():
    obj = gen_obj()
    assert "id" in obj
    assert "key3" in obj
