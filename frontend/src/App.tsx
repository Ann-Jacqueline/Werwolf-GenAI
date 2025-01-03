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
    const [currentPhaseId, setCurrentPhaseId] = useState<number | null>(null);
    const [currentLog, setCurrentLog] = useState('');

    useEffect(() => {
        axios
            .get('http://127.0.0.1:5000/api/data')
            .then((response) => {
                console.log('Nachricht vom Backend', response.data.message);
            })
            .catch((error) => {
                console.error('Fehler beim Abrufen der Daten:', error);
            });
    }, []);

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

     // Fetch logs periodically


    useEffect(() => {
        const interval = setInterval(() => {
            axios.get('http://127.0.0.1:5000/api/log')
                .then(response => {
                    setCurrentLog(response.data.relevant_log || "No relevant logs.");
                })
                .catch(error => console.error("Error fetching logs:", error));
        }, 5000); // Update every 5 seconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate active game and phase
    if (!currentGameId) {
        alert('No active game. Please start a game first.');
        return;
    }
    if (!currentPhaseId) {
        alert('No active phase. Please start a phase first.');
        return;
    }

    try {
        // Send prompt to the backend
        const { data } = await axios.post('http://127.0.0.1:5000/api/data', {
            game_id: currentGameId,
            phase_id: currentPhaseId,
            prompt: userInput,
            response: '', // Placeholder for backend-generated response
        });

        // Update response state or notify if no response
        setResponse(data.response || 'No response from the backend.');
    } catch (error) {
        console.error('Error sending prompt:', error);
        setResponse('Failed to send the prompt. Please try again.');
    }
};

const startGame = async () => {
    try {
        const humanPlayers = 1; // Fixed number of human players
        const totalPlayers = playerCount; // User input for the total number of players
        const aiPlayers = totalPlayers - humanPlayers; // Calculate the number of AI players

        // Send the total number of players (human + AI) to the backend
        const response = await axios.post('http://127.0.0.1:5000/api/start_game', {
            human_players: humanPlayers,
            total_players: totalPlayers,
        });

        setCurrentGameId(response.data.game_id);
        alert(`Game started! ID: ${response.data.game_id}, AI Players: ${aiPlayers}`);
    } catch (error) {
        console.error('Error starting the game:', error);
        alert('Failed to start the game.');
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
            setCurrentPhaseId(null);
        } catch (error) {
            console.error('Error ending the game:', error);
            alert('Failed to end the game.');
        }
    };

    const exportGameData = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/export');
            alert(response.data.message);
        } catch (error) {
            console.error('Error exporting game data:', error);
            alert('Failed to export game data.');
        }
    };

    return (
        <div className="app-container">
            <div className="background">{bubbles}</div>

            <div className="content">
                <h1 className="title">Enter the Magical Forest</h1>

                <div className="game-controls">
                    <button onClick={startGame} className="button">
                        Start Game
                    </button>
                    <button onClick={endGame} className="button" disabled={!currentGameId}>
                        End Game
                    </button>
                    <button onClick={exportGameData} className="button">
                        Export Data
                    </button>
                </div>

                <p className="game-status">
                    {currentGameId
                        ? `Active Game ID: ${currentGameId}`
                        : 'No active game.'}
                </p>

                <div className="log-container">
                    <h2 className="log-title">Relevant Log</h2>
                    <p className="log-message">{currentLog}</p>
                </div>


                <form onSubmit={handleSubmit} className="form">
                    <label className="label">
                        Number of Players
                        <input
                            type="number"
                            min="7"
                            max="20"
                            value={playerCount}
                            onChange={(e) => setPlayerCount(parseInt(e.target.value, 10))}
                            className="input"
                        />
                    </label>
                    <label className="label">
                        Your Message
                        <textarea
                            value={userInput}
                            onChange={(e) => setUserInput(e.target.value)}
                            className="input input-animated"
                            placeholder="Type your message here..."
                        ></textarea>
                    </label>
                    <button type="submit" className="button">
                        Send Message
                    </button>
                </form>

                <div className="response-container">
                    <h2 className="response-title">Response from Backend</h2>
                    <p className="response-message">{response || 'Waiting for a response ...'}</p>
                </div>
            </div>
        </div>
    );
}

export default App;