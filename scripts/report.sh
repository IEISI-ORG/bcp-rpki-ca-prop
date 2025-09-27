#!/bin/bash

python3 rpki_error_analyzer.py | tee reports/rpki_errors_$(date +%Y%m%d).txt

#
# you may be in the wrong dir, try this from the root of the repo
#
