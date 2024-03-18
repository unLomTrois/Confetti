# Confetti = ComfyUI + RenPy

## Preview

https://github.com/unLomTrois/Confetti/assets/51882489/50564d5c-593f-46e5-a594-5fc93f607ffd

## What is it?

It is a Python script to connect your RenPy visual novels to Stable Diffusion via ComfyUI workflows

What is a "workflow"? It is a file with step-by-step instructions for Stable Diffusion on what image you want to generate

The idea is simple:
- You prepare workflows for ComfyUI, put them in the `game/workflows` directory
- Then in your renpy script files you call the `generate` function with the name of this workflow in a background thread
- Confetti sends this workflow to the ComfyUI server (local or global)
- ComfyUI generates image and sends it back
- Confetti stores this image in the `game/images` folder
- You show this image to a player

## You need websocket-client

This script uses websocket-client package to communicate with ComfyUI server.
So you need to pack this package in your game:

```sh
pip install --target game/python-packages websocket-client
```
## Todo

- [x] Proof of Concept
- [x] Add notifications
- [ ] Add support for batches (save multiple images from a single workflow)
- [ ] Improve the script, remove outdated methods
- [ ] Publish this package in PyPi
- [ ] Add support for LMStudio API (so it could generate text as well)
- [ ] Add a map generator

