__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'

from .reinterpreter.reinterpreter_mock import ReinterpreterMock as Reinterpreter


class Case:
    """
    FrameworkTestCase for running predicate tests on a pygrametl program given a set of sources
    """

    def __init__(self, program, mapping, pred_list, program_is_path):
        """
        :param program: A path or string of a pygrametl program
        :param mapping: A map of sources
        :param pred_list: A list of predicates we wish to run
        """
        self.program = program
        self.mapping = mapping
        self.pred_list = pred_list
        self.program_is_path = program_is_path

        # Sets up and runs reinterpreter getting DWRepresentation object
        tc = Reinterpreter()
        # Reinterpreter(program=self.program, conn_scope=self.mapping, program_is_path = self.program_is_path)
        self.dw_rep = tc.run()

        # Runs all predicates and reports their results
        for p in self.pred_list:
            p.run(self.dw_rep)
            report = p.report()
            report.run()






class Report(object):
    def __init__(self, name_of_predicate='', result=False, message_if_true='', message_if_false='',
                 list_of_wrong_elements=None):
        """
        :param name_of_predicate: name of the the predicate class used, for the lazy just use: self.__class__.__name__
        :type name_of_predicate: str
        :param result: final result of the test
        :type result: bool
        :param message_if_true: message which will be printed if results are True
        :type message_if_false: str
        :param message_if_false: message which will be printed if results are False
        :type message_if_false: str
        :param list_of_wrong_elements: list of all the elements in which the predicate returned false
        """
        self.nop = name_of_predicate
        self.r = result
        self.mit = message_if_true
        self.mif = message_if_false
        self.l = list_of_wrong_elements

    def run(self):
        """
        Checks if results are true or false, prints the predicate used, result, message which is different dependent on
        results and if result is false, also prints a list of the elements which returned false if any are provided.
        In the cause that result is somehow neither, a failed message will show.
        """
        if self.r is True:
            print('{} returned {} {}'.format(self.nop, self.r, self.mit))
        elif self.r is False:
            if self.l is not None:
                print('{} returned {} at the following elements {} {} '.format(self.nop, self.r, self.l, self.mif))
            else:
                print('{} returned {} {} '.format(self.nop, self.r, self.mif))
        else:
            # TODO: Make/get a mail people can report errors to
            print('Failure to report, please contact us at errorReport@pyrgrametl.dk if you see this message')


