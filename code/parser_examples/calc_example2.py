from arpeggio import number


number <- r'\d*\.\d*|\d+';
factor <- ("+" / "-")? (number / "(" expression ")");
term <- factor (( "*" / "/") factor)*;
expression <- term (("+" / "-") term)*;
calc <- expression+ EOF;

parser = arpeggio.ParserPython(calc)

parse_tree = parser.parse("-(4-1)*5+(2+4.67)+5.89/(.2+7)")