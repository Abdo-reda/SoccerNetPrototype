import os
import subprocess
import signal
import logging
import time
from datetime import datetime
from parameters import *
from configuration import Configuration

PROCESSING = True


def create_folders(dir_path):
    # create the output folders if they don't exist
    if not os.path.exists(dir_path + '/chunk_generator/input_stream'):
        os.makedirs(dir_path + '/chunk_generator/input_stream')
    if not os.path.exists(dir_path + '/chunk_generator/generated_chunks'):
        os.makedirs(dir_path + '/chunk_generator/generated_chunks')
    if not os.path.exists(dir_path + '/chunk_generator/generated_chunks/video_chunks'):
        os.makedirs(dir_path + '/chunk_generator/generated_chunks/video_chunks')
    if not os.path.exists(dir_path + '/chunk_generator/generated_chunks/audio_chunks'):
        os.makedirs(dir_path + '/chunk_generator/generated_chunks/audio_chunks')
    if not os.path.exists(dir_path + '/chunk_generator/generated_chunks/transcript_chunks'):
        os.makedirs(dir_path + '/chunk_generator/generated_chunks/transcript_chunks')
    if not os.path.exists(dir_path + '/feature_extraction/generated_features'):
        os.makedirs(dir_path + '/feature_extraction/generated_features')
    if not os.path.exists(dir_path + '/output_generation/generated_output'):
        os.makedirs(dir_path + '/output_generation/generated_output')


def build_model_wrapper(model_configuration):
    return buildModel(model_configuration)


def main(args):
    # ---------------- Initialize some stuff
    timer = time.time()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    create_folders(dir_path)

    # ---------------- Initilize the processes
    process_capture_stream = subprocess.Popen(['python', dir_path + '/chunk_generator/capture_stream.py'])
    process_generate_chunks = subprocess.Popen(['python', dir_path + '/chunk_generator/generate_chunks.py'])
    #process_transcribe_audio = subprocess.Popen(['python', dir_path + '/chunk_generator/transcribe_audio.py']) #rename to generate_transcription
    process_generate_features = subprocess.Popen(['python', dir_path + '/feature_extraction/generate_features.py'])
    process_generate_output = subprocess.Popen(['python', dir_path + '/output_generation/generate_output.py'])

    # --------------- Process Chunks and Generate Output

    # --------------- Handling Program Exit
    def handling_program_exit(signal_number, frame):
        process_capture_stream.terminate()
        process_generate_chunks.terminate()
        #process_transcribe_audio.terminate()
        process_generate_features.terminate()
        process_generate_output.terminate()
        global PROCESSING
        PROCESSING = False
        print('\n-------exiting------\n')

    signal.signal(signal.SIGINT, handling_program_exit)
    while PROCESSING:
        # ....processing
        pass


if __name__ == "__main__":

    # -----Get Any Parameters Regarding the Input Video & Model
    myConfiguration = Configuration()
    args = myConfiguration.get_configuration()

    # ------Setup Logging, directory and level.
    numeric_level = getattr(logging, 'INFO', None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level')

    #run_path = os.path.join('/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/output', datetime.now().strftime('RUN_%Y-%m-%d_%H-%M-%S'))
    #os.makedirs(run_path)
    log_path = '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/output_generation' + '/run.log'

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])

    # # ----Sets up the values for some environment variables, not sure if they are used but they could be important ..
    # os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    # os.environ["CUDA_VISIBLE_DEVICES"] = str(0)

    main(args)
