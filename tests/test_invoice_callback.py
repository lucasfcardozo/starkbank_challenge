import random
import unittest
from unittest.mock import MagicMock, patch

import starkbank
from flask import Flask, request

from functions.invoice_callback.main import (invoice_callback,
                                             set_starkbank_settings,
                                             transfer_amount)

_fake_success_response = b'{"event":{"log":{"authentication":"","created":"2024-12-25T22:40:18.699528+00:00","errors":[],"id":"4984893683531776","invoice":{"nominalAmount":22590},"type":"credited"},"subscription":"invoice"}}'

class TestInvoiceCallback(unittest.TestCase):

    @patch('functions.invoice_callback.main.transfer_amount')
    def test_invoice_callback_invalid_payload(self, transfer_amount):
        transfer_amount.return_value = MagicMock()

        app = Flask(__name__)
        with app.test_request_context('/', data=b'{"invalid": "payload"}'):
            response = invoice_callback(request)
            self.assertEqual(response[1], 200)
            self.assertIn("ok", response[0])
            # how many times transfer_amount was called
            self.assertEqual(transfer_amount.call_count, 0)
        

    @patch('functions.invoice_callback.main.transfer_amount')
    def test_invoice_callback_valid_payload(self, transfer_amount):
        transfer_amount.return_value = MagicMock()

        app = Flask(__name__)
        with app.test_request_context('/', data=_fake_success_response):
            response = invoice_callback(request)
            self.assertEqual(response[1], 200)
            self.assertIn("ok", response[0])
            transfer_amount.assert_called_once()

    @patch('functions.invoice_callback.main.set_starkbank_settings')
    @patch('functions.invoice_callback.main.starkbank')
    def test_transfer_amount(self, starkbank, set_starkbank_settings):
        set_starkbank_settings.return_value = MagicMock()

        starkbank.transfer = MagicMock()
        starkbank.transfer.create = MagicMock()
        starkbank.Transfer = MagicMock()

        invoice = {
            "nominalAmount": random.randint(1, 1000)
        }

        transfer_amount(invoice)

        set_starkbank_settings.assert_called_once()
        
        args, kwargs = starkbank.Transfer.call_args
        
        self.assertIsInstance(kwargs, dict)
        self.assertEqual(kwargs["amount"], invoice["nominalAmount"])
        self.assertEqual(starkbank.transfer.create.call_count, 1)

    @patch('functions.invoice_callback.main.starkbank')
    def test_set_starkbank_settings(self, starkbank):
        starkbank.Project = MagicMock()

        set_starkbank_settings()

        starkbank.Project.assert_called_once()
        
        args, kwargs = starkbank.Project.call_args

        self.assertIsInstance(kwargs, dict)
        self.assertTrue("environment" in kwargs)
        self.assertTrue("id" in kwargs)
        self.assertTrue("private_key" in kwargs)
