import dijkstra
MAX_N = 8

class Mawarikomiya():

    def __init__(self):
        self.field, self.edge = self.GetInitialField()
        self.dijk = dijkstra.Dijkstra(self.edge)
        self.pos = [7, 7]
        self.player_pos = [3, 3]
    
    def GetInitialField(self):
        field = [[0] * MAX_N for _ in range(MAX_N)] 
        edge = [[] for _ in range(MAX_N**2)]
        for i in range(MAX_N):
            for j in range(MAX_N):
                for dx, dy in [[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]]:
                    if i+dx < 0 or i+dx > 7 or j+dy < 0 or j+dy > 7:
                        continue
                    edge[i*8 + j].append((i+dx) * 8 + (j+dy))
        return field, edge

    def Move(self, pos):
        self.pos[0] = pos[0] 
        self.pos[1] = pos[1] 
    
    def CalcShortestPath(self, goal):
        start = self.pos[0]*8 + self.pos[1]
        goal = goal[0]*8 + goal[1]
        player = self.player_pos[0]*8 + self.player_pos[1]
        traj = self.dijk.calc(start, player, goal)
        self.dijk.reset()
        return traj

    def ReactPlayerMotion(self, new_player_pos):
        delta_pos = [new_player_pos[0] - self.player_pos[0], new_player_pos[1] - self.player_pos[1]]
        goal = [new_player_pos[0] + delta_pos[0], new_player_pos[1] + delta_pos[1]]
        self.player_pos[0] = new_player_pos[0]
        self.player_pos[1] = new_player_pos[1]

        traj = self.CalcShortestPath(goal)
        self.Move(goal)
        return traj

if __name__ == "__main__":
    MK = Mawarikomiya()
    traj = MK.ReactPlayerMotion([2,2])
    print(traj)
    traj = MK.ReactPlayerMotion([3,3])
    print(traj)