VERSION=01
VERSION_PREC=$$(($(VERSION)-1))
VERSION_PREC_PRT=$(shell printf "%02d" ${VERSION_PREC} )

all:
	cd builder; python3 build_transaction_id_draft.py ${VERSION}
	LOCALE="EN_us.utf8" xml2rfc draft-quilbeuf-opsawg-configuration-tracing-${VERSION}.xml 
	rfcdiff draft-quilbeuf-opsawg-configuration-tracing-${VERSION_PREC_PRT}.txt  draft-quilbeuf-opsawg-configuration-tracing-${VERSION}.txt

