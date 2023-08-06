from jft.fake.printer import f as FP
def f(x, p=print):
  if isinstance(x, list):
    x = '\n'.join(x)
  p(x)
  return False

def t_0():
  _fake_printer = FP()
  observation = f('abc', _fake_printer)
  expectation = False
  return all([
    _fake_printer.history[0] == 'abc',
    observation == expectation
  ])

def t_1():
  _fake_printer = FP()
  observation = f(['abc', '123', 'xyz'], _fake_printer)
  expectation = False
  return all([
    _fake_printer.history[0] == 'abc\n123\nxyz',
    observation == expectation
  ])

def t():
  if not t_0(): print("t_0() Failed"); return False
  if not t_1(): print("t_1() Failed"); return False
  return True
