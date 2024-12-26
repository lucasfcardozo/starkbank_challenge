import json
import os

import starkbank
from dotenv import load_dotenv
from flask import Flask, Request

load_dotenv()

_app = Flask(__name__)

@_app.route("/")
def invoice_callback(request: Request):
    print(request.data)

    data: dict = json.loads(request.data)

    if "event" in data and "subscription" in data["event"] \
        and data["event"]["subscription"] == "invoice" \
        and "log" in data["event"] \
        and "type" in data["event"]["log"] \
        and data["event"]["log"]["type"] == "credited":
        transfer_amount(data["event"]["log"]["invoice"])

    return "ok", 200


def transfer_amount(invoice):
    set_starkbank_settings()
    
    starkbank.transfer.create([
        starkbank.Transfer(
            amount=invoice["nominalAmount"],
            name="Stark Bank S.A",
            tax_id="20.018.183/0001-80",
            bank_code="20018183",
            branch_code="0001",
            account_number="6341320293482496",
            account_type="payment",
        )
    ])

def set_starkbank_settings():
    starkbank.user = starkbank.Project(
        environment="sandbox",
        id=os.getenv("STARKBANK_PROJECT_ID"),
        private_key=os.getenv("STARKBANK_PROJECT_PK"),
    )

if __name__ == "__main__":
    _app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
