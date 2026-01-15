#!/usr/bin/env python3
"""Generate a crab claw snap notification sound."""

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SAMPLE_RATE = 44100
DURATION_MS = 500

def make_single_snap(num_samples, offset_samples=0, seed=42):
    """Create a shell snap - moderate stretch for smoother sound."""
    snap_duration = int(SAMPLE_RATE * 0.073)  # 73ms (10% longer again)
    t_snap = np.linspace(0, 0.073, snap_duration)

    np.random.seed(seed)

    # Two clicks slightly offset - 1.5x stretch

    # Click 1: The initial contact - warmer, mid-focused
    click1_len = int(SAMPLE_RATE * 0.0045)  # 4.5ms (was 3ms)
    click1 = np.zeros(snap_duration)
    raw1 = np.random.randn(click1_len)
    b1, a1 = butter(2, [800 / (SAMPLE_RATE / 2), 2200 / (SAMPLE_RATE / 2)], btype='band')
    click1[:click1_len] = lfilter(b1, a1, raw1) * np.exp(-np.linspace(0, 1, click1_len) * 4)

    # Click 2: The "shell closure" - slightly delayed, warm mids
    click2_start = int(SAMPLE_RATE * 0.006)  # 6ms delay (was 4ms)
    click2_len = int(SAMPLE_RATE * 0.009)  # 9ms (was 6ms)
    click2 = np.zeros(snap_duration)
    raw2 = np.random.randn(click2_len)
    b2, a2 = butter(2, [600 / (SAMPLE_RATE / 2), 1800 / (SAMPLE_RATE / 2)], btype='band')
    filtered2 = lfilter(b2, a2, raw2) * np.exp(-np.linspace(0, 1, click2_len) * 3)
    click2[click2_start:click2_start + click2_len] = filtered2

    # Body resonance - mid focused
    body = np.random.randn(snap_duration)
    b_body, a_body = butter(2, [800 / (SAMPLE_RATE / 2), 1600 / (SAMPLE_RATE / 2)], btype='band')
    body = lfilter(b_body, a_body, body)
    body *= np.exp(-t_snap * 90)  # Moderate decay

    # Hollow resonance - tuned sine with quick ring-out (like tapping a hollow bone)
    hollow_len = int(SAMPLE_RATE * 0.025)  # 25ms ring
    hollow = np.zeros(snap_duration)
    t_hollow = np.linspace(0, 0.025, hollow_len)
    # Primary hollow tone with slight detuned overtone for organic quality
    hollow_wave = np.sin(2 * np.pi * 1200 * t_hollow) * 0.7
    hollow_wave += np.sin(2 * np.pi * 1850 * t_hollow) * 0.3  # slight overtone
    hollow_wave *= np.exp(-t_hollow * 180)  # quick decay but with ring
    hollow[click2_start:click2_start + hollow_len] = hollow_wave[:hollow_len]

    # Crunch - subtle fibrous texture
    crunch = np.zeros(snap_duration)
    np.random.seed(seed + 100)
    # Just a few soft crackles
    burst_times = [1, 5, 10]  # fewer, simpler
    for t_ms in burst_times:
        burst_start = int(t_ms * SAMPLE_RATE / 1000)
        burst_len = int(SAMPLE_RATE * 0.003)  # 3ms bursts
        if burst_start + burst_len < snap_duration:
            burst = np.random.randn(burst_len)
            # Lower frequency, softer crunch
            b_crunch, a_crunch = butter(2, [800 / (SAMPLE_RATE / 2), 2500 / (SAMPLE_RATE / 2)], btype='band')
            burst = lfilter(b_crunch, a_crunch, burst)
            burst *= np.exp(-np.linspace(0, 1, burst_len) * 5)
            crunch[burst_start:burst_start + burst_len] += burst

    # Very subtle low-end warmth - much quieter
    thump_len = click2_len
    thump = np.zeros(snap_duration)
    thump_wave = np.sin(2 * np.pi * 250 * np.linspace(0, thump_len/SAMPLE_RATE, thump_len))
    thump_wave *= np.exp(-np.linspace(0, 1, thump_len) * 6)
    thump[click2_start:click2_start + thump_len] = thump_wave

    # Mix - subtle crunch
    snap = 0.40 * click1 + 0.40 * click2 + 0.05 * body + 0.07 * hollow + 0.06 * crunch + 0.02 * thump

    # Place in full array at offset
    result = np.zeros(num_samples)
    end_idx = min(offset_samples + snap_duration, num_samples)
    actual_len = end_idx - offset_samples
    result[offset_samples:end_idx] = snap[:actual_len]

    return result

def add_subtle_echo(sound, delay_ms=30, decay=0.08):
    """Add a very subtle echo/reverb."""
    delay_samples = int(SAMPLE_RATE * delay_ms / 1000)
    echo = np.zeros(len(sound))
    echo[delay_samples:] = sound[:-delay_samples] * decay
    return sound + echo


def generate_crab_snap():
    """Generate two shell-like snaps like a crab claw."""
    num_samples = int(SAMPLE_RATE * DURATION_MS / 1000)

    # First snap at the start
    snap1 = make_single_snap(num_samples, offset_samples=0, seed=42)

    # Second snap ~260ms later
    gap_ms = 260
    snap2_offset = int(SAMPLE_RATE * gap_ms / 1000)
    snap2 = make_single_snap(num_samples, offset_samples=snap2_offset, seed=99)

    # Second snap slightly quieter
    sound = snap1 + 0.85 * snap2

    # Add subtle echo
    sound = add_subtle_echo(sound, delay_ms=30, decay=0.08)

    # Normalize to full volume
    sound = sound / np.max(np.abs(sound)) * 0.95

    return (sound * 32767).astype(np.int16)

if __name__ == "__main__":
    sound = generate_crab_snap()
    output_path = "/Users/andrewneilson/claude-notification/crab-snap.wav"
    wavfile.write(output_path, SAMPLE_RATE, sound)
    print(f"Generated: {output_path}")
    print(f"Duration: {DURATION_MS}ms, Sample rate: {SAMPLE_RATE}Hz")
