import heapq
from os import close, name
from typing import Union, Optional


class Node:
    """
        Huffman tree representation where a node is either a char (leaf) of internal Node.
        More of an Abstract class

        Attributes:
            __weight = the weight of the tree
            __is_leaf = boolean if char
            __left = left child, None if no left child
            __right = right child, None if no right child
    """
    def __init__(self, weight:int ) -> None:
        self.__weight = weight
        self.__is_leaf = False
        self.__left = None
        self.__right = None

    def get_weight(self)->int:
        return self.__weight
    
    def is_leaf(self)->bool:
        return self.__is_leaf

    def get_left(self)->Union["Node",None]:
        return self.__left

    def get_right(self)->Union["Node", None]:
        return self.__right
    
    def get_c(self)->str:
        return ""
   
    def __lt__(self, other)->bool :
        return self.get_weight() < other.get_weight()

    def __repr__(self):
        return self.__str__()
    
    def tree_to_str(self)-> str:
        """
        Preorder tree traversal, appends the node and it's children to string. 
        If node add 0, if leaf add 1 and the char value

        returns:
            the tree representation with the current node and it's children
        """
        if self.is_leaf() :
            return "1"+self.get_c()


        left = ""
        right = ""
        if self.get_left():
            left = self.get_left().tree_to_str()
        if self.get_right():
            right = self.get_right().tree_to_str()


        return "0" + left + right





# Character nodes with their weight. They will be the leafs of the huffman tree
class CharNode(Node):
    def __init__(self, c:str, weight:int ) -> None:
        super().__init__(weight)
        self.__is_leaf = True
        self.__char = c
   
    def is_leaf(self) -> bool:
        return self.__is_leaf

    def get_c(self)->str:
        return self.__char

    def __str__(self) -> str:
        return f"({self.get_c()}: {self.get_weight()})"
    

# Internal nodes, represent the weight of all their CharNode children
class InterNode(Node):
    def __init__(self, node1: Node, node2: Node) -> None:
        super().__init__(node1.get_weight() + node2.get_weight())        
        self.set_children(node1, node2)
    
    def set_children(self, node1: Node, node2: Node):
        if node1 < node2 :
            self.__left = node1
            self.__right = node2
        else:
            self.__left = node2
            self.__right = node1

    def get_left(self)->Node:
        return self.__left

    def get_right(self)->Node:
        return self.__right

    def __str__(self) -> str:
        return f"(Internal Node: {self.get_weight()})"


# Takes a hufmann tree and makes a corresponding table
def get_hdict(tree:Node, d:dict, code:str="") -> None:
    if tree != None:
        if tree.is_leaf():
            char = tree.get_c()
            d[char] = code
        else:
            get_hdict(tree.get_left(), d, code+"0")
            get_hdict(tree.get_right(), d, code+"1")



# take a file and create a frequency dictionary 
def file_to_dict(path : str)-> dict:
    """
    Takes a txt file and creates a frequency dictrionnary out of it

    Args:
        path: a path to a txt file

    Returns:
        A dict with characters as keys and their occurence frequency as value.
        example:
            {'c': 16,
             'a': 2,
             's': 1}

    """
    freq:dict = {}
    with open(path) as f:
        while True:
            c = f.read(1)
            if not c:
                print("end of file")
                break
            # add 1 to corresponding
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1
    return freq


def dic_to_heap(freq:dict)->list:
    heap = []
    for char in freq:
        node = CharNode(char, freq[char])
        heapq.heappush(heap, node)
    return heap

def heap_to_htree(heap:list)->Node:
    while (len(heap) > 1) :
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = InterNode(node1, node2)
        heapq.heappush(heap, merged)
    return heap[0]

def file_compression(path: str, htable: dict, tree_rep: bytes)-> str:
    """
        Compresses a text file with a given table created with a Huffman Tree.

        Args:
            tree_rep:
                String representation of the huffman tree
            path:
                Path to the text file we want to compress
            htable:
                Huffman based dict used for conversion

        returns:
            Path to the new compressed file. File header contains the string representation
            of the tree for decompression as well as compressed data.
    """
    byte = 0
    bit_count = 0

    with open(path, "r") as f:
        comp_path = path+".hcp"
        with open(comp_path, "wb") as compf:
            compf.write(tree_rep)
            while True:
                c = f.read(1)
                if not c:
                    break
                code = htable[c]
                for bit in code:
                    # Error handling
                    if bit not in [1,0]:
                        print("Error: can only add bits")
                    byte = (byte<<1) | bit
                    bit_count += 1

                    if bit_count == 8:
                        compf.write(bytes([byte]))

            if bit_count > 0:
                byte<<=(8-bit_count)
                compf.write(bytes([byte]))
    return comp_path

def file_decompression(path: str, tree: Union[InterNode, CharNode])->str:
    head = tree
    it = tree
    # TODO add possibility to give filename
    output_path = path[:-4] # remove the file extension
    output_file = open(output_path, "w")
    with open(path, "rb") as compf:
        byte = compf.read(1)
        # Get each bit from byte and go through tree
        for bit in get_bits_from_byte(byte):
            if bit == 0:
                it = it.get_left()
            else:
                it = it.get_right()
            if it.is_leaf():
                output_file.write(it.get_c())
                it = head


    output_file.close()
    return ""

def get_bits_from_byte(byte: bytes):
    for i in range(8):
        bit = (byte[0] >> i) & 1 # mask all but last bit I'm extracting
        yield bit

# TODO need to continue reading tree, 1 + children 
def get_tree_bytes(node: Node) -> bytes:
    if node:
        if isinstance(node, CharNode):
            char_bytes = node.get_c().encode('utf-8')  # Encode char into bytes using UTF-8
            len_char = len(char_bytes).to_bytes(1) # len in bytes (big endian by default) 
            # b'' -> bite representation
            return b'0' + len_char + char_bytes # Prefix with '0', and length
        else:
            return b'1' + get_tree_bytes(node.get_left()) + get_tree_bytes(node.get_right())
    return b''

    

if __name__ == "__main__":

    dic: dict[str, int] = file_to_dict("smalltest.txt")
    heap: list[CharNode] = dic_to_heap(dic)
    htree = heap_to_htree(heap)
    tree_str = get_tree_bytes(htree)
    print(tree_str)


