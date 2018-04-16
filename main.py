class WGC_Node:
    incompatibilities = [
        ["c", "g", "w"],
        ["g", "w"],
        ["c", "g"]
    ]

    def __init__(self, west=["w", "c", "g"], east=[], boat_side=False, children=[]):
        self.west = west
        self.east = east
        self.boat_side = boat_side
        self.children = children

    def __str__(self):
        return str(self.west) + str(self.east) + ("Left" if not self.boat_side else "Right")

    def generate_children(self, previous_states, parent_map):
        children = []
        if not self.boat_side:
            for i in self.west:
                new_west = self.west[:]
                new_west.remove(i)
                new_east = self.east[:]
                new_east.append(i)
                if sorted(new_west) not in WGC_Node.incompatibilities and not WGC_Node.state_in_previous(previous_states, new_west, new_east, not self.boat_side):
                    child = WGC_Node(new_west, new_east, not self.boat_side, [])
                    children.append(child)
                    parent_map[child] = self
            if sorted(self.west) not in WGC_Node.incompatibilities and not WGC_Node.state_in_previous(previous_states, self.west[:], self.east[:], not self.boat_side):
                child = WGC_Node(self.west[:], self.east[:], not self.boat_side, [])
                children.append(child)
                parent_map[child] = self
        else:
            for i in self.east:
                new_west = self.west[:]
                new_west.append(i)
                new_east = self.east[:]
                new_east.remove(i)
                if sorted(new_east) not in WGC_Node.incompatibilities and not WGC_Node.state_in_previous(previous_states, new_west, new_east, not self.boat_side):
                    child = WGC_Node(new_west, new_east, not self.boat_side, [])
                    children.append(child)
                    parent_map[child] = self
            if sorted(self.east) not in WGC_Node.incompatibilities and not WGC_Node.state_in_previous(previous_states, self.west[:], self.east[:], not self.boat_side):
                child = WGC_Node(self.west[:], self.east[:], not self.boat_side, [])
                children.append(child)
                parent_map[child] = self
        self.children = children

    @staticmethod
    def state_in_previous(previous_states, west, east, boat_side):
        return any(
            sorted(west) == sorted(i.west) and
            sorted(east) == sorted(i.east) and
            boat_side == i.boat_side
            for i in previous_states
        )


def find_solution(root_node, use_bfs=False):
    '''
    Find a solution to the WGC Problem.
    use_bfs: False for DFS, True for BFS
    '''
    to_visit = [root_node]
    node = root_node
    previous_states = []
    parent_map = {root_node: None}
    while to_visit:
        node = to_visit.pop()
        if not WGC_Node.state_in_previous(previous_states, node.west, node.east, node.boat_side):
            previous_states.append(node)
        node.generate_children(previous_states, parent_map)
        if use_bfs:
            to_visit = node.children + to_visit
        else:
            to_visit = to_visit + node.children
        if sorted(node.east) == ["c", "g", "w"]:
            solution = []
            while node is not None:
                solution = [node] + solution
                node = parent_map[node]
            return solution
    return None

if __name__ == "__main__":
    root = WGC_Node()
    solution = find_solution(root, use_bfs=False)
    print("DFS solution = [", end='')
    for i in solution:
        print(i, '\b, ', end='')
    print("\b\b]")

    solution = find_solution(root, use_bfs=True)
    print("BFS solution = [", end='')
    for i in solution:
        print(i, '\b, ', end='')
    print("\b\b]")
