# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a Python script that generates a synthesized "crab claw snap" notification sound. It uses numpy and scipy to create a two-part clicking sound with hollow resonance, subtle crunch textures, and echo effects.

## Commands

Generate the sound file:
```bash
python3 generate_sound.py
```

Play the generated sound (macOS):
```bash
afplay crab-snap.wav
```

## Dependencies

- numpy
- scipy (specifically scipy.io.wavfile and scipy.signal)

## Architecture

The sound is built from layered components in `generate_sound.py`:
- Two bandpass-filtered noise bursts (initial contact + shell closure)
- Hollow resonance using detuned sine waves
- Subtle crunch texture from random bursts
- Low-frequency warmth component
- Final echo/reverb pass

The `make_single_snap()` function creates one snap; `generate_crab_snap()` combines two snaps ~260ms apart with the second slightly quieter.
