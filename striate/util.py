from pycuda.gpuarray import GPUArray
from pycuda import gpuarray
import cPickle
import os
import sys
import threading
import time
import traceback
import numpy as np

program_start = time.time()
log_mutex = threading.Lock()
def log(msg, *args, **kw):
  with log_mutex:
    caller = sys._getframe(1)
    filename = caller.f_code.co_filename
    lineno = caller.f_lineno
    now = time.time() - program_start
    if 'exc_info' in kw:
      exc = ''.join(traceback.format_exc())
    else:
      exc = None
    print >> sys.stderr, '%.3f:%s:%d: %s' % (now, os.path.basename(filename), lineno, msg % args)
    if exc:
      print >> sys.stderr, exc


class Timer:
  def __init__(self):
    self.func_time = {}
    self.last_time = 0.0

  def start(self):
    self.last_time = time.time()

  def end(self, func_name):
    ftime = time.time() - self.last_time
    if func_name in self.func_time:
      self.func_time[func_name] += ftime
    else:
      self.func_time[func_name] = ftime

  def report(self):
    dic = self.func_time
    for key in sorted(dic):
      print key, ':', dic[key]


timer = Timer()

def ceil(x, base):
  if x / base * base == x:
    return x / base
  else:
    return x / base + 1

def load(filename):
  with open(filename, 'rb') as f:
    model = cPickle.load(f)
  return model

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def isinteger(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

def string_to_int_list(str):
  str = str.strip()
  if str.find('-'):
    f = int(str[0:str.find('-')])
    t = int(str[str.find('-') + 1:-1])

    return range(f, t + 1)
  else:
    elt = int(str)
    return [elt]


def printMatrix(x, name):
  print name
  if isinstance(x, GPUArray):
    a = x.get()[:, 0]
  else:
    a = x[:, 0]

  for i in a:
    print '%.15f ' % i

def abs_mean(x):
  if isinstance(x, GPUArray):
    return (gpuarray.sum(x.__abs__()) / x.size).get().item()
  if isinstance(x, np.ndarray):
    return np.mean(np.abs(x))
