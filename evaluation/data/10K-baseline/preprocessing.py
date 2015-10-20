__author__ = 'hadyelsahar'

"""
script to preprocess 10K-baseline dataset
"""

import argparse
import re
import codecs

parser = argparse.ArgumentParser(description='script to preprocess 10K-baseline dataset')
parser.add_argument('-i', '--input', help='input raw file', required=True)
parser.add_argument('-o', '--output', help='output file', required=True)
args = parser.parse_args()


fi = codecs.open(args.input, 'r', encoding="utf-8")
output = set()
for l in fi:
    # removal of quotes in front and end
    l = re.sub(r"^\"", "", l)
    l = re.sub(r"\"$", "", l)
    # removal of in between brackets and fwd slashes
    l = re.sub(r"\(.*\)", " ", l)
    l = re.sub(r"/.*/", " ", l)

    # Take first two sentences only for easing handling of coreferences resolution and topic drifts
    # or Take the First sentence if it's long enough
    l = l.split(".")
    if len(l[0].split(" ")) > 15:
        l = l[0] + " ."
    else:
        continue
        # l = " . ".join(l[:2]) + " ."

    # replace tabs by
    l = re.sub(r"\t", " ", l)
    l = re.sub(r"\s+", " ", l)
    l = re.sub(r"\n+", "\n", l)

    # remove special entries
    l = re.sub(r".*\. \..*", "", l)
    l = re.sub(r".*[Tt]emplate.*", "", l)
    l = re.sub(r".*Coordinates.*", "", l)

    output.add(l)


fo = codecs.open(args.output, 'w', encoding="utf-8")
fo.write("\n".join(output))

fi.close()
fo.close()

