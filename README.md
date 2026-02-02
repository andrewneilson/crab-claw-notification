# Crab claw notification

This generates a `.wav` file that sounds like a satisfying pair of claw snaps. It's meant to get your attention when a coding agent like Claude Code is done a task or waiting for input.

## Instructions

1. Generate the sound

```bash
python generate_sound.py
```

2. Add the absolute path to the `.wav` file to `notification.sh`

3. Add `notification.sh` as a hook in your coding agent. With Claude Code the default location is `~/.claude/hooks/`

## More info

* I'm currently using this with Ghostty on MacOS 15.6.1
* Also see [`CLAUDE.md`](CLAUDE.md)
