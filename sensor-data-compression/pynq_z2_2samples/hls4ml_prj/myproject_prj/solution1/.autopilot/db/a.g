#!/bin/sh
lli=${LLVMINTERP-lli}
exec $lli \
    /app/dev/pynq_z2/hls4ml_prj/myproject_prj/solution1/.autopilot/db/a.g.bc ${1+"$@"}
