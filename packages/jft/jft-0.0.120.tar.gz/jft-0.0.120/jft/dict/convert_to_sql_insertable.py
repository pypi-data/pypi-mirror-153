from jft.string.double_single_quotes import f as dub1qt
f = lambda Δ: {k: dub1qt(v) if "'" in str(v) else v for (k, v) in Δ.items()}
t = lambda: all([f({'a': "O'Neil", 'b': 'B'}) == {'a': "O''Neil", 'b': 'B'}])