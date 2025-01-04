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
    const [isGameRunning, setIsGameRunning] = useState(false); // Neuer State

    // Fetch logs periodically
    useEffect(() => {
        const interval = setInterval(() => {
            axios
                .get('http://127.0.0.1:5000/api/log')
                .then((response) => {
                    console.log("Logs fetched:", response.data.console_output);
                    setConsoleOutput(response.data.console_output || []);
                })
                .catch((error) => console.error('Error fetching logs:', error));
        }, 2000); // Alle 5 Sekunden abrufen

        return () => clearInterval(interval); // Cleanup
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // Validate active game
        if (!currentGameId) {
            alert('No active game. Please start a game first.');
            return;
        }

        try {
            const { data } = await axios.post('http://127.0.0.1:5000/api/data', {
                game_id: currentGameId,
                prompt: userInput,
                response: '', // Placeholder
            });

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

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/start_game', {
                human_players: 1, // Fixed number of human players
                total_players: playerCount,
            });

            setCurrentGameId(response.data.game_id);
            setIsGameRunning(true);
            alert(`Game started! ID: ${response.data.game_id}`);
        } catch (error: unknown) {
            if(axios.isAxiosError(error))
            if (error.response && error.response.data.error) {
                alert(error.response.data.error);
            } else {
                alert('Failed to start the game.');
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
            if(axios.isAxiosError(error))
            if (error.response && error.response.data.error) {
                alert(error.response.data.error);
            } else {
                alert('Failed to end the game.');
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

    // Bubble animation (unchanged)
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
                <h1 className="title">Enter the Magical Forest</h1>

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
                    {currentGameId
                        ? `Active Game ID: ${currentGameId}`
                        : 'No active game.'}
                </p>

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
                    <h2 className="response-title">Backend Response</h2>
                    <p>{response || 'Waiting for a response...'}</p>
                </div>

                <div className="console-container">
                    <h2 className="console-title">Console Output</h2>
                    <ul>
                        {consoleOutput.map((log, index) => (
                            <li key={index}>{log}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default App;
