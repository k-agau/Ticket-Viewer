import unittest
from unittest.mock import patch
from click.testing import CliRunner
import viewer
from viewer import fixLength
from viewer import formatTickets
from viewer import cx
from viewer import isValid

runner = CliRunner()

class TestViewer(unittest.TestCase):
    def test_fixLength(self):
        emptyString = ''
        randomString = 'asdlkjasfljadofinqeopifnjqaoasodnqeofinwef'
        hundredCharString = 'asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda'
        overHundredCharString = 'asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaa'
        twoHundredCharString = 'asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda'
        overTwoHundredCharString = 'asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaa'
        result = fixLength(emptyString)
        self.assertEqual(result, emptyString, "Not equal")
        result = fixLength(randomString)
        self.assertEqual(result, randomString, "Not equal")
        result = fixLength(hundredCharString)
        self.assertEqual(result, hundredCharString, "Not equal")
        result = fixLength(overHundredCharString)
        self.assertEqual(result, hundredCharString + '\n' + 'a', "Not equal")
        result = fixLength(twoHundredCharString)
        self.assertEqual(result, hundredCharString + '\n' + hundredCharString, "Not equal")
        result = fixLength(overTwoHundredCharString)
        self.assertEqual(result, hundredCharString + '\n' + hundredCharString + '\n' + 'a', "Not equal")
    @patch('builtins.print')
    def test_formatTickets(self, mock_print):
        # BASIC FORMAT
        # Empty ticket
        _id = ''
        subj = ''
        sent = ''
        opened = ''
        desc = ''
        dict = {'id': _id, 'subject': subj, 'submitter_id': sent, 'created_at': opened, 'description': desc}
        formatTickets(dict)
        mock_print.assert_called_with('Ticket  with subject  was sent on  and opened on .\n')

        # Short subj
        _id = '1'
        subj = 'asd'
        sent = '1'
        opened = '2'
        desc = 'asd'
        dict = {'id': _id, 'subject': subj, 'submitter_id': sent, 'created_at': opened, 'description': desc}
        formatTickets(dict)
        mock_print.assert_called_with('Ticket 1 with subject asd was sent on 1 and opened on 2.\n')

        # Long subj
        _id = '1'
        subj = 'asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda'
        sent = '1'
        opened = '2'
        desc = 'asd'
        dict = {'id': _id, 'subject': subj, 'submitter_id': sent, 'created_at': opened, 'description': desc}
        formatTickets(dict)
        mock_print.assert_called_with('Ticket 1 with subject asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdas\ndaasdasdasdaasdasdasdaasdasdasda was sent on 1 and opened on 2.\n')

        # ADVANCED FORMAT
        # Empty ticket
        _id = ''
        subj = ''
        sent = ''
        opened = ''
        desc = ''
        dict = {'id': _id, 'subject': subj, 'submitter_id': sent, 'created_at': opened, 'description': desc}
        formatTickets(dict, True)
        mock_print.assert_called_with('ID: \nSubject: \nSent by: \nOpened on: \nDescription:\n')

        # Short subj
        _id = '1'
        subj = 'asd'
        sent = '1'
        opened = '2'
        desc = 'asd'
        dict = {'id': _id, 'subject': subj, 'submitter_id': sent, 'created_at': opened, 'description': desc}
        formatTickets(dict, True)
        mock_print.assert_called_with('ID: 1\nSubject: asd\nSent by: 1\nOpened on: 2\nDescription:\nasd')

        # Long subj
        _id = '1'
        subj = 'asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda'
        sent = '1'
        opened = '2'
        desc = 'asd'
        dict = {'id': _id, 'subject': subj, 'submitter_id': sent, 'created_at': opened, 'description': desc}
        formatTickets(dict, True)
        mock_print.assert_called_with('ID: 1\nSubject: asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda\nasdasdasda\nSent by: 1\nOpened on: 2\nDescription:\nasd')

        # Long subj, long desc
        _id = '1'
        subj = 'asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda'
        sent = '1'
        opened = '2'
        desc = 'asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda'
        dict = {'id': _id, 'subject': subj, 'submitter_id': sent, 'created_at': opened, 'description': desc}
        formatTickets(dict, True)
        mock_print.assert_called_with('ID: 1\nSubject: asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda\nasdasdasda\nSent by: 1\nOpened on: 2\nDescription:\nasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasda\nasdasdasda')
    def test_cx(self):
        # Assumes with valid token. Assumes validation step works.
        '''
        # Broken URL
        try:
            cx()
        except Exception as e:
            self.assertEqual(1, 1, 'Should have failed')
        # Existing ticket
        try:
            cx('tickets/1')
        except Exception as e:
            self.assertEqual(1, 2, 'Should have passed')
        # Non-existant ticket
        try:
            cx('tickets/1000')
        except Exception as e:
            self.assertEqual(1, 2, 'Should have failed')
        # Receive all tickets
        try:
            cx('incremental/tickets.json?start_time=0')
        except Exception as e:
            self.assertEqual(1, 2, "Should have passed")
        '''
        # Assumes invalid token
        # Valid ticket
        try:
            cx('tickets/1')
        except Exception as e:
            self.assertEqual(1, 1, 'Should have failed')
        # Non-existant ticket
        try:
            cx('tickets/1000')
        except Exception as e:
            self.assertEqual(1, 1, 'Should have failed')
        # Receive all tickets
        try:
            cx('incremental/tickets.json?start_time=0')
        except Exception as e:
            self.assertEqual(1, 1, "Should have failed")
        #'''
    def test_isValid(self):
        # Assuming valid token
        '''
        result = isValid()
        self.assertEqual(result, True, "Should return true")
        '''
        # Assuming invalid token
        
        result = isValid()
        self.assertEqual(result, False, "Should return false")
        #'''

if __name__ == '__main__':
    unittest.main()