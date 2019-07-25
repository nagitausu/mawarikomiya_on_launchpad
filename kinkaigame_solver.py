def solve(field, machines):
    machine_num = len(machines)
    memo = dict()

    def dfs(x0, x1, y0, y1):
        index = str(x0)+"_"+str(x1)+"_"+str(y0)+"_"+str(y1)
        if index in memo:
            return memo[index]
        ret = 0
        for x, y in machines:
            val = 0
            if x0 <= x and x < x1 and y0 <= y and y < y1:
                val += dfs(x0, x, y0, y)
                val += dfs(x+1, x1, y+1, y1)
                val += dfs(x0, x, y+1, y1)
                val += dfs(x+1, x1, y0, y)
                val += (x1 - x0) + (y1 - y0) - 1
            ret = max(ret, val)
        memo[index] = ret
        return ret

    return dfs(0, len(field), 0, len(field[0]))

if __name__ == "__main__":
    field = [[1] * 6 for _ in range(4)]
    machines = [[0,1], [1,3], [3,2]]
    print(solve(field, machines) - len(machines))