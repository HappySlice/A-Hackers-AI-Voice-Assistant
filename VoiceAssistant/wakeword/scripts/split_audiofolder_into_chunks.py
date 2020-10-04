import os
import argparse
from pydub import AudioSegment
from pydub.utils import make_chunks

def main(args):

    def chunk_and_save(entry):
        audio = AudioSegment.from_file(entry.path)
        length = args.seconds * 1000 # this is in miliseconds
        chunks = make_chunks(audio, length)
        names = []
        for i, chunk in enumerate(chunks):
            _name = entry.path.split("/")[-1]
            name = "{}_{}".format(i, _name)
            wav_path = os.path.join(args.save_path, name)
            chunk.export(wav_path, format="wav")
        return names

    directory = args.audio_folder

    for entry in os.scandir(directory):
        if(entry.path.endswith(".wav")) and entry.is_file():
            chunk_and_save(entry)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="script to split audio files into chunks")
    parser.add_argument('--seconds', type=int, default=None,
                        help='if set to None, then will record forever until keyboard interrupt')
    parser.add_argument('--audio_folder', type=str, default=None, required=True,
                        help='name of audio folder')
    parser.add_argument('--save_path', type=str, default=None, required=True,
                        help='full path to to save data. i.e. /to/path/saved_clips/')

    args = parser.parse_args()

    main(args)
