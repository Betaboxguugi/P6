__author__ = 'Alexander Brandborg & Arash Michael Sami Kjær'
__maintainer__ = 'Mathias Claus Jensen'


class Case:
    def __init__(self, dw_rep, pred_list):
        """
        Executes predicates upon a DWRepresentation associated with a DW
        :param pred_list: list of predicates
        :param dw_rep: object representing a DW.
        OBS! connection must not be closed! Maybe include connection parameters
        in rep?
        """
        self.pred_list = pred_list
        self.dw_rep = dw_rep

    def run(self):
        # Runs all the predicates and saves the reports
        reports = []
        for p in self.pred_list:
            r = p.run(self.dw_rep)
            reports.append(r)

        # For debugging purposes, replace with some CL GUI stuff, maybe :D
        for r in reports:
            print(r)
