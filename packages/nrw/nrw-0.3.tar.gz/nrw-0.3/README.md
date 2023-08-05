# Nix Random Wallpaper

A simple program that sets random wallpaper images as desktop backgrounds in nix based operating systems / window managers. It fetches images from a local directory or Unsplash, composes a new image to match display size and arrangement, and sets the new image as the desktop background.

This project was forked from [Gnome Random Wallpaper](https://github.com/miliarch/gnome_random_wallpaper), which while great at its original limited scope, is no longer maintained.

**Example arrangement**

![Example Arrangement](example_arrangement.png)

**Example wallpaper**

![Example Wallpaper](example_wallpaper.jpg)

## Usage

Nix Random Wallpaper (`nrw`) currently makes the following assumptions about the user:
* The user will configure some external scheduler to prompt the `nrw` command to run in the background
* The user doesn't usually want to keep the generated wallpaper images forever
  * The last image that was generated is replaced by the newly generated image
  * The default output directory is `/tmp/random` - `/tmp` is commonly a tmpfs filesystem and exists only in memory (while the system remains powered on)
    * Note: The default output directory can and probably should be changed to a non-volatile location in [configuration](#configuration). Specifying a non-volatile directory will prevent temporary auto-selection of a system default wallpaper by the window manager on login after a fresh boot cycle, which can be disorienting.
* The user won't interact directly with the program often, making command line argument support unnecessary

Simply running `nrw` will fetch images from either the [Unsplash API](https://source.unsplash.com/) or the image directory (`images_dir`) defined in configuration, resize and compose the images on a spanned canvas matching your current display arrangement, save the resulting wallpaper image to the output directory (`output_dir`), and update your desktop background.

Some suggested steps to take in your environment:
* Configure a cron job or timer of some sort to run `nrw` at regular intervals (every 15 minutes works well for me - `*/15 * * * * /path/to/nrw`)
* Configure a Startup Application to run `nrw` on login

## Installation

Use the following command to install the `nrw` module from PyPi with pip:
```
pip install nrw
```

Or to install the latest version of the repository with pip:
```
pip install git+https://github.com/miliarch/nrw.git
```

After installation, a `nrw` executable link should be placed in your `$HOME/.local/bin` directory (this may vary depending on distro). If this directory is included in your PATH environment variable, the `nrw` command should be available for use without any further steps. Otherwise, you'll need to either specify the full path to run the program, or add the `$HOME/.local/bin` directory to your PATH environment variable.

Alternatively, clone this repository to your preferred installation directory and manually link `./nrw/nix_random_wallpaper.py` in the execution directory of your choice.

## Configuration

Default configuration can be found in [nrw/config.yaml](nrw/config.yaml). This file can be copied to `$HOME/.config/nix_random_wallpaper/config.yaml` and modified to override the default options.

Each configuration option in the file includes an in-line comment that details its function. If you have any questions about how existing options behave, or requests for new options, please raise an issue in this repository.

## Supported display configurations

Any number of displays that are arranged horizontally (side-by-side) within the vertical (height) bounds of the largest display should be supported.

## Unsupported display configurations

Vertical arrangements, including mixed vertical/horizontal arrangements, are currently unsupported. Support may be implemented in the future.

## Tested configurations

### Window managers

* Cinnamon 5.0.5-5.0.7
* awesome v4.3

### Wallpaper setters

* gnome (via gsettings)
* [nitrogen](https://github.com/l3ib/nitrogen) (recommended)

### Resolutions
* 1920x1080
* 2560x1440
* 3840x2160

### Display arrangements
* Dual monitor, landscape orientation, horizontal arrangement (side-by-side)
