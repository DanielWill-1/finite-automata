from flask import send_file
from flask import Flask, request, jsonify
from flask_cors import CORS
import graphviz
import os


app = Flask(__name__)
CORS(app, resources={r"/get_graph": {"origins": "*"}}) # Allow frontend to communicate with the backend

@app.route('/process_automata', methods=['POST'])
def process_automata():
    data = request.json
    states = data.get("states", "").split(",")
    transitions = data.get("transitions", "").split("\n")
    dot = graphviz.Digraph(format="png")

    for state in states:
        dot.node(state.strip())
    
    for transition in transitions:
        parts = transition.split("->")
        if len(parts) == 2:
            start, rest = parts[0].strip(), parts[1].strip().split(",")
            symbol, end = rest[0], rest[1]
            dot.edge(start, end, label=symbol)

    filename = "static/automata"
    dot.render(filename, format="png", cleanup=True)
    return jsonify({"image_url": f"http://127.0.0.1:5000/{filename}"})

@app.route('/static/<path:filename>')
def serve_image(filename):
    return send_file(f"static/{filename}")

def simulate_automaton(states, transitions, start_state, accept_states, input_string):
    current_state = start_state
    for symbol in input_string:
        if (current_state, symbol) in transitions:
            current_state = transitions[(current_state, symbol)]
        else:
            return False  # No valid transition
    return current_state in accept_states

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    states = data["states"].split(",")
    transitions_raw = data["transitions"].split("\n")
    start_state = data["start_state"]
    accept_states = set(data["accept_states"].split(","))
    input_string = data["input_string"]

    transitions = {}
    for transition in transitions_raw:
        parts = transition.split("->")
        if len(parts) == 2:
            start, rest = parts[0].strip(), parts[1].strip().split(",")
            symbol, end = rest[0], rest[1]
            transitions[(start, symbol)] = end

    result = simulate_automaton(states, transitions, start_state, accept_states, input_string)

    return jsonify({"accepted": result})

@app.route("/get_graph", methods=["GET"])
def get_graph():
    return send_file("automata.png", mimetype="image/png")

if __name__ == '__main__':
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
