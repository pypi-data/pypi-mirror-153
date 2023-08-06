#!/bin/bash

CURRENT_VERSION=`git describe --tags --match v* --exact-match`
ERROR_STR="CHANGELOG has not been updated for ${CURRENT_VERSION}\\nSee the README for instructions"
ERROR_PAD="***********"

head -n 1 CHANGELOG.rst | grep -q $CURRENT_VERSION - || {
  echo -e "\\n${ERROR_PAD}"
  echo -e $ERROR_STR;
  echo -e "${ERROR_PAD}"
  exit 1; }
