# zhconvert.py
import argparse
from opencc import OpenCC

parser = argparse.ArgumentParser(description='Convert between Simplified and Traditional Chinese.')
parser.add_argument('text', help='Text to convert')
parser.add_argument('--mode', default='s2t', choices=[
    's2t', 't2s', 's2tw', 'tw2s', 's2hk', 'hk2s', 't2tw', 'tw2t'
], help='Conversion mode')
args = parser.parse_args()

cc = OpenCC(args.mode)
converted = cc.convert(args.text)
print(converted)
