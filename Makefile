PROJECT_ID := $(shell gcloud config get-value project)

invoice-creator-deploy:
	gcloud functions deploy invoice_creator \
		--runtime python39 \
		--source ./functions/invoice_creator \
        --trigger-http \
		--allow-unauthenticated

invoice-creator-set-schedule:
	gcloud scheduler jobs create http invoice_creator \
		--uri=https://us-central1-$(PROJECT_ID).cloudfunctions.net/invoice_creator \
		--schedule="0 */3 26 12 *" \
		--location=us-central1

invoice-callback-deploy:
	gcloud functions deploy invoice_callback \
		--runtime python39 \
		--source ./functions/invoice_callback \
        --trigger-http \
		--allow-unauthenticated

pytests:
	pytest tests --cov=functions --cov-report=xml
