import heapq

from Assets.data import totalGameStatus as s


def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def main(start:tuple, targetID:list, positiveID:list):
    grid = s.Dungeon[s.Dy][s.Dx]['room']

    openList = []
    heapq.heappush(openList, (0, start))
    
    cameFrom  = {}
    costSoFar = {}
    
    cameFrom [start] = None
    costSoFar[start] = 0
    
    while openList:
        _, curr = heapq.heappop(openList)
        
        if grid[curr[0]][curr[1]]['id'] in targetID:
            path = []
            while curr:
                path.append(curr)
                curr = cameFrom[curr]
            path.reverse()

            return path[1] if len(path)>1 else start
        
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nextNode = (curr[0] + dx, curr[1] + dy)

            if  (0 <= nextNode[0] < len(grid) and 0 <= nextNode[1] < len(grid[0]))\
            and (grid[nextNode[0]][nextNode[1]]['id'] in positiveID+targetID or nextNode==start):
                newCost = costSoFar[curr]+1

                if nextNode not in costSoFar or newCost<costSoFar[nextNode]:
                    costSoFar[nextNode] = newCost
                    priority            = newCost+heuristic(start, nextNode)

                    heapq.heappush(openList, (priority, nextNode))
                    cameFrom[nextNode] = curr
    
    return None

def forTag(start:tuple, tag:str, positiveID:list):
    grid = s.Dungeon[s.Dy][s.Dx]['room']

    openList = []
    heapq.heappush(openList, (0, start))
    
    cameFrom  = {}
    costSoFar = {}
    
    cameFrom [start] = None
    costSoFar[start] = 0
    
    while openList:
        _, curr = heapq.heappop(openList)

        if  grid[curr[0]][curr[1]]['type']=='entity'\
        and grid[curr[0]][curr[1]]['tag'] ==tag:
            path = []
            while curr:
                path.append(curr)
                curr = cameFrom[curr]
            path.reverse()

            return path[1] if len(path)>1 else start
        
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nextNode = (curr[0]+dx, curr[1]+dy)
            
            if (0<=nextNode[0]<len(grid) and 0<=nextNode[1]<len(grid[0]))\
            and (grid[nextNode[0]][nextNode[1]]['id'] in positiveID\
                or (
                    grid[nextNode[0]][nextNode[1]]['type']   =='entity'
                    and nextNode                             !=(s.y,s.x)
                    and grid[nextNode[0]][nextNode[1]]['tag']==tag
                )\
                or nextNode == start
            ):
                newCost = costSoFar[curr] + 1

                if nextNode not in costSoFar\
                or newCost < costSoFar[nextNode]:
                    costSoFar[nextNode] = newCost
                    priority            = newCost+heuristic(start, nextNode)

                    heapq.heappush(openList, (priority, nextNode))
                    cameFrom[nextNode] = curr
    
    return None