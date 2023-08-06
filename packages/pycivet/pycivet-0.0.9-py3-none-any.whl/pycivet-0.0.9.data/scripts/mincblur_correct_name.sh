#!/bin/bash -e
# Wrapper for mincblur, but saves the output file to the given
# file name instead of {}_blur.mnc

blurred="$(mktemp)"
mincblur "${@:1:$#-1}" "$blurred"
mv $blurred* "${@: -1}"
