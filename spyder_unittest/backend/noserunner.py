# -*- coding: utf-8 -*-
#
# Copyright © 2013 Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
"""Support for Nose framework."""

# Third party imports
from lxml import etree
from spyder.config.base import get_translation

# Local imports
from spyder_unittest.backend.runnerbase import Category, RunnerBase, TestResult

try:
    _ = get_translation('spyder_unittest')
except KeyError:
    import gettext
    _ = gettext.gettext


class NoseRunner(RunnerBase):
    """Class for running tests within Nose framework."""

    module = 'nose'
    name = 'nose'

    def create_argument_list(self, config, cov_path):
        """Create argument list for testing process."""
        return [
            '-m',
            self.module,
            '--with-xunit',
            f'--xunit-file={self.resultfilename}',
        ]

    def finished(self):
        """Called when the unit test process has finished."""
        output = self.read_all_process_output()
        testresults = self.load_data()
        self.sig_finished.emit(testresults, output, True)

    def load_data(self):
        """
        Read and parse unit test results.

        This function reads the unit test results from the file with name
        `self.resultfilename` and parses them. The file should contain the
        test results in JUnitXML format.

        Returns
        -------
        list of TestResult
            Unit test results.
        """
        try:
            data = etree.parse(self.resultfilename).getroot()
        except OSError:
            data = []

        testresults = []
        for testcase in data:
            category = Category.OK
            status = 'ok'
            name = f"{testcase.get('classname')}.{testcase.get('name')}"
            message = ''
            time = float(testcase.get('time'))
            extras = []

            for child in testcase:
                if child.tag in ('error', 'failure', 'skipped'):
                    category = Category.SKIP if child.tag == 'skipped' else Category.FAIL
                    status = child.tag
                    type_ = child.get('type')
                    message = child.get('message', default='')
                    if type_:
                        message = '{0}: {1}'.format(type_, message) if message else type_
                    if child.text:
                        extras.append(child.text)
                elif child.tag in ('system-out', 'system-err'):
                    if child.tag == 'system-out':
                        heading = _('Captured stdout')
                    else:
                        heading = _('Captured stderr')
                    contents = child.text.rstrip('\n')
                    extras.append(f'----- {heading} -----\n{contents}')

            extra_text = '\n\n'.join(extras)
            testresults.append(
                TestResult(category, status, name, message, time, extra_text))

        return testresults
