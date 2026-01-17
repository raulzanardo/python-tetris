# Tiny Tetris — (Not Tiny, Just Ambitious)

Welcome to your very own microscopic Tetris. This project runs at a scale where pixels are a personality trait.

## Quick Start

- Install dependencies: you need Python and pygame.
- Run the game (example):

```bash
python3 tetris.py --pixel-size 4
```

- Want the original Atari squint-mode? Try `-p 1`.

## Controls

- Joystick D-pad / hat: left/right to move, down to soft-drop, up to rotate.
- Joysticks axis also supported (analog left/right/down).
- Keyboard: the game prints key presses for debugging; you can use a keyboard but this script currently prefers joystick input for movement.

## Features

- Boundary-checked piece movement (pieces won't escape the playfield).
- Ghost/shadow shows where the piece will land (considers locked pieces).
- Auto-restart after 5 seconds on Game Over (or press any key to restart immediately).
- Score display scaled to the tiny screen.
- Block borders so pieces actually look like blocks and not existential voids.

## Notes & Tips

- The default screen is intentionally small; increase `--pixel-size` if you want to actually see what's happening.
- If borders look off, try larger `--pixel-size` values (e.g. 4 or 8).

## Contributing

- Want keyboard movement? Submit a PR that maps arrow keys to moves.
- Want proper rotation kicks and SRS? Please bring snacks.

## License

Do whatever you want with it, but if you make an amazing tiny-arcade cabinet, invite me.

Enjoy the tiny falling-block chaos!
I vibe coded a tetris game to run on my 192x128 led matrix.
