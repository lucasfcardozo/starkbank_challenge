import datetime
import os
import random

import starkbank
from dotenv import load_dotenv
from faker import Faker
from flask import Flask, Request

_faker = Faker('pt_BR')
# _faker.add_provider(ssn)

load_dotenv()

_app = Flask(__name__)


@_app.route("/", methods=["GET"])
def invoice_creator(request: Request):
    set_starkbank_settings()

    num_invoices = random.randint(8, 12)

    invoices: List[starkbank.Invoice] = []

    for i in range(1, num_invoices):
        try:
            invoices.append(create_random_invoice())
        except Exception as e:
            return str(e), 500

    created = starkbank.invoice.create(invoices)
    
    return "{num} invoice(s) created successfully".format(num=num_invoices), 200

def create_random_invoice() -> starkbank.Invoice:
    return starkbank.Invoice(
        amount=random_value(),
        # due=datetime.datetime.now() + datetime.timedelta(minutes=2),
        tax_id=_faker.cpf(),
        name=_faker.name(),
        descriptions=[
            {
                "key": "challenger",
                "value": "lucas"
            }
        ]
    )

def set_starkbank_settings():
    starkbank.user = starkbank.Project(
        environment="sandbox",
        id=os.getenv("STARKBANK_PROJECT_ID"),
        private_key=os.getenv("STARKBANK_PROJECT_PK"),
    )

def random_value():
    return random.randint(10000, 50000)

if __name__ == "__main__":
    _app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
