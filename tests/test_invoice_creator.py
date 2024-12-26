import unittest
from unittest.mock import MagicMock, patch

import starkbank
from flask import Flask, request

from functions.invoice_creator.main import (create_random_invoice,
                                            invoice_creator, random_value,
                                            set_starkbank_settings)


class TestInvoiceCreator(unittest.TestCase):

    @patch('functions.invoice_creator.main.set_starkbank_settings')
    @patch('functions.invoice_creator.main.create_random_invoice')
    @patch('functions.invoice_creator.main.starkbank.invoice.create')
    def test_invoice_creator(self, mock_create, mock_random_invoice, mock_set_settings):
        mock_random_invoice.return_value = MagicMock(spec=starkbank.Invoice)
        mock_create.return_value = [MagicMock(spec=starkbank.Invoice)]
        
        app = Flask(__name__)
        with app.test_request_context('/'):
            response = invoice_creator(request)
            self.assertEqual(response[1], 200)
            self.assertIn("invoice(s) created successfully", response[0])

    def test_create_random_invoice(self):
        invoice = create_random_invoice()
        self.assertIsInstance(invoice, starkbank.Invoice)
        self.assertTrue(hasattr(invoice, 'amount'))
        self.assertTrue(hasattr(invoice, 'tax_id'))
        self.assertTrue(hasattr(invoice, 'name'))
        self.assertTrue(hasattr(invoice, 'descriptions'))

    def test_random_value(self):
        value = random_value()
        self.assertTrue(10000 <= value <= 50000)
