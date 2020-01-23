import imageio
from pathlib import Path
import os
import logging

logger = logging.getLogger("AnimationGenerator")


class AnimationGenerator:
    def __init__(self, game_id):
        self.game_id = game_id
        self.saving_path = Path("Images") / self.game_id

        self.image_paths = []
        self.images = []

        self.file_created = False

    def gather_image_paths(self):
        """Gather image paths in game id folder
        """
        self.image_paths = [
            self.saving_path / file
            for file in os.listdir(self.saving_path)
            if file[-4:] == ".png"
        ]
        self.image_paths.sort()
        logger.info("Image paths gathered")

    def import_images(self):
        """Gather images in game id folder
        """
        if len(self.image_paths) > 0:
            self.images = [imageio.imread(file) for file in self.image_paths]
            logger.info("Images loaded")
        else:
            logger.error("No image path loaded")

    def generate_gif(self, duration_input):
        """Generate game gif
        """
        if len(self.images) > 0:
            logger.info("Generating GIF")
            imageio.mimsave(
                self.saving_path / (self.game_id + ".gif"),
                self.images,
                duration=duration_input,
            )
            self.file_created = True
            logger.info("Done")
        else:
            logger.error("No image loaded")

    def clean_up_and_move(self):
        """Delete all images and move gif to gif folder
        """
        if self.file_created:
            for file in self.image_paths:
                os.remove(file)
            os.rename(
                self.saving_path / (self.game_id + ".gif"),
                Path("Images/game_gifs") / (self.game_id + ".gif"),
            )
            os.rmdir(self.saving_path)
        else:
            logger.error("File has not been created yet")

    def execute_whole_process(self, duration_input, delete_after_creation=True):
        """Execute whole process until gif generation
        
        Args:
            duration_input (float): Duration per image in seconds
        """
        self.gather_image_paths()
        self.import_images()
        self.generate_gif(duration_input)

        if delete_after_creation:
            self.clean_up_and_move()

