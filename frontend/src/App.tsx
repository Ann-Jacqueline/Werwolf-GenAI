import React, { useState, useEffect } from 'react';
import './App.css';
import './animations.css';
import axios from 'axios';

function App() {
    const [playerCount, setPlayerCount] = useState(1);
    const [userInput, setUserInput] = useState('');
    const [response, setResponse] = useState('');
    const [bubbles, setBubbles] = useState<JSX.Element[]>([]);
    const [currentGameId, setCurrentGameId] = useState<number | null>(null);
    const [consoleOutput, setConsoleOutput] = useState<string[]>([]);
    const [isGameRunning, setIsGameRunning] = useState(false);
    const [humanPlayer, setHumanPlayer] = useState('');

    // Fetch logs periodically
    useEffect(() => {
        const interval = setInterval(() => {
            axios
                .get('http://127.0.0.1:5000/api/live_log')
                .then((response) => {
                    setConsoleOutput(response.data.logs || []);
                })
                .catch((error) => console.error('Error fetching logs:', error));
        }, 5000); // Every 5 seconds

        return () => clearInterval(interval); // Cleanup
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate active game
    if (!currentGameId) {
        alert('No active game. Please start a game first.');
        return;
    }

    // Beispiel für phase_id - hier dynamisch oder festgelegt:
    const currentPhaseId = "example_phase_id"; // Ersetzen durch den tatsächlichen Wert
    const currentPlayerId = "Human"; // Annahme, dass der Human-Player immer "Human" ist

    try {
        const { data } = await axios.post('http://127.0.0.1:5000/api/data', {
            game_id: currentGameId,   // Spiel-ID
            phase_id: currentPhaseId, // Phase-ID
            player_id: currentPlayerId, // Spieler-ID
            prompt: userInput,       // Eingabefeld
            response: '',            // Antwort - aktuell leer
        });

        // Setze die Antwort des Backends
        setResponse(data.response || 'No response from the backend.');
    } catch (error) {
        console.error('Error sending prompt:', error);
        setResponse('Failed to send the prompt. Please try again.');
    }
};


    const startGame = async () => {
    if (isGameRunning) {
        alert('Game is already running. End the current game to start a new one.');
        return;
    }

    if (!humanPlayer.trim()) {
        alert('Please provide your name to start the game.');
        return;
    }

    if (playerCount < 7) {
        alert('You must have at least 7 players to start the game.');
        return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/api/start_game', {
            human_players: 1,           // Anzahl der menschlichen Spieler
            total_players: playerCount, // Gesamte Spieleranzahl
            human_name: humanPlayer,    // Name des Human-Players
        });

        setCurrentGameId(response.data.game_id);
        setIsGameRunning(true);
        alert(`Game started! Welcome, ${humanPlayer}!`);
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            if (error.response && error.response.data.error) {
                alert(error.response.data.error);
            } else {
                alert('Failed to start the game.');
            }
        }
    }
};


    const endGame = async () => {
        if (!currentGameId) {
            alert('No active game to end.');
            return;
        }

        try {
            await axios.post('http://127.0.0.1:5000/api/end_game', {
                game_id: currentGameId,
            });

            alert(`Game ${currentGameId} ended!`);
            setCurrentGameId(null);
            setIsGameRunning(false);
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                if (error.response && error.response.data.error) {
                    alert(error.response.data.error);
                } else {
                    alert('Failed to end the game.');
                }
            }
        }
    };

    const exportGameData = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/export');
            alert(response.data.message);
        } catch {
            alert('Failed to export game data.');
        }
    };

    // Bubble animation
    useEffect(() => {
        const colors = ['bubble-green', 'bubble-beige', 'bubble-pink', 'bubble-purple'];
        const sizes = ['bubble-small', 'bubble-medium', 'bubble-large'];

        const generatedBubbles = [...Array(30)].map((_, i) => {
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            const randomSize = sizes[Math.floor(Math.random() * sizes.length)];
            const randomX = Math.random() * 100;
            const randomY = Math.random() * 100;
            const randomDelay = Math.random() * 5;

            return (
                <div
                    key={i}
                    className={`bubble ${randomColor} ${randomSize}`}
                    style={{
                        left: `${randomX}%`,
                        top: `${randomY}%`,
                        animationDelay: `${randomDelay}s`,
                    }}
                ></div>
            );
        });

        setBubbles(generatedBubbles);
    }, []);

   return (
    <div className="app-container">
        <div className="background">{bubbles}</div>
        <div className="content">
            <h1 className="title">Welcome to WerwolfIQ</h1>


            <div className="game-controls">
                <button onClick={startGame} className="button" disabled={isGameRunning}>
                    Start Game
                </button>
                <button onClick={endGame} className="button" disabled={!isGameRunning}>
                    End Game
                </button>
                <button onClick={exportGameData} className="button">
                    Export Data
                </button>
            </div>

            <p className="game-status">
                {currentGameId ? `Active Game ID: ${currentGameId}` : "No active game."}
            </p>

            {/* Eingabefelder und Response-Container */}
            <div className="form-container">
                {/* Linker Bereich: Eingabefelder */}
                <form onSubmit={handleSubmit} className="input-group">
                    <label className="label" htmlFor="players">
                        Number of Players
                    </label>
                    <input
                        type="number"
                        id="players"
                        min="7"
                        max="20"
                        value={playerCount}
                        onChange={(e) => setPlayerCount(parseInt(e.target.value, 10))}
                        className="input"
                    />

                    <label className="label" htmlFor="name">
                        Your Name:
                    </label>
                    <input
                        type="text"
                        id="name"
                        value={humanPlayer}
                        onChange={(e) => setHumanPlayer(e.target.value)}
                        className="input"
                        placeholder="Enter your name..."
                    />

                    <label className="label" htmlFor="message">
                        Your Message:
                    </label>
                    <textarea
                        id="message"
                        value={userInput}
                        onChange={(e) => setUserInput(e.target.value)}
                        className="input"
                        placeholder="Type your message here..."
                    ></textarea>
                </form>

                {/* Rechter Bereich: Response-Container */}
                <div>
                    <div className="response-container">
                        <h2 className="response-title">Backend Response</h2>
                        <p>{response || "Waiting for a response..."}</p>
                    </div>
                    <button type="submit" className="button" onClick={handleSubmit}>
                        Send Message
                    </button>
                </div>
            </div>

            <div className="wolf-container">
                <img src="Wolf_image.jpeg" alt="Wolf Icon" className="wolf-image"/>
            </div>

            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet"/>

            {/* Konsolenausgabe */}
            <div className="console-container">
                <h2 className="console-title">Console Output</h2>
                {consoleOutput && consoleOutput.length > 0 ? (
                    <ul>
                        {consoleOutput.map((log, index) => (
                            <li key={index}>{log}</li>
                        ))}
                    </ul>
                ) : (
                    <p>No logs available.</p>
                )}
            </div>
        </div>
    </div>
   );

}

export default App;
