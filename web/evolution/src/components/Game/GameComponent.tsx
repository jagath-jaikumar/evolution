import { useContext, useEffect } from "react";
import GameContext from "../../context/GameContext";
import StartGameButton from "./StartGameButton";
import UserContext from "../../context/UserContext";

export default function GameComponent() {
  const { game, setGame } = useContext(GameContext);
  const { userId, setUserId } = useContext(UserContext);
  
  useEffect(() => {
    if (!game) return;

    const pollGame = async () => {
      try {
        const response = await fetch(`/api/observe/game?game_id=${game.id}`);
        const data = await response.json();
        setGame(data);
      } catch (error) {
        console.error("Failed to poll game:", error);
      }
    };

    const interval = setInterval(pollGame, 3000);

    return () => clearInterval(interval);
  }, [game, setGame]);

  if (!game) {
    return <div>No game selected</div>;
  }

  return (
    <div>
      {!game.started && game.created_by === userId && (
        <div>
          <StartGameButton gameId={game.id} />
        </div>
      )}
      <h2>Game Details</h2>
      <p>ID: {game.id}</p>
      <p>Players: {game.players.join(", ")}</p>
      <p>Epoch: {game.epoch}</p>
      <p>Created by: {game.created_by}</p>
      <p>
        Status:{" "}
        {game.ended
          ? "Ended"
          : game.started
            ? "In Progress"
            : "Waiting to Start"}
      </p>
    </div>
  );
}
