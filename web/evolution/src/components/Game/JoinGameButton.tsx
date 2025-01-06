import { useState } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";

interface JoinGameButtonProps {
  onModalOpen: () => void;
  onModalClose: () => void;
}

export default function JoinGameButton({
  onModalOpen,
  onModalClose,
}: JoinGameButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [gameId, setGameId] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleClickOpen = () => {
    setOpen(true);
    setError(null);
    onModalOpen();
  };

  const handleClose = () => {
    setOpen(false);
    setGameId("");
    setError(null);
    onModalClose();
  };

  const handleJoinGame = async () => {
    if (!gameId.trim()) {
      setError("Please enter a game ID");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const userId = sessionStorage.getItem("userId");
      const response = await axios.post("/api/setup/join", {
        game_id: gameId,
        user_id: userId,
      });
      handleClose();
    } catch (error) {
      console.error("Failed to join game:", error);
      if (axios.isAxiosError(error)) {
        setError(
          error.response?.data?.message ||
            "Failed to join game. Please try again.",
        );
      } else {
        setError("An unexpected error occurred");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Button
        variant="outlined"
        color="primary"
        onClick={handleClickOpen}
        disabled={isLoading}
        sx={{
          textTransform: "none",
          "&:hover": {
            transform: "scale(1.05)",
            transition: "transform 0.2s",
          },
        }}
      >
        Join Game
      </Button>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Join Game</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            id="gameId"
            label="Game ID"
            type="text"
            fullWidth
            variant="outlined"
            value={gameId}
            onChange={(e) => setGameId(e.target.value)}
            error={!!error}
          />
          {error && (
            <Typography color="error" variant="body2" sx={{ mt: 1 }}>
              {error}
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleJoinGame} disabled={isLoading}>
            {isLoading ? "Joining..." : "Join"}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
