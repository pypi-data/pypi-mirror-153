#!/usr/bin/env python3
import yaml
from datetime import datetime
from io import BytesIO
from os import environ
from pathlib import Path
from PIL import Image
from random import choice
from requests import get
from shutil import move
from subprocess import run
from sys import exit
from time import sleep

# Path configuration
BASE_DIR = Path(__file__).resolve().parents[0]
USER_HOME_PATH = Path.home()
CONFIG_DIR = Path(f"{USER_HOME_PATH}/.config/nix_random_wallpaper")
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = Path(f'{CONFIG_DIR}/config.yaml')


class Display:
    def __init__(self, resolution, offset_w, offset_h):
        self.resolution_w, self.resolution_h = map(int, resolution.split('x'))
        self.offset_w = int(offset_w)
        self.offset_h = int(offset_h)


def calculate_canvas_dimensions(displays):
    """Calculate canvas dimensions from given Display objects

    Assume a horizontal layout - sum width, largest height (this can be improved)
    """
    total_width = sum([d.resolution_w for d in displays])
    total_height = max(displays, key=lambda x: x.resolution_h).resolution_h
    return total_width, total_height


def calculate_crop_box(display, image):
    """Calculate crop box for given image based on display dimensions"""
    top_left = 0
    top_right = 0
    bottom_right = display.resolution_w
    bottom_lower = display.resolution_h

    if display.resolution_w < image.width:
        excess = image.width - display.resolution_w
        top_left = int(excess / 2)
        bottom_right = display.resolution_w + (int(excess / 2) + excess % 2)

    if display.resolution_h < image.height:
        excess = image.height - display.resolution_h
        top_right = int(excess / 2)
        bottom_lower = display.resolution_h + (int(excess / 2) + excess % 2)

    return (top_left, top_right, bottom_right, bottom_lower)


def calculate_proportional_dimensions(display, image):
    """Calculate proportional dimensions for given image based on display
    dimensions
    """
    adjusted_width = int(display.resolution_h * image.width / image.height)
    adjusted_height = int(display.resolution_w * image.height / image.width)

    if adjusted_height < display.resolution_h:
        # Return size based on display height - adjusted image width is
        # too small to fill display
        return (adjusted_width, display.resolution_h)
    # Return size based on display width in the common case
    return (display.resolution_w, adjusted_height)


def compose_images(displays, images):
    """Compose images on canvas that spans displays"""
    total_width, total_height = calculate_canvas_dimensions(displays)
    canvas = Image.new('RGB', (total_width, total_height))
    for display in displays:
        image = images.pop(0)
        new_dimensions = calculate_proportional_dimensions(display, image)
        image = image.resize(new_dimensions)
        image = image.crop(box=calculate_crop_box(display, image))
        canvas.paste(image, (display.offset_w, display.offset_h))
    return canvas


def configure_environment(setter=None):
    env = environ.copy()
    env['DISPLAY'] = ':0'
    if setter == 'gnome':
        # Identify PID of gnome session
        cmd_str = 'pgrep -f "gnome-session" | head -n1'
        cmd = run(cmd_str, shell=True, capture_output=True)
        pid = int(cmd.stdout.decode('utf-8').replace('\n', ''))

        # Get DBUS_SESSION_BUS_ADDRESS from environment
        cmd_str = f'grep -z DBUS_SESSION_BUS_ADDRESS /proc/{pid}/environ|cut -d= -f2-'
        cmd = run(cmd_str, shell=True, capture_output=True)
        dbus_sba = cmd.stdout.decode('utf-8').replace('\n', '').replace('\x00', '')

        env['DBUS_SESSION_BUS_ADDRESS'] = dbus_sba
    return env


def ensure_image_source(images_dir, unsplash):
    """Ensure that at least one valid image source is specified"""
    if images_dir:
        if not images_dir.exists() or not images_dir.is_dir():
            help_str = f"images_dir is invalid: {images_dir}"
            exit(help_str)
    elif not unsplash:
        help_str = "No file source specified, check configuration"
        exit(help_str)


def gather_displays():
    """Gather and return list of Display objects representing physical
    displays connected to the system
    """

    # Capture display resolution and arrangement information
    cmd_str = 'xrandr | grep " connected"'
    cmd = run(cmd_str, env=configure_environment(), shell=True, capture_output=True)
    displays_raw = cmd.stdout.decode('utf-8').split('\n')

    # Build list of Display objects
    displays = []
    for dr in displays_raw:
        if dr:
            if 'primary' in dr:
                dimensions = dr.split(' ')[3]
            else:
                dimensions = dr.split(' ')[2]
            displays.append(Display(*dimensions.split('+')))

    # Bail if no displays were instantiated
    if len(displays) == 0:
        help_str = 'No displays detected - environment not supported'
        exit(help_str)

    return displays


