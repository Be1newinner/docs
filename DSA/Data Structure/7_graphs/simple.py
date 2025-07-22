from typing import List, Tuple

routes = [
    ("Mumbai", "Paris"),
    ("Mumbai", "Dubai"),
    ("Paris", "Dubai"),
    ("Paris", "New York"),
    ("Dubai", "New York"),
    ("New York", "Toronto"),
]


class Graph:
    def __init__(self, edges: List[Tuple[str, str]]):
        self.edges = edges
        self.graph_dict: dict[str, list[str]] = {}
        for start, end in self.edges:
            if start in self.graph_dict:
                self.graph_dict[start].append(end)
            else:
                self.graph_dict[start] = [end]
                
    def get_all_paths(self, start: str, end: str, path: list[str] = []):
        path = path + [start]
        
        if start == end:
            return [path]
        
        if start not in self.graph_dict:
            return []
        
        if start in self.graph_dict:
            if not len(self.graph_dict[start]):
                return []
            else:
                temp_paths = []
                for node in self.graph_dict[start]:
                    new_paths = self.get_all_paths(node, end, path)
                    for p in new_paths:
                        temp_paths += [p]
                return temp_paths
                
        return path
    
    
    def find_shortest_path(self, start, end):
        if start == end:
            return []
        
        all_paths = self.get_all_paths(start, end)
        
        if all_paths:
            shortest_index = None
            shortest_length = float('inf')
            for path_index in range(len(all_paths)):
                if len(all_paths[path_index]) < shortest_length:
                    shortest_length = len(all_paths[path_index])
                    shortest_index = path_index
            return all_paths[shortest_index]
            
        else:
            return []
        
graph = Graph(routes)


print(graph.get_all_paths("Mumbai", "New York"))
print(graph.find_shortest_path("Mumbai", "New York"))
# expected output of Graph() constructor
# d = {
#     "Mumbai": ["Paris", "Dubai"],
#     "Paris": ["Dubai", "New York"],
#     "Dubai": ["New York"],
#     "New York": ["Toronto"],
# }
