def nelder_mead(points, n_iterations, n, delay, plot=False):
    def objective_function(point):
        import math
        x = point[0]
        y = point[1]
        f = math.exp(x) + (2 * math.exp(-x)) + (x * y) + y ** 2
        return f

    def fi_function(v, vp, parameter):
        fi = (((1 - parameter) * v[0]) + (parameter * vp[0]), ((1 - parameter) * v[1]) + (parameter * vp[1]))
        return fi

    def gravity(n, p, points):
        points.remove(p)
        v = (sum(x for x, y in points) / n, sum(y for x, y in points) / n)
        return v

    def order_points(points):
        solution = []
        for coord in points:
            solution.append(objective_function(coord))
        vm, fm = points[solution.index(min(solution))], solution[solution.index(min(solution))]
        vp, fp = points[solution.index(max(solution))], solution[solution.index(max(solution))]
        vi = [coord for coord in points if coord not in [vm, vp]][0]
        fi = objective_function(vi)
        return vm, vp, vi, fm, fp, fi

    def plot_triangle(points, delay):
        import matplotlib.pyplot as plt
        import time
        plt.rcParams["figure.autolayout"] = True
        x_values = [point[0] for point in points]
        x_values.append(x_values[0])
        y_values = [point[1] for point in points]
        y_values.append(y_values[0])
        plt.plot(x_values, y_values, 'bo', linestyle="--")
        plt.xlim([-6, 6])
        plt.ylim([-6, 6])
        plt.show()
        time.sleep(delay)

    if plot:
        plot_triangle(points, delay)
    for i in range(n_iterations):
        vm, vp, vi, fm, fp, fi = order_points(points)
        v = gravity(n, vp, points=[vi, vp, vm])
        r = fi_function(v, vp, parameter=-1)
        fr = objective_function(r)

        if fr < fm:
            e = fi_function(v, vp, parameter=-2)
            fe = objective_function(e)
            if fe < fm:
                vp = e
                fp = fe
            else:
                vp = r
                fp = fr

        elif fm <= fr < fp:
            vp = r
            fp = fr

        else:
            c = fi_function(v, vp, parameter=1/2)
            fc = objective_function(c)
            if fc < fp:
                vp = c
                fp = fc
            else:
                vi = fi_function(vm, vi, parameter=1/2)
                fi = objective_function(vi)
                vp = fi_function(vm, vp, parameter=1/2)
                fp = objective_function(vp)
        points = [vm, vp, vi]
        if plot:
            plot_triangle(points, delay)
    f = [objective_function(point) for point in points]
    return points, f

v0 = (0, 0)
v1 = (5, 0)
v2 = (0, 5)

delay = 0.25     #time sleep between plots

points = [v0, v1, v2]

n_iterations = 10
n = 2


points, f = nelder_mead(points, n_iterations, n, delay, plot=True)


print(f"points = {points}, with objective functions {f}, respectively")