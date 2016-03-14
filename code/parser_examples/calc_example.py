import arpeggio


def number(): return arpeggio.RegExMatch(r'\d*\.\d*|\d+')


def factor(): return arpeggio.Optional(["+", "-"]), [number, ("(", expression, ")")]


def term(): return factor, arpeggio.ZeroOrMore(["*", "/"], factor)


def expression(): return term, arpeggio.ZeroOrMore(["+", "-"], term)


def calc(): return arpeggio.OneOrMore(expression), arpeggio.EOF

parser = arpeggio.ParserPython(calc)

parse_tree = parser.parse("-(4-1)*5+(2+4.67)+5.89/(.2+7)")



