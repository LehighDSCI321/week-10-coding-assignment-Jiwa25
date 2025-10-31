'''
this module is for week 10 coding
'''
from collections import deque

try:
    import graphviz
except ImportError:
    pass

try:
    from bokeh.plotting import figure, show
    from bokeh.models import ColumnDataSource
    from bokeh.palettes import Bright6
except ImportError:
    pass

class VersatileDigraph:
    '''
    represent a digraph
    '''
    def __init__(self) -> None:
        '''
        initialize the class
        '''
        self.nodes = {}         # store nodes' ids
        self.edges = {}         # store edges
        self.edge_names = {}    # store edges' names

    def add_edge(self, start_node_id, end_node_id, **kwargs) -> None:
        '''
        add an edge to the graph
        '''
        start_node_value = kwargs.get('start_node_value',0)
        end_node_value = kwargs.get('end_node_value',0)
        edge_name = kwargs.get('edge_name',start_node_id + "->" + end_node_id)
        edge_weight = kwargs.get('edge_weight',0)
        if not isinstance(edge_weight, int) and not isinstance(edge_weight, float):
            raise TypeError('edge weight must be numeric')
        if edge_weight < 0:
            raise ValueError('edge weight must be non-negative')

        # if there is an edge from start node
        if start_node_id not in self.edges:
            self.edges[start_node_id] = {end_node_id:[edge_name,edge_weight]}
            self.edge_names[start_node_id] = {edge_name:end_node_id}
        else:
            if edge_name in self.edge_names[start_node_id]:
                raise KeyError(f'there is already an edge {edge_name}')
            self.edges[start_node_id][end_node_id] = [edge_name,edge_weight]
            self.edge_names[start_node_id][edge_name]= end_node_id
        # add start node
        if start_node_id not in self.nodes:
            self.add_node(start_node_id,start_node_value)
        # add end node
        if end_node_id not in self.nodes:
            self.add_node(end_node_id,end_node_value)

    def add_node(self, node_id, node_value = 0) -> None:
        '''
        add the node to the graph
        '''
        if not isinstance(node_value, int) and not isinstance(node_value, float):
            raise TypeError('node value must be numeric')
        self.nodes[node_id] = node_value

    def get_nodes(self) -> list:
        '''
        return a list of nodes in the graph
        '''
        return list(self.nodes)

    def get_edge_weight(self, start_node, end_node) -> int:
        '''
        given the start_node and the end_node for an edge, return the edge weight
        '''
        if start_node in self.edges:
            if end_node in self.edges[start_node]:
                return self.edges[start_node][end_node][1]
        raise KeyError(f'there is no edge from {start_node} to {end_node}')

    def get_node_value(self, node_id) -> int:
        '''
        given a node_id, return the node value
        '''
        if node_id not in self.nodes:
            raise KeyError(f'there is no node {node_id}')
        return self.nodes[node_id]

    def print_graph(self) -> None:
        '''
        prints sentences describing the nodes and edges of the graph
        '''
        node = None
        for node in self.nodes.items():
            if node is None:
                print("There is not any node in this graph.")
                break
            print(f"Node {node[0]} with value {node[1]}.")
            if node[0] in self.edges:
                edge = None
                for edge in self.edges[node[0]]:
                    if edge is None:
                        break
                    print(f"Edge from {node[0]} to {edge} with "
                        f"weight {self.edges[node[0]][edge][1]} and "
                        f"name {self.edges[node[0]][edge][0]}.")

    def predecessors(self, node) -> list:
        '''
        return a list of nodes that immediately precede that node
        '''
        if node not in self.nodes:
            raise KeyError(f'there is no node {node}')
        return [edge[0] for edge in self.edges.items()
            for end_node in edge[1] if end_node[0] == node]

    def successors(self, node) -> list:
        '''
        return a list of nodes that immediately succeed that node
        '''
        if node in self.edges:
            return [end_node for end_node in self.edges[node]]  # check a mistake before w9
        return []

    def successor_on_edge(self, node, edge_name) -> str:
        '''
        return the successor of the node on the edge with the provided name
        '''
        return self.edge_names[node][edge_name]

    def in_degree(self, node) -> int:
        '''
        return the number of edges that lead to that node
        '''
        if node not in self.nodes:
            raise KeyError(f"there is no node {node}")
        in_degree = 0
        for edge in self.edges.items():
            for end_node in edge[1]:
                if end_node == node:
                    in_degree += 1
                    break
        return in_degree

    def out_degree(self, node) -> int:
        '''
        return the number of edges that lead from that node
        '''
        if node not in self.nodes:
            raise KeyError(f"there is no node {node}")
        if node in self.edges:
            return len(self.edges[node])
        return 0

    def plot_graph(self) -> None:
        '''
        make a plot of the object
        '''
        try:
            # create a digraph
            dot = graphviz.Digraph()
            # add nodes to the digraph
            for node in self.nodes.items():
                dot.node(node[0],f"{node[0]}:{node[1]}")
            # add edges to the digraph
            for edge in self.edges.items():
                for end_node in edge[1]:
                    dot.edge(edge[0],end_node,f"{edge[1][end_node][0]}:{edge[1][end_node][1]}")
            # render the digraph
            dot.render(view=True)
        except NameError as exc:
            raise ImportError(
                "The 'plot_graph' function requires the 'graphviz' library. "
                "Please install it by running: pip install graphviz"
            ) from exc

    def plot_edge_weights(self, title = '') -> None:
        '''
        make a bar graph showing the weight of each edge
        '''
        try:
            # get edge names and weights
            edge_names, edge_weights = [], []
            for edge in self.edges.items():
                for end_node in edge[1]:
                    edge_names.append(f'{edge[1][end_node][0]}\n({edge[0]} -> {end_node})')
                    edge_weights.append(edge[1][end_node][1])
            # sort the bars
            sorted_edges = sorted(edge_names, key=lambda x: edge_weights[edge_names.index(x)])
            # create a figure
            p = figure(x_range = sorted_edges, title = title)
            # color the bars
            source = ColumnDataSource(data=dict(edge=edge_names,weight=edge_weights,color=Bright6))
            # render vertical bars
            p.vbar(x='edge', top='weight', width=0.8, color='color', source=source)
            # customize the graph
            p.xaxis.major_label_orientation = 0.75
            p.y_range.start = 0
            # show the graph
            show(p)
        except NameError as exc:
            raise ImportError(
                "The 'plot_edge_weights' function requires the 'bokeh' library. "
                "Please install it by running: pip install bokeh"
            ) from exc

