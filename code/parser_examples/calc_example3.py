from arpeggio.peg import QUESTION, expression

number = r'\d*\.\d*|\d+'    # this is a comment
factor = ("+" / "-")QUESTION(number / "(" expression ")")
term = factor (( "*" / "/") factor)*
expression = term (("+" / "-") term)*
calc = expression + arpeggio.EOF