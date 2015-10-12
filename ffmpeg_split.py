import re
import math
from optparse import OptionParser
from subprocess import check_call, PIPE, Popen
import shlex, os

def main():
    filename, split_length, split_offset = parse_options()
    #filename.replace("'", "")
    #print(filename.encode('cp866'))
    #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    filename = os.path.join(os.getcwd(), filename)
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if split_length <= 0:
        print("Split length can't be 0")
        raise SystemExit

    p1 = Popen(shlex.split(("ffmpeg_duration.bat" + ' "' + filename + '" ' + "ffmpeg").encode('cp866').decode('cp1251')), stdout=PIPE)
    output = p1.stdout.read()
    video_length = int(output)
    p1.stdout.close()
    print("Video length in seconds: {}".format(video_length))

    split_count = int(math.ceil(video_length / split_length))
    print("Split count: {}".format(split_count))

    if split_count == 1:
        print("Video length is less than the target split length.")
        raise SystemExit

    for n in range(split_count):
        split_start = split_length * n
        pth, ext = filename.rsplit(".", 1)
        cmd = 'ffmpeg -ss {} -i "{}" -t {} -c copy "{}_part{}.{}"'.\
            format(split_start, filename, split_length + split_offset, pth, n + 1, ext)
        print("About to run: {}".format(cmd))
        check_call(shlex.split(cmd.encode('cp866').decode('cp1251')), universal_newlines=True)


def parse_options():
    parser = OptionParser()

    parser.add_option("-f", "--file",
                      dest="filename",
                      help="file to split, for example sample.avi",
                      type="string",
                      action="store"
    )
    parser.add_option("-s", "--split-size",
                      dest="split_size",
                      help="split or chunk size in seconds, for example 3550",
                      type="int",
                      action="store"
    )
    parser.add_option("-d", "--split-offset",
                      dest="split_offset",
                      help="split offset in seconds, for example 5",
                      type="int",
                      action="store"
    )
    (options, args) = parser.parse_args()

    if options.filename and options.split_size:
        if not options.split_offset:
            options.split_offset = 0
        return options.filename, options.split_size, options.split_offset
    else:
        parser.print_help()
        raise SystemExit

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
