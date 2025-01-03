import argparse
import helpers 

parser = argparse.ArgumentParser(prog="huffcomp",description="A compression tool using Huffman Tree")


group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-c","--compress",  help="flag for compressing file given as argument", action="store_true")
group.add_argument("-d","--decompress",  help="flag for decompressing file given as argument", action="store_true")
parser.add_argument("file", metavar="file", type=str, help="file you want to compress or decompress")


args = parser.parse_args()
print(args)

if args.compress == True:
    print("compressing")
    freq = helpers.file_to_dict(args.file)
    heap = helpers.dic_to_heap(freq)
    print(freq)
    print(heap)

    
elif args.decompress == True:
    print("decompressing")

#print(args)


