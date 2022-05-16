all:
	cd builder; python3 build_transaction_id_draft.py
	LOCALE="EN_us.utf8" xml2rfc --v2 $(shell ls draft-claise-opsawg-external-transaction-id-??.xml | sort | tail -n 1)

