#!/bin/sh
# Serialise heavy jobs across parallel reel builds (mattes, snapshots, checks,
# renders, whisper): sh work/b1021/heavy.sh <command...>. The cloud container
# has 4 cores; two heavy jobs at once only make both slower.
exec flock /tmp/reels-heavy.lock "$@"
