from spleeter.separator import Separator


class AudioSeparator:
    def __init__(self, configuration='spleeter:2stems'):
        self.separator = Separator(configuration)

    def separate(self, audio_file, output_folder='out'):
        try:
            # Perform the separation
            self.separator.separate_to_file(audio_file, output_folder)
            return True, "Separation completed successfully!"
        except Exception as e:
            return False, str(e)
