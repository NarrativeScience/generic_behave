#!/bin/bash

    artifact_prefix="$1"
    tempdir=$(mktemp -d)
    dir=$(pwd)

    unzip -qq "dist/${artifact_prefix}.pex" -d ${tempdir}
    exit_code=$?
    if [ "${exit_code}" -gt 2 ] ; then
        ECHO "Failed to unzip pex file"
        return ${exit_code}
    fi
    strip_bin=strip
    [ "$(uname)" = 'Darwin' ] && strip_bin=gstrip

    (cd "${tempdir}" &&
        find .deps -name '*.so'| grep -v psycopg2 | xargs ${strip_bin} ;  # Shrink dependency size by stripping them first
        zip -rqq "${dir}/dist/${artifact_prefix}.pex.rezip" .) &&
        mv "dist/${artifact_prefix}.pex.rezip" "dist/${artifact_prefix}.pex" &&
        rm -rf "${tempdir}"
        ECHO "Rezipped ${artifact_prefix}"