VERSION=00
VERSION_PREC=$$(($(VERSION)-1))
VERSION_PREC_PRT=$(shell printf "%02d" ${VERSION_PREC} )

all:
	cd builder; python3 build_transaction_id_draft.py ${VERSION}
	LOCALE="EN_us.utf8" xml2rfc draft-ietf-netconf-configuration-tracing-${VERSION}.xml
	rfcdiff draft-quilbeuf-netconf-configuration-tracing-${VERSION_PREC_PRT}.txt  draft-quilbeuf-netconf-configuration-tracing-${VERSION}.txt

