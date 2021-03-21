#!/usr/bin/env bash

# Example:
# (Prerequisite: Clone fastapi repository under the var directory.)
# ./check_hl_lines.sh ../var/fastapi/docs/ja/docs/tutorial

set -eu

script_base=$(cd $(dirname $0); pwd -P)
translation_base=$(cd $1; pwd -P)

for file in $(find ${translation_base} -type f)
do
  echo "Process ${file} ..."
  python ${script_base}/highlight_sync_checker.py ${file}
done
