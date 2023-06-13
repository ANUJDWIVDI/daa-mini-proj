from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

cities = ['India', 'USA', 'China', 'Australia', 'Brazil']
distances = [
    [0, 2000, 4000, 6000, 8000],
    [2000, 0, 1000, 3000, 5000],
    [4000, 1000, 0, 2000, 4000],
    [6000, 3000, 2000, 0, 1000],
    [8000, 5000, 4000, 1000, 0]
]

# Update distances to prefer going through intermediate cities
for i in range(len(distances)):
    for j in range(len(distances[i])):
        for k in range(len(distances)):
            if distances[i][j] > distances[i][k] + distances[k][j]:
                distances[i][j] = distances[i][k] + distances[k][j]

@app.route('/')
def index():
    num_cities = len(cities)
    return render_template('index.html', cities=cities, distances=distances, num_cities=num_cities)


@app.route('/calculate_path', methods=['POST'])
def calculate_path():
    start_country = request.json['start_country']
    end_country = request.json['end_country']

    start_index = cities.index(start_country)
    end_index = cities.index(end_country)

    result = find_path(start_index, end_index)
    return jsonify(result)


def find_path(start, end):
    num_cities = len(cities)
    visited = [False] * num_cities
    path = []
    min_cost = float('inf')
    path_details = []

    def backtrack(curr, cost):
        nonlocal min_cost

        if curr == end:
            if cost < min_cost:
                min_cost = cost
                path_details.clear()
                for i in range(len(path) - 1):
                    path_details.append({
                        'start': cities[path[i]],
                        'end': cities[path[i + 1]],
                        'cost': distances[path[i]][path[i + 1]]
                    })

        for i in range(num_cities):
            if not visited[i] and distances[curr][i] != 0:
                visited[i] = True
                path.append(i)
                backtrack(i, cost + distances[curr][i])
                visited[i] = False
                path.pop()

    visited[start] = True
    path.append(start)
    backtrack(start, 0)

    route = ' -> '.join([cities[i] for i in path])
    return {'route': route, 'min_cost': min_cost, 'path_details': path_details}


if __name__ == '__main__':
    app.run(debug=True)
