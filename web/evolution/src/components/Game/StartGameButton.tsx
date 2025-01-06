import { useState } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

interface StartGameButtonProps {
  gameId: string;
  onGameStarted?: () => void;
}

export default function StartGameButton({
  gameId,
  onGameStarted,
}: StartGameButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleStartGame = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post("/api/setup/start", {
        game_id: gameId,
      });

      if (onGameStarted) {
        onGameStarted();
      }
    } catch (error: any) {
      console.error("Failed to start game:", error);
      setError(error.response?.data?.error || "Failed to start game");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <Button
        variant="contained"
        color="primary"
        onClick={handleStartGame}
        disabled={isLoading}
        sx={{
          textTransform: "none",
          "&:hover": {
            transform: "scale(1.05)",
            transition: "transform 0.2s",
          },
        }}
      >
        {isLoading ? "Starting..." : "Start Game"}
      </Button>
      {error && (
        <Typography color="error" variant="body2" sx={{ mt: 1 }}>
          {error}
        </Typography>
      )}
    </Box>
  );
}
