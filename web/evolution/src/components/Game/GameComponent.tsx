import { useContext, useEffect, useState } from "react";
import GameContext from "../../context/GameContext";
import StartGameButton from "./StartGameButton";
import UserContext from "../../context/UserContext";
import HandTray from "./components/HandTray";
import { Box, Typography } from "@mui/material";

interface PreGameProps {
  game: any;
  userId: string;
}

const PreGameComponent: React.FC<PreGameProps> = ({ game, userId }) => {
  if (game.started || game.created_by !== userId) return null;

  return (
    <Box>
      <Typography variant="h4">Game Details</Typography>
      <Typography>Join Code: {game.id}</Typography>
      <Typography>Player Count: {game.players.length}</Typography>
      <Typography>
        Status: {game.ended ? "Ended" : game.started ? "In Progress" : "Waiting to Start"}
      </Typography>
      <StartGameButton gameId={game.id} />
    </Box>
  );
};

interface MainGameProps {
  game: any;
}

const MainGameComponent: React.FC<MainGameProps> = ({ game }) => {
  const [showHandTray, setShowHandTray] = useState(false);

  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      const { clientY } = event;
      const windowHeight = window.innerHeight;
      const threshold = 100; // Distance from the bottom to trigger tray visibility

      if (windowHeight - clientY < threshold) {
        setShowHandTray(true);
      } else {
        setShowHandTray(false);
      }
    };

    window.addEventListener("mousemove", handleMouseMove);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <Box>
      <HandTray game={game} visible={showHandTray} />
    </Box>
  );
};

export default function GameComponent() {
  const { game, setGame } = useContext(GameContext);
  const { userId } = useContext(UserContext);

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
    return <Typography>No game selected</Typography>;
  }

  return (
    <Box>
      {!game.started ? (
        <PreGameComponent game={game} userId={userId} />
      ) : (
        <MainGameComponent game={game} />
      )}
    </Box>
  );
}