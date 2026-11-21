#!/bin/sh
# Month 4 logic tests. Needs only g++.  Usage:  sh run_tests.sh
cd "$(dirname "$0")" || exit 1
CODE=../../../month-04-binary-clock/code
fail=0
g++ -std=c++17 -I. -c sim_core.cpp -o /tmp/mhc_m4_core.o || exit 1
for b in 1:build-1-blink:12:00:00 2:build-2-rtc-hello:12:34:50 3:build-3-binary-clock:23:59:55; do
  n=${b%%:*}; rest=${b#*:}; d=${rest%%:*}; tm=${rest#*:}
  g++ -std=c++17 -x c++ -Dmain=sim_main -I. -Wno-unknown-pragmas -Wno-builtin-macro-redefined -U__TIME__ "-D__TIME__=\"$tm\"" -c "$CODE/$d/main.c" -o /tmp/mhc_m4_b$n.o || { echo "COMPILE FAILED: $d"; fail=1; continue; }
  g++ -std=c++17 -I. -DBUILD=$n tests4.cpp /tmp/mhc_m4_b$n.o /tmp/mhc_m4_core.o -o /tmp/mhc_m4_t$n || { fail=1; continue; }
  timeout 120 /tmp/mhc_m4_t$n || fail=1
done
exit $fail
