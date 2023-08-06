f = lambda σ: ''.join([_ if _ != "'" else "''" for _ in σ])
t = lambda: f("abc'def'ghi") == "abc''def''ghi"