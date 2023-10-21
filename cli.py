import logging
import os
from pathlib import Path
import click
import zipfile
from PIL import Image


def extract_maps_from_zip(zip_ref):
    """Extract map names from a zip reference."""
    return [
        file_name.split("/")[1][:-4]
        for file_name in zip_ref.namelist()
        if file_name.endswith(".bsp")
    ]


def extract_levelshots_from_map(zip_ref, map_name):
    """Extract and save levelshot images for a given map from a zip reference."""
    levelshots = [
        file_name
        for file_name in zip_ref.namelist()
        if file_name in [f"levelshots/{map_name}.tga", f"levelshots/{map_name}_cc.tga"]
    ]

    for file_name in levelshots:
        try:
            with zip_ref.open(file_name) as tga_file:
                base_name = os.path.basename(file_name).split(".")[0]
                with Image.open(tga_file) as img:
                    img = img.convert("RGB")
                    img.save(f"levelshots/{base_name}.jpg")
        except Exception:
            logging.exception(f"Failed to extract levelshot for {map_name}")


@click.command()
@click.argument("path", type=click.Path(exists=True))
def read(path: str):
    """Extract and convert levelshots from pk3 files."""
    Path("levelshots").mkdir(parents=True, exist_ok=True)

    for file in os.listdir(path):
        if file.endswith(".pk3"):
            with zipfile.ZipFile(Path(path) / file, "r") as zip_ref:
                maps = extract_maps_from_zip(zip_ref)

                for map_name in maps:
                    extract_levelshots_from_map(zip_ref, map_name)


if __name__ == "__main__":
    read()
