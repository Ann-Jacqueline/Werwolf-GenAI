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

    useEffect(() => {
        axios
            .get('http://127.0.0.1:5000/api/data')
            .then((response) => {
                console.log('Nachricht vom BE', response.data.message);
            })
            .catch((error) => {
                console.error('Fehler beim Abrufen der Daten:', error);
            });
    }, []);

    useEffect(() => {
        // Generiere Bläschen nur einmal beim Laden der Komponente
        const colors = ['bubble-green', 'bubble-beige', 'bubble-pink', 'bubble-purple'];
        const sizes = ['bubble-small', 'bubble-medium', 'bubble-large'];

        const generatedBubbles = [...Array(30)].map((_, i) => {
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            const randomSize = sizes[Math.floor(Math.random() * sizes.length)];
            const randomX = Math.random() * 100; // Positionierung in Prozent
            const randomY = Math.random() * 100;
            const randomDelay = Math.random() * 5; // Zufällige Verzögerung (Sekunden)

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
    }, []); // Leer, damit es nur einmal ausgeführt wird

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const maxPlayers = 8;

        if (playerCount > maxPlayers) {
            setResponse(`Maximale Spieler*innenanzahl von ${maxPlayers} überschritten`);
            return;
        }

        const agentsToAdd = maxPlayers - playerCount;

        const message = `${playerCount} Spieler treten bei. Bitte generiere ${agentsToAdd} zusätzliche Agent*innen, um die Gruppe auf ${maxPlayers} zu füllen.`;

        // Nachricht ans Backend
        try {
            const res = await axios.post('http://127.0.0.1:5000/api/data', {
                prompt: message,
            });
            setResponse(res.data.response || 'Keine Antwort vom Backend');
        } catch (error) {
            console.error('Fehler beim Senden der Anfrage', error);
            setResponse('Fehler beim Senden der Anfrage');
        }
    };

    // Spiel starten
    const startGame = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/start_game');
            setCurrentGameId(response.data.game_round_id);
            alert(`Spiel gestartet! ID: ${response.data.game_round_id}`);
        } catch (error) {
            console.error('Fehler beim Starten des Spiels:', error);
            alert('Fehler beim Starten des Spiels.');
        }
    };

    // Spiel beenden
    const endGame = async () => {
        if (!currentGameId) {
            alert('Kein aktives Spiel zum Beenden.');
            return;
        }

        try {
            await axios.post('http://127.0.0.1:5000/api/end_game', {
                game_round_id: currentGameId,
            });
            alert(`Spielrunde ${currentGameId} beendet!`);
            setCurrentGameId(null); // Spielrunde zurücksetzen
        } catch (error) {
            console.error('Fehler beim Beenden des Spiels:', error);
            alert('Fehler beim Beenden des Spiels.');
        }
    };

    return (
        <div className="app-container">
            {/* Hintergrundanimation */}
            <div className="background">{bubbles}</div>

            {/* Hauptinhalt */}
            <div className="content">
                <h1 className="title">Enter the Magical Forest</h1>

                {/* Spiel-Buttons */}
                <div className="game-controls">
                    <button onClick={startGame} className="button">
                        Spiel Start
                    </button>
                    <button
                        onClick={endGame}
                        className="button"
                        disabled={!currentGameId}
                    >
                        Spiel Ende
                    </button>
                </div>

                {/* Anzeige der aktuellen Spielrunde */}
                <p className="game-status">
                    {currentGameId
                        ? `Aktive Spielrunde: ${currentGameId}`
                        : 'Kein aktives Spiel.'}
                </p>

                {/* Spieleranzahl und Nachricht */}
                <form onSubmit={handleSubmit} className="form">
                    <label className="label">
                        Number of Players
                        <input
                            type="number"
                            min="1"
                            max="8"
                            value={playerCount}
                            onChange={(e) => setPlayerCount(parseInt(e.target.value, 9))}
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

                {/* Antwortfeld */}
                <div className="response-container">
                    <h2 className="response-title">Response from Backend</h2>
                    <p className="response-message">{response || 'Waiting for a response ...'}</p>
                </div>
            </div>
        </div>
    );
}

export default App;
