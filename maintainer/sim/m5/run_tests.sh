#!/bin/sh
# Month 5 logic tests. Needs only g++.  Usage:  sh run_tests.sh
cd "$(dirname "$0")" || exit 1
CODE=../../../month-05-sixteen-bit-and-memory/code
fail=0
g++ -std=c++17 -I. -c sim_core.cpp -o /tmp/mhc_m5_core.o || exit 1
for b in 1:build-1-blink 2:build-2-eeprom-hello 3:build-3-boot-counter; do
  n=${b%%:*}; d=${b#*:}
  g++ -std=c++17 -x c++ -Dmain=sim_main -I. -Wno-unknown-pragmas -c "$CODE/$d/main.c" -o /tmp/mhc_m5_b$n.o || { echo "COMPILE FAILED: $d"; fail=1; continue; }
  g++ -std=c++17 -I. -DBUILD=$n tests5.cpp /tmp/mhc_m5_b$n.o /tmp/mhc_m5_core.o -o /tmp/mhc_m5_t$n || { fail=1; continue; }
  timeout 120 /tmp/mhc_m5_t$n || fail=1
done
exit $fail
