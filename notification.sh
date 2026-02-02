#!/bin/bash

# Play the crab snap sound in background
afplay <PATH TO .WAV FILE> &

# Show desktop notification (must complete before script exits)
osascript -e 'display notification "Claude is waiting for your input" with title "Claude Code"'
