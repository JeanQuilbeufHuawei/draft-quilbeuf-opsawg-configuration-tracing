# Configuration tracing draft

## Requirements

 * python3 and pakages listed in [requirements.txt](requirements.txt) `pip install -r requirements.txt` to install
 * xml2rfc
 * make

## Modify the draft

### Change in the text

Modify [builder/draft-quilbeuf-opsawg-configuration-tracing.xml](builder/draft-quilbeuf-opsawg-configuration-tracing.xml).
Run `make` to update the .xml and .txt versions in the main folder.

### Change in the YANG

Modify the YANG module in [yang](yang) folder. Run `make` to update the .xml and .txt versions in the main folder.


