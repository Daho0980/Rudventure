import heapq

from Assets.data import totalGameStatus as s


def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def main(start, targetID, positiveID):
    grid = s.Dungeon[s.Dy][s.Dx]['room']

    openList = []
    heapq.heappush(openList, (0, start))
    
    cameFrom  = {}
    costSoFar = {}
    
    cameFrom[start]  = None
    costSoFar[start] = 0
    
    while openList:
        _, current = heapq.heappop(openList)
        
        if grid[current[0]][current[1]]['id'] in targetID:
            path = []
            while current:
                path.append(current)
                current = cameFrom[current]
            path.reverse()
            return path[1] if len(path)>1 else start
        
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nextNode = (current[0] + dx, current[1] + dy)

            if  (0 <= nextNode[0] < len(grid) and 0 <= nextNode[1] < len(grid[0]))\
            and (grid[nextNode[0]][nextNode[1]]['id'] in positiveID+targetID or nextNode==start):
                newCost = costSoFar[current]+1

                if nextNode not in costSoFar or newCost < costSoFar[nextNode]:
                    costSoFar[nextNode] = newCost
                    priority            = newCost+heuristic(start, nextNode)

                    heapq.heappush(openList, (priority, nextNode))
                    cameFrom[nextNode] = current
    
    return None

import heapq

def forHashKey(start, hashKey, positiveID):
    grid = s.Dungeon[s.Dy][s.Dx]['room']

    openList = []
    heapq.heappush(openList, (0, start))
    
    cameFrom  = {}
    costSoFar = {}
    
    cameFrom[start]  = None
    costSoFar[start] = 0
    
    while openList:
        _, current = heapq.heappop(openList)

        if grid[current[0]][current[1]]['type']==1 and grid[current[0]][current[1]]['hashKey']==hashKey:
            path = []
            while current:
                path.append(current)
                current = cameFrom[current]
            path.reverse()
            return path[1] if len(path)>1 else start
        
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nextNode = (current[0]+dx, current[1]+dy)
            
            if (0 <= nextNode[0] < len(grid) and 0 <= nextNode[1] < len(grid[0]))\
               and (grid[nextNode[0]][nextNode[1]]['id'] in positiveID\
                    or (
                            grid[nextNode[0]][nextNode[1]]['type']       ==1
                            and nextNode                                 !=(s.y,s.x)
                            and grid[nextNode[0]][nextNode[1]]['hashKey']==hashKey
                        )\
                    or nextNode == start
                ):
                newCost = costSoFar[current] + 1

                if nextNode not in costSoFar\
                or newCost < costSoFar[nextNode]:
                    costSoFar[nextNode] = newCost
                    priority            = newCost+heuristic(start, nextNode)

                    heapq.heappush(openList, (priority, nextNode))
                    cameFrom[nextNode] = current
    
    return None