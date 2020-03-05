import pygame as pg
import heapq
import settings
import utils
vec = pg.math.Vector2

def heuristic(a, b):
    # heuristic uses the distance between location and target
    return (abs(a.x - b.x) + abs(a.y - b.y)) * settings.s_tileSize

def a_star_algorithm(graph, start, end):
    frontier = priorityQueue()
    frontier.enQueue(utils.tup(start), 0)
    path = {}
    cost = {}
    path[utils.tup(start)] = None
    cost[utils.tup(start)] = 0

    while not frontier.isEmpty():
        current = frontier.deQueue()
        if current == end:
            break
        for nb in graph.find_neighbors(vec(current)):
            nb = utils.tup(nb)
            # c(move) = f(x) + g(x) ~> cost = costOfMove + heuristic
            nextCost = cost[current] + graph.cost(current, nb)
            if nb not in cost or nextCost < cost[nb]:
                cost[nb] = nextCost
                priority = nextCost + heuristic(end, vec(nb))
                frontier.enQueue(nb, priority)
                path[nb] = {"from": vec(current), "direct": vec(current)-vec(nb)}
    return path

class priorityQueue:
    def __init__(self):
        self.nodes = []
    def enQueue(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))
    def deQueue(self):
        return heapq.heappop(self.nodes)[1]
    def isEmpty(self):
        return len(self.nodes) == 0

