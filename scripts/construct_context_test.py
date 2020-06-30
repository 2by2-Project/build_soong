#!/usr/bin/env python
#
# Copyright (C) 2020 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Unit tests for construct_context.py."""

import sys
import unittest

import construct_context as cc

sys.dont_write_bytecode = True

def construct_contexts(arglist):
  args = cc.parse_args(arglist)
  return cc.construct_contexts(args)

classpaths = [
  '--host-classpath-for-sdk', '28', 'out/zdir/z.jar',
  '--target-classpath-for-sdk', '28', '/system/z.jar',
  '--host-classpath-for-sdk', '29', 'out/xdir/x.jar:out/ydir/y.jar',
  '--target-classpath-for-sdk', '29', '/system/x.jar:/product/y.jar',
  '--host-classpath-for-sdk', 'any', 'out/adir/a.jar:out/android.hidl.manager-V1.0-java.jar:out/bdir/b.jar',
  '--target-classpath-for-sdk', 'any', '/system/a.jar:/system/android.hidl.manager-V1.0-java.jar:/product/b.jar',
]

class ConstructContextTest(unittest.TestCase):
  def test_construct_context_28(self):
    args = ['--target-sdk-version', '28'] + classpaths
    result = construct_contexts(args)
    expect = ('class_loader_context_arg=--class-loader-context=PCL[]{PCL[out/xdir/x.jar]'
      '#PCL[out/ydir/y.jar]'
      '#PCL[out/adir/a.jar]'
      '#PCL[out/android.hidl.manager-V1.0-java.jar]{PCL[out/android.hidl.base-V1.0-java.jar]}'
      '#PCL[out/bdir/b.jar]}'
      ' ; '
      'stored_class_loader_context_arg=--stored-class-loader-context=PCL[]{PCL[/system/x.jar]'
      '#PCL[/product/y.jar]'
      '#PCL[/system/a.jar]'
      '#PCL[/system/android.hidl.manager-V1.0-java.jar]{PCL[/system/android.hidl.base-V1.0-java.jar]}'
      '#PCL[/product/b.jar]}')
    self.assertEqual(result, expect)

  def test_construct_context_29(self):
    args = ['--target-sdk-version', '29'] + classpaths
    result = construct_contexts(args)
    expect = ('class_loader_context_arg=--class-loader-context=PCL[]{PCL[out/adir/a.jar]'
      '#PCL[out/android.hidl.manager-V1.0-java.jar]{PCL[out/android.hidl.base-V1.0-java.jar]}'
      '#PCL[out/bdir/b.jar]}'
      ' ; '
      'stored_class_loader_context_arg=--stored-class-loader-context=PCL[]{PCL[/system/a.jar]'
      '#PCL[/system/android.hidl.manager-V1.0-java.jar]{PCL[/system/android.hidl.base-V1.0-java.jar]}'
      '#PCL[/product/b.jar]}')
    self.assertEqual(result, expect)

  def test_construct_context_S(self):
    args = ['--target-sdk-version', 'S'] + classpaths
    result = construct_contexts(args)
    expect = ('class_loader_context_arg=--class-loader-context=PCL[]{PCL[out/adir/a.jar]'
      '#PCL[out/android.hidl.manager-V1.0-java.jar]{PCL[out/android.hidl.base-V1.0-java.jar]}'
      '#PCL[out/bdir/b.jar]}'
      ' ; '
      'stored_class_loader_context_arg=--stored-class-loader-context=PCL[]{PCL[/system/a.jar]'
      '#PCL[/system/android.hidl.manager-V1.0-java.jar]{PCL[/system/android.hidl.base-V1.0-java.jar]}'
      '#PCL[/product/b.jar]}')
    self.assertEqual(result, expect)

if __name__ == '__main__':
  unittest.main(verbosity=2)
