#!/bin/sh
# Month 1 logic tests. Needs only g++.  Usage:  sh run_tests.sh
cd "$(dirname "$0")" || exit 1
CODE=../../../month-01-electronic-dice/code
fail=0
g++ -std=c++17 -I. -c sim1.cpp -o /tmp/mhc_m1_core.o || exit 1
for b in 1:build-1-blink 2:build-2-button 3:build-3-dice; do
  n=${b%%:*}; d=${b#*:}
  g++ -std=c++17 -x c++ -Dmain=sim_main -I. -Wno-unknown-pragmas -c "$CODE/$d/main.c" -o /tmp/mhc_m1_b$n.o || { echo "COMPILE FAILED: $d"; fail=1; continue; }
  g++ -std=c++17 -I. -DBUILD=$n tests1.cpp /tmp/mhc_m1_b$n.o /tmp/mhc_m1_core.o -o /tmp/mhc_m1_t$n || { fail=1; continue; }
  timeout 60 /tmp/mhc_m1_t$n || fail=1
done
exit $fail
