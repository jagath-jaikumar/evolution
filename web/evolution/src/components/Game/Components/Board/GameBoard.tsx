import { useContext, useEffect, useState } from "react";
import GameContext from "@/context/GameContext";
import { Box, Typography } from "@mui/material";
import StartGameButton from "@/components/Game/Components/Buttons/StartGameButton";
import { callApi } from "@/utils/callApi";
import { Game } from "@/types/types";

export default function GameBoard() {
  const { game, setGame } = useContext(GameContext);
  const [isPolling, setIsPolling] = useState(false);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const pollGame = async () => {
      if (!game?.id) return;

      try {
        const result = await callApi<Game>("get", `api/game/${game.id}/`);
        if (result.success && result.data) {
          setGame(result.data);
          
          // Start polling if game starts
          if (result.data.started && !isPolling) {
            setIsPolling(true);
          }
        }
      } catch (error) {
        console.error("Error polling game:", error);
      }
    };

    if (game?.id) {
      // Initial poll
      pollGame();

      // Set up polling interval
      intervalId = setInterval(pollGame, 3000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [game?.id, setGame, isPolling]);

  if (!game) {
    return null;
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        Game Details
      </Typography>

      <Typography variant="body1">Game ID: {game.id}</Typography>

      <Typography variant="body1">
        Created At: {new Date(game.created_at).toLocaleString()}
      </Typography>

      <Typography variant="body1">
        Status:{" "}
        {game.started ? (game.ended ? "Ended" : "In Progress") : "Not Started"}
      </Typography>

      <Typography variant="body1">
        Current Epoch: {game.current_epoch?.epoch_number || "N/A"}
      </Typography>

      {!game.started && game.created_by_this_user && (
        <Box sx={{ mt: 2 }}>
          <StartGameButton gameId={game.id} onGameStarted={() => setIsPolling(true)} />
        </Box>
      )}

      <Typography variant="h5" sx={{ mt: 2, mb: 1 }}>
        Players ({game.player_count})
      </Typography>

      {game.this_player && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="h6">Your Player</Typography>
          <Typography variant="body1">
            Score: {game.this_player.score}
          </Typography>
          <Typography variant="body1">
            Cards in Hand: {game.this_player.hand.length}
          </Typography>
          <Typography variant="body1">
            Animals: {game.this_player.animals.length}
          </Typography>
        </Box>
      )}

      {game.other_players.map((player, index) => (
        <Box key={index} sx={{ mb: 2 }}>
          <Typography variant="h6">Player {player.email}</Typography>
          <Typography variant="body1">Score: {player.score}</Typography>
          <Typography variant="body1">
            Animals: {player.animals.length}
          </Typography>
          <Typography variant="body1">
            Cards in Hand: {player.hand_count}
          </Typography>
        </Box>
      ))}
    </Box>
  );
}
