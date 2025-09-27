#!/bin/bash

# local copy of mmark, debian is behind many versions
MMARK=../mmark/mmark

# debian requies this to be force install via pip3
XML2RFC=`which xml2rfc`

IDNITS=`which idnits`

for f in draft-sweetser-bcp-rpki-ca-??.md ; do

	echo "Processing ${f}"
	F_XML=`echo ${f} | sed 's/\.md/.xml/'`
	F_TXT=`echo ${f} | sed 's/\.md/.txt/'`
	${MMARK} ${f} > "${F_XML}"
	${XML2RFC} --v3 --strict --html --text "${F_XML}"

	# results will differ ...
	${IDNITS} -m submission "${F_TXT}"
	${IDNITS} -m submission "${F_XML}"

done

#
# you may be in the wrong dir, try this from the root of the repo
#
