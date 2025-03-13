import React, { useState } from "react";
import "./App.css";

function App() {
  const [states, setStates] = useState("");
  const [transitions, setTransitions] = useState("");
  const [startState, setStartState] = useState("");
  const [acceptStates, setAcceptStates] = useState("");
  const [inputString, setInputString] = useState("");
  const [imageUrl, setImageUrl] = useState(null);
  const [result, setResult] = useState(null);

  const handleVisualize = async () => {
    const response = await fetch("http://127.0.0.1:5000/process_automata", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ states, transitions }),
    });

    const data = await response.json();
    setImageUrl(data.image_url);
  };

  const handleSimulate = async () => {
    const response = await fetch("http://127.0.0.1:5000/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ states, transitions, start_state: startState, accept_states: acceptStates, input_string: inputString }),
    });

    const data = await response.json();
    setResult(data.accepted ? "Accepted ✅" : "Rejected ❌");
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1>Finite Automata Simulator</h1>

      <textarea placeholder="Enter states (comma separated)" value={states} onChange={(e) => setStates(e.target.value)} />
      <textarea placeholder="Enter transitions (e.g., q0->a,q1)" value={transitions} onChange={(e) => setTransitions(e.target.value)} />
      <input type="text" placeholder="Start state" value={startState} onChange={(e) => setStartState(e.target.value)} />
      <input type="text" placeholder="Accept states (comma separated)" value={acceptStates} onChange={(e) => setAcceptStates(e.target.value)} />
      <input type="text" placeholder="Input string" value={inputString} onChange={(e) => setInputString(e.target.value)} />

      <button onClick={handleVisualize}>Visualize Automaton</button>
      <button onClick={handleSimulate}>Simulate Input</button>

      {imageUrl && <div><h3>Graph:</h3><img src={imageUrl} alt="Automata" /></div>}
      {result && <h3>Result: {result}</h3>}
    </div>
  );
}

export default App;