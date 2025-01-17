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
    tree = helpers.heap_to_htree(heap)
    print(heap)
    print(tree)
    huff_table = {}
    helpers.get_hdict(tree, huff_table)
    print(huff_table)
    print("\n\n")
    print(tree.tree_to_str())

    for char in huff_table:
        if len(huff_table[char]) < 5:
            print(f"{char} : {huff_table[char]}")
    
elif args.decompress == True:
    print("decompressing")

#print(args)


