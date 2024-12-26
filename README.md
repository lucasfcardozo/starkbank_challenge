# StarkBank Challenge

This is a project developed for the StarkBank Challenge. The project consists of a webhook system that receives callbacks and processes the requests. In this case, invoices are generated automatically and the values are transferred to a specific account, deducting the applicable fees.


## Deploy

Consider that you already has a google cloud project, run the following command to deploy the application:

```bash
make invoice-creator-deploy
make invoice-callback-deploy
```

Remember to create a scheduler to run the invoice-creator function every 3 hours.
```bash
make invoice-creator-set-schedule
```

## ENVs

You must create a .env file for each function with the following variables:

```
STARKBANK_API_KEY=your_starkbank_api_key
STARKBANK_API_SECRET=your_starkbank_api_secret
```

# Tests

To run the tests, you must run the following command:

```bash
make pytests
```