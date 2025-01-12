from functools import reduce

def chain(*funcs):
  return reduce(lambda f, g: lambda x: g(f(x)), funcs)
