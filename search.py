# from lib2to3.pytree import Node
from __future__ import annotations
from typing import TypeVar, Generic, List, Optional, Callable, Set, Dict
from heapq import heappush, heappop

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self):
        self._list_container: List[T] = []

    def is_empty(self):
        return not self._list_container

    def push(self, item: T):
        self._list_container.append(item)

    def pop(self):
        return self._list_container.pop()


class Node(Generic[T]):
    def __init__(self, state: T, parent_node: Optional[Node], cost: float = 0.0, heuristic_value: float = 0.0) -> None:
        self.state: T = state
        self.parent_node: Optional[Node] = parent_node
        self.cost: float = cost
        self.heuristic_value: float = heuristic_value

    def __lt__(self, node: Node):
        return (self.cost + self.heuristic_value) < (node.cost + node.heuristic_value)


def dfs(initial: T, test_goal: Callable[[T], bool], move: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # node we have to explore
    front: Stack[Node[T]] = Stack()
    # push node to the list
    front.push(Node(initial, None))
    # current node that we explored
    explored_nodes: Set[T] = {initial}

    # exploring the maze
    while not front.is_empty():
        current_node: Node[T] = front.pop()
        current_state: T = current_node.state

        # if we found the goal
        if test_goal(current_state):
            return current_node

        # going to the next node that we haven't explored
        for node in move(current_state):
            # if we already explored that
            if node in explored_nodes:
                continue

            explored_nodes.add(node)
            front.push(Node(node, current_node))
        print(explored_nodes)

    return None  # you found nothing


def select_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work backwards from end to front
    while node.parent_node is not None:
        node = node.parent_node
        path.append(node.state)
    path.reverse()
    return path


# A* implementation

class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def is_empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)

    def pop(self) -> T:
        return heappop(self._container)

    def __repr__(self) -> str:
        return repr(self._container)


def a_star(initial: T, test_goal: Callable[[T], bool], move: Callable[[T], List[T]],
           heuristic: Callable[[T], float]) -> Optional[Node[T]]:
    front: PriorityQueue[Node[T]] = PriorityQueue()
    front.push(Node(initial, None, 0.0, heuristic(initial)))
    explored: Dict[T, float] = {initial: 0.0}

    # keep going while there is more to explore
    while not front.is_empty:
        current_node: Node[T] = front.pop()
        current_state: T = current_node.state

        if test_goal(current_state):
            return current_node

        for node in move(current_state):
            new_cost: float = current_node.cost + 1

            if node not in explored or explored[node] > new_cost:
                explored[node] = new_cost
                front.push(Node(node, current_node, new_cost, heuristic(node)))
    return None

