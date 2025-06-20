Echo

A simple `strings` call revealed the flag

SVBRG{HEXEDITING}

The hint makes me think something else was intended


Indeed, it could be opened with hexedit and the string is present at the very bottom:

002B3CB0   FA F9 3F C3  B6 91 ED 63  D2 9C 6D D3  6B F4 F2 F2  ..?....c..m.k...
002B3CC0   FC BB 6B FF  D9 53 56 42  52 47 7B 48  45 58 45 44  ..k..SVBRG{HEXED
002B3CD0   49 54 49 4E  47 7D                                  ITING}
