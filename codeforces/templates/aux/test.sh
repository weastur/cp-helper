#!/usr/bin/env bash

set -e

is_python=false

while getopts ":p" opt; do
  case "${opt}" in
    p)
      is_python=true
      ;;
    \?)
      echo "Invalid option: -${OPTARG}" >&2
      ;;
  esac
done

if ! $is_python ; then
    gcc -static -fno-asm -lm -s -std=c11 -m32 -Wall -Wextra -Wpedantic -O2 ./*.c
    RUN_CMD="$(command -v time) -o time.out -f '(%es)' ./a.out"
else
    RUN_CMD="$(command -v time) -o time.out -f '(%es)' python3 ./*.py"
fi

test_count="$(find . -type f -name '*.in' | wc -l)"
for test_case in $(seq "${test_count}")
do
    input_testcase="${test_case}.in"
    output_testcase="${test_case}.in"
    my_output="${test_case}_my.out"
    if ! bash -c "${RUN_CMD}" < "${input_testcase}" > "${my_output}"; then
        echo "[1m[31mSample test #${test_case}: Runtime Error[0m $(cat time.out)"
        echo "========================================"
        echo "Sample Input \#${test_case}"
        cat "${input_testcase}"
    else
        if diff --brief --ignore-space-change "${my_output}" "${output_testcase}"; then
            echo "[1m[32mSample test #${test_case}: Accepted[0m $(cat time.out)"
        else
            echo "[1m[31mSample test #${test_case}: Wrong Answer[0m $(cat time.out)"
            echo "========================================"
            echo "Sample Input #${test_case}"
            cat "${input_testcase}"
            echo "========================================"
            echo "Sample Output #${test_case}"
            cat "${output_testcase}"
            echo "========================================"
            echo "My Output #${test_case}"
            cat "${my_output}"
            echo -e "\n========================================"
        fi
    fi
done