def gather_random_local_images(displays, images_dir):
    """Gather collection of random local images to match count of displays"""
    image_paths = []
    for i in range(len(displays)):
        image_paths.append(select_random_child_path(images_dir))
    return [Image.open(ip) for ip in image_paths]


def gather_random_unsplash_images(displays, max_resolution_w, max_resolution_h, collections, orientation):
    """Gather collection of random unsplash images to match count of displays -
    each image must be constrained to provided maximum dimensions, unsplash
    collection name list, and orientation
    """
    images = []
    for idx, display in enumerate(displays):
        resolution_w = display.resolution_w if max_resolution_w >= display.resolution_w else max_resolution_w
        resolution_h = display.resolution_h if max_resolution_h >= display.resolution_h else max_resolution_h
        image = get_unsplash_image(
            resolution_w,
            resolution_h,
            collections,
            orientation)
        images.append(image)
        if idx < len(displays) - 1:
            # Slow down between requests - unsplash rate limits
            sleep(1)
    return images


def get_unsplash_image(resolution_w, resolution_h, collections, orientation):
    """Get image from unsplash of specified dimensions matching provided
    collection names list and orientation ('landscape', 'portrait') to filter
    results
    """
    endpoint = 'https://source.unsplash.com/random'
    resolution = f'{resolution_w}x{resolution_h}'
    orientation = f'orientation={orientation}'
    collections = f'&{",".join(collections)}'
    url = f'{endpoint}/{resolution}?{orientation}{collections}'
    response = get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))


def import_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except IOError:
        # Config file doesn't exist - load the default
        with open(BASE_DIR.joinpath('config.yaml'), 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def select_random_child_path(parent_path):
    return str(choice([x for x in Path(parent_path).glob('*')]))


def set_wallpaper(wallpaper_setter, image_file_path):
    wallpaper_setter(image_file_path)


def set_wallpaper_gnome(image_file_path):
    # Configure environment
    env = configure_environment('gnome')

    # Set newly generated image as background
    cmd_list = [
        'gsettings',
        'set',
        'org.gnome.desktop.background',
        'picture-uri',
        f'file://{str(image_file_path)}'
    ]
    run(cmd_list, env=env, capture_output=True)


def set_wallpaper_nitrogen(image_file_path):
    # Configure environment
    env = configure_environment('nitrogen')

    # Set newly generated image as background
    cmd_list = [
        'nitrogen',
        '--set-tiled',
        str(image_file_path)
    ]
    run(cmd_list, env=env, capture_output=True)


def main():
    # Import config
    config = import_config()

    # Unsplash configuration
    unsplash = config['unsplash']
    unsplash_collections = config['unsplash_collections']
    unsplash_max_resolution_w = config['unsplash_resolution_w']
    unsplash_max_resolution_h = config['unsplash_resolution_h']
    unsplash_orientation = config['unsplash_orientation']

    # File path configuration
    images_dir = Path(config['images_dir']) if config['images_dir'] else None
    image_format = config['output_image_format']
    output_dir = Path(config['output_dir'])
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    temp_file = Path(f'{output_dir}/{timestamp}_nrw_out.{image_format}')
    output_file = Path(f'{output_dir}/{config["output_image_name"]}')

    # Configure wallpaper setter and function mappings
    wallpaper_setter = config['wallpaper_setter']
    wallpaper_setters = {
        'gnome': set_wallpaper_gnome,
        'nitrogen': set_wallpaper_nitrogen,
    }

    # Ensure that image source has been specified
    ensure_image_source(images_dir, unsplash)

    # Ensure that output_dir exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Gather list of Display objects
    displays = gather_displays()

    # Sort displays by offset_w (arrangement based on offset, left to right)
    displays.sort(key=lambda x: x.offset_w)

    # Stage Image objects for composition
    if unsplash:
        # Fetch unsplash images
        images = gather_random_unsplash_images(
            displays,
            unsplash_max_resolution_w,
            unsplash_max_resolution_h,
            unsplash_collections,
            unsplash_orientation)
    else:
        # Fetch random local image paths
        images = gather_random_local_images(displays, images_dir)

    # Compose images on canvas
    canvas = compose_images(displays, images)

    # Save canvas to temp file
    canvas.save(temp_file, format=image_format)

    # Move temp file to output file (initial image write is slow)
    move(temp_file, output_file)

    # Set wallpaper
    set_wallpaper(wallpaper_setters[wallpaper_setter], output_file)


if __name__ == '__main__':
    main()
