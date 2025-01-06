import { useState } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

interface NewGameButtonProps {
  onGameCreated?: () => void;
}

export default function NewGameButton({ onGameCreated }: NewGameButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleNewGame = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // First create the new game and get the ID
      const userId = sessionStorage.getItem("userId");
      const response = await axios.post("/api/setup/new/");
      const gameId = response.data.id;

      // Only attempt to join if we have a valid game ID
      if (!gameId) {
        throw new Error("Failed to get game ID from create response");
      }

      // Join the newly created game
      const joinResponse = await axios.post("/api/setup/join", {
        game_id: gameId,
        user_id: userId,
      });

      // Call the onGameCreated callback if provided
      if (onGameCreated) {
        onGameCreated();
      }
    } catch (error: any) {
      console.error("Failed to create new game:", error);
      setError(error.response?.data?.error || "Failed to create or join game");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <Button
        variant="contained"
        color="primary"
        onClick={handleNewGame}
        disabled={isLoading}
        sx={{
          textTransform: "none",
          "&:hover": {
            transform: "scale(1.05)",
            transition: "transform 0.2s",
          },
        }}
      >
        {isLoading ? "Creating..." : "New Game"}
      </Button>
      {error && (
        <Typography color="error" variant="body2" sx={{ mt: 1 }}>
          {error}
        </Typography>
      )}
    </Box>
  );
}
