all:
	cd builder; python3 build_transaction_id_draft.py
	LOCALE="EN_us.utf8" xml2rfc --v2 $(shell ls draft-quilbeuf-opsawg-configuration-tracing-??.xml | sort | tail -n 1)

