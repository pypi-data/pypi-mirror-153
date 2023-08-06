f = lambda x: isinstance(x, str) or x is None
t = lambda: all([f(""), f("a"), f(None), not any([f(_) for _ in [0, 1.5]])])