#!/bin/sh
# Month 2 logic tests. Needs only g++.  Usage:  sh run_tests.sh
cd "$(dirname "$0")" || exit 1
CODE=../../../month-02-workshop-command-centre/code
fail=0
for b in 1:build-1-blink 2:build-2-hello-expander 3:build-3-led-chase 4:build-4-command-centre; do
  n=${b%%:*}; d=${b#*:}
  g++ -std=c++17 -x c++ -Dmain=sim_main -I. -Wno-unknown-pragmas -Wno-write-strings -c "$CODE/$d/main.c" -o /tmp/mhc_m2_b$n.o || { echo "COMPILE FAILED: $d"; fail=1; continue; }
  g++ -std=c++17 -I. -c sim_core.cpp -o /tmp/mhc_m2_core.o || fail=1
  g++ -std=c++17 -I. test_b$n.cpp /tmp/mhc_m2_b$n.o /tmp/mhc_m2_core.o -o /tmp/mhc_m2_test$n || { fail=1; continue; }
  /tmp/mhc_m2_test$n || fail=1
done
exit $fail
