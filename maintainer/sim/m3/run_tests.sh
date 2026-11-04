#!/bin/sh
# Month 3 logic tests. Needs only g++.  Usage:  sh run_tests.sh
cd "$(dirname "$0")" || exit 1
CODE=../../../month-03-analogue-in-out/code
fail=0
g++ -std=c++17 -I. -c sim3.cpp -o /tmp/mhc_m3_core.o || exit 1
for b in 1:build-1-adc-bar-graph 2:build-2-dac 3:build-3-loopback; do
  n=${b%%:*}; d=${b#*:}
  g++ -std=c++17 -x c++ -Dmain=sim_main -I. -Wno-unknown-pragmas -c "$CODE/$d/main.c" -o /tmp/mhc_m3_b$n.o || { echo "COMPILE FAILED: $d"; fail=1; continue; }
  g++ -std=c++17 -I. -DBUILD=$n tests3.cpp /tmp/mhc_m3_b$n.o /tmp/mhc_m3_core.o -o /tmp/mhc_m3_t$n || { fail=1; continue; }
  timeout 120 /tmp/mhc_m3_t$n || fail=1
done
exit $fail
