# fak-config

FAK user configuration repository.

## Features

- QMK-like folder structure with `keyboards` and `keymaps`
- All-in-one `fak` command for flashing, compiling, etc.
- The latest release is automatically updated every push with ready-to-flash firmware for all your keyboards and keymaps
- Ready-to-use dev container for easy remote development via GitHub Codespaces or VS Code
- Globally shared Nickel files in `shared/lib` for code reuse across keyboards and keymaps

## Setup

### GitHub Codespace

The quickest and easiest way to get started is using [GitHub Codespaces](https://github.com/features/codespaces). You don't have to go through the trouble of setting up the development environment. Everything is remote, comes preloaded, and it just works.

1. Fork this repo
1. Create a new codespace
1. Wait for the environment to be loaded in the terminal until you can enter commands

The only thing that won't work from a remote setup is, of course, flashing. You'll have to do that locally with [`wchisp`](https://github.com/ch32-rs/wchisp/releases/tag/nightly). Thankfully, `wchisp` provides prebuilt binaries so getting that set up on your local machine is very easy.

1. In your codespace, `fak compile -kb [keyboard] -km [keymap]`. It will print the path(s) where it put the firmware.
1. Download the `.ihx` file(s) located in the printed path(s).
1. In your local machine, `wchisp flash [keyboard].[keymap].central.ihx`.
1. And then if you have a split, `wchisp flash [keyboard].[keymap].peripheral.ihx`.

Alternatively, you can push your changes, wait a bit, then you will find all ready-to-flash `.ihx` files in the latest release. From there, download the ones you need, then flash with `wchisp`.

If, for whatever reason, you're getting `fak: command not found`, enter `nix develop` then you should be back up.

### Nix

If you have Nix installed on your system, a Nix flake is provided. There are two dev shells: `default` and `full`. The only difference between the two is that `full` comes with `wchisp`, the flashing utility, so you will most likely want to use `full`. `default` dev shell is what the dev container uses, because it's impossible to flash remotely and it wouldn't make sense to have `wchisp` there.

1. Fork and clone this repo
1. `nix develop .#full` or `nix develop`

### Manual setup

Requirements:
- [`sdcc` 4.2.0](https://sourceforge.net/projects/sdcc/files)
- [`nickel` 1.5.0](https://github.com/tweag/nickel/releases/tag/1.5.0)
- [`python` 3.11.6](https://www.python.org/downloads)
- [`meson` 1.2.3](https://mesonbuild.com/)
- [`ninja` 1.11.1](https://github.com/ninja-build/ninja/releases/tag/v1.11.1)
- [`wchisp`](https://github.com/ch32-rs/wchisp/releases/tag/nightly)

With manual setup, the `fak` command isn't included. Use `python fak.py` in place of `fak` (e.g., `fak clean` becomes `python fak.py clean`). Alternatively, you may make a shell alias for `fak` if you wish.

## Commands

Now that you have your development environment set up and ready, compiling is as easy as `fak compile -kb [keyboard] -km [keymap]`. You may omit `-km [keymap]` if keymap is "default" (e.g., `fak compile -km [keyboard]`). This will also print the path(s) where it put the firmware files in, which is helpful in a remote setup.

If you're using a local setup, you can flash directly with `fak flash -kb [keyboard] -km [keymap]`. Then if you have a split, flash the peripheral side with `fak flash_p -kb [keyboard] -km [keymap]`. Likewise, you may omit `-km [keymap]` if keymap is "default".

If something's off, wrong, or not working, cleaning your build files might help with `fak clean`.

To compile every keyboard with its every keymap, enter `fak compile_all`. Whenever you push, this is what GitHub Actions actually does behind the scenes to update the latest release with all ready-to-flash `.ihx` files.

## Included Nickel paths

All Nickel files are evaluated with two include paths:
- `ncl` directory in [`fak`](https://github.com/semickolon/fak). This makes `import "fak/somefile.ncl"` possible.
- `shared` directory in this repo. This makes `import "lib/somefile.ncl"` possible.

We do this so you don't have to do something like `import ../../../subprojects/fak/ncl/fak/somefile.ncl`. Yeah. Horrible.

## Migrating from FAK forks

If you're one of the OGs who use FAK before user config repos existed and you want to migrate:

1. Fork and clone this repo.
1. Copy over your keyboards and keymaps in `keyboards` while respecting the file structure.
1. Replace all those (horrible) relative `fak` imports with `import "fak/somefile.ncl"`.

## Switching versions

1. (Optional) To use a different FAK repo, like your own fork, change the `url` in `subprojects/fak.wrap`.
1. To use a different version, change the `revision` in `subprojects/fak.wrap`. This can be a commit hash (recommended) or a tag.
1. `fak update`.

⚠️ This affects all your keyboards and keymaps, so if there's a breaking change in the version and/or repo you're switching to, you'll have to fix that in **all** your Nickel files.
