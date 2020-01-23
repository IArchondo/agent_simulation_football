import imageio
from pathlib import Path
from os import listdir
import logging

logger = logging.getLogger("AnimationGenerator")


class AnimationGenerator:
    def __init__(self, game_id):
        self.game_id = game_id
        self.saving_path = Path("Images") / self.game_id

        self.image_paths = []
        self.images = []

    def gather_image_paths(self):
        """Gather image paths in game id folder
        """
        self.image_paths = [
            self.saving_path / file
            for file in listdir(self.saving_path)
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
            logger.info("Done")
        else:
            logger.error("No image loaded")

    def execute_whole_process(self, duration_input):
        """Execute whole process until gif generation
        
        Args:
            duration_input (float): Duration per image in seconds
        """
        self.gather_image_paths()
        self.import_images()
        self.generate_gif(duration_input)