class SortableDigraph(VersatileDigraph):
    '''
    represent a sortable digraph
    '''
    def top_sort(self):
        '''
        return a topologically sorted list of nodes in the graph
        '''
        count = {u:self.in_degree(u) for u in self.nodes}   # in-degree for each node
        src_nodes = [u for u in self.nodes if count[u] == 0]    # initial/source nodes
        sorted_ls = []  # sorted list of nodes
        while src_nodes:
            u = src_nodes.pop()     # pick an initial node
            sorted_ls.append(u)     # use it as first of the rest
            for v in self.successors(u):
                count[v] -= 1       # uncount its outgoing degrees
                if count[v] == 0:   # new initial node
                    src_nodes.append(v)
        return sorted_ls

class TraversableDigraph(SortableDigraph):
    '''
    represent a traversable digraph
    '''
    # def dfs(self,node,visited=None):
    #     '''perform a depth-first search traversal'''
    #     if visited is None:
    #         visited = set()
    #     visited.add(node)
    #     for u in self.successors(node):
    #         if u not in visited:
    #             yield from self.dfs(u,visited)
 
    def dfs(self, node):
        '''perform a depth-first search traversal from a certain node'''
        # Visited set and LIFO stack
        visited, stack = set(node), []
        # We plan on visiting node's adjacent nodes
        stack.extend(self.successors(node))
        while stack:
            # Get one (Last-In, First-Out)
            u = stack.pop()
            if u not in visited:    # Unvisited
                visited.add(u)
                # Schedule all neighbors (append them to the end)
                stack.extend(self.successors(u))
                # Report u as visited
                yield u

    def bfs(self, node):
        '''
        perform a breadth-first search traversal from a certain node
        '''
        # parents dict and FIFO queue
        parents, queue = {node: None}, deque([node])
        while queue:
            u = queue.popleft()
            for v in self.successors(u):    # adjacent nodes
                if v not in parents:    # unvisited
                    parents[v] = u      # mark u as v's parent
                    queue.append(v)
                    yield v

class DAG(TraversableDigraph):
    '''
    represent a directed acyclic graph
    '''
    def add_edge(self, start_node_id, end_node_id, **kwargs) -> None:
        path = list(self.dfs(end_node_id))
        if start_node_id in path:
            raise ValueError(f"There will be a cycle at node {end_node_id}")
        return super().add_edge(start_node_id, end_node_id, **kwargs)
