import argparse
from .PhotoFrame import PhotoFrame

# configure argument parser
parser = argparse.ArgumentParser()
parser.add_argument('image', help='image file')

# TODO add --verbose
# parser.add_argument('--verbose', '-v', action='store_true', help='print all messages')

args = parser.parse_args()

# load data
with open(args.image, 'rb') as file:
    content = file.read()

# send to frame
pf = PhotoFrame.find()
pf.send(content, timeout=5000)
