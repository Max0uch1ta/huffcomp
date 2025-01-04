import heapq

class Node:
    def __init__(self, weight:int ) -> None:
        self.__weight = weight
        self.__is_leaf = False

    def get_weight(self)->int:
        return self.__weight
    
    def is_leaf(self)->bool:
        return self.__is_leaf
    
    def __lt__(self, other)->bool :
        return self.get_weight() < other.get_weight()

    def __repr__(self):
        return self.__str__()


# Character nodes with their weight. They will be the leafs of the huffman tree
class CharNode(Node):
    def __init__(self, c:str, weight:int ) -> None:
        super().__init__(weight)
        self.__is_leaf = True
        self.__char = c
    
    def get_c(self)->str:
        return self.__char

    def __str__(self) -> str:
        return f"({self.get_c()}: {self.get_weight()})"
    

# Internal nodes, represent the weight of all their CharNode children
class InterNode(Node):
    def __init__(self, node1: Node, node2: Node) -> None:
        super().__init__(node1.get_weight() + node2.get_weight())
        self.__is_leaf = False
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





def file_to_dict(path : str)-> dict:
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

