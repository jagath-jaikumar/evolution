import { useState } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";

interface JoinGameButtonProps {
  onModalOpen: () => void;
  onModalClose: () => void;
}

export default function JoinGameButton({ onModalOpen, onModalClose }: JoinGameButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [gameId, setGameId] = useState("");

  const handleClickOpen = () => {
    setOpen(true);
    onModalOpen();
  };

  const handleClose = () => {
    setOpen(false);
    setGameId("");
    onModalClose();
  };

  const handleJoinGame = async () => {
    if (!gameId.trim()) return;

    setIsLoading(true);
    try {
      const response = await axios.post("/api/game/join", { game_id: gameId });
      console.log("Joined game:", response.data);
      handleClose();
    } catch (error) {
      console.error("Failed to join game:", error);
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
          />
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
