import pygame as pg
import heapq
import settings
import utils
vec = pg.math.Vector2

def heuristic(a, b):
    return (abs(a.x - b.x) + abs(a.y - b.y)) *10

def a_star_algorithm(graph, start, end):
    frontier = priorityQueue()
    frontier.enQueue(utils.vec2int(start), 0)
    path = {}
    cost = {}
    path[utils.vec2int(start)] = None
    cost[utils.vec2int(start)] = 0

    while not frontier.isEmpty():
        current = frontier.deQueue()
        if current == end:
            break
        for nb in graph.find_neighbors(vec(current)):
            nb = utils.vec2int(nb)
            # c(move) = f(x) + g(x) #
            # cost = costUpToHere + heuristic
            nextCost = cost[current] + graph.cost(current, nb)
            if nb not in cost or nextCost < cost[nb]:
                cost[nb] = nextCost
                priority = nextCost + heuristic(end, vec(nb))
                frontier.enQueue(nb, priority)
                path[nb] = vec(current) - vec(nb)
    return path

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
    current = frontier.get()

   if current == goal:
      break
   
   for next in graph.neighbors(current):
      new_cost = cost_so_far[current] + graph.cost(current, next)
      if next not in cost_so_far or new_cost < cost_so_far[next]:
         cost_so_far[next] = new_cost
         priority = new_cost + heuristic(goal, next)
         frontier.put(next, priority)
         came_from[next] = current

class priorityQueue:
    def __init__(self):
        self.nodes = []
    def enQueue(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))
    def deQueue(self):
        return heapq.heappop(self.nodes)[1]
    def isEmpty(self):
        return len(self.nodes) == 0

