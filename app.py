from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Flight routes and distances
adjacency_matrix = [
    [0, 5, 2, float('inf'), float('inf')],
    [5, 0, float('inf'), 1, 6],
    [2, float('inf'), 0, 3, float('inf')],
    [float('inf'), 1, 3, 0, 2],
    [float('inf'), 6, float('inf'), 2, 0]
]

airport_names = ['A', 'B', 'C', 'D', 'E']


def find_shortest_routes(adjacency_matrix):
    n = len(adjacency_matrix)
    shortest_distances = [[0] * n for _ in range(n)]
    next_hops = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            shortest_distances[i][j] = adjacency_matrix[i][j]
            if adjacency_matrix[i][j] != float('inf'):
                next_hops[i][j] = j

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if shortest_distances[i][j] > shortest_distances[i][k] + shortest_distances[k][j]:
                    shortest_distances[i][j] = shortest_distances[i][k] + shortest_distances[k][j]
                    next_hops[i][j] = next_hops[i][k]

    return shortest_distances, next_hops


def reconstruct_route(next_hops, source_index, destination_index):
    if next_hops[source_index][destination_index] == 0:
        return []

    route = [source_index]
    while source_index != destination_index:
        source_index = next_hops[source_index][destination_index]
        route.append(source_index)

    return route


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate_path', methods=['POST'])
def calculate_path():
    data = request.get_json()
    start_city = data['start_city']
    end_city = data['end_city']

    source_index = ord(start_city.upper()) - ord('A')
    destination_index = ord(end_city.upper()) - ord('A')

    if source_index < 0 or source_index >= len(adjacency_matrix) or destination_index < 0 or destination_index >= len(
            adjacency_matrix):
        response_data = {
            'error': 'Invalid airport selection. Please try again.'
        }
        return jsonify(response_data)

    shortest_distances, next_hops = find_shortest_routes(adjacency_matrix)
    shortest_route = reconstruct_route(next_hops, source_index, destination_index)

    if not shortest_route:
        response_data = {
            'error': 'No route available between the selected airports.'
        }
        return jsonify(response_data)

    route = ' -> '.join(airport_names[airport_index] for airport_index in shortest_route)
    min_cost = shortest_distances[source_index][destination_index]

    response_data = {
        'route': route,
        'min_cost': min_cost
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
