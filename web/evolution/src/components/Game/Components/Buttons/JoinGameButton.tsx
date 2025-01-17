import { useState } from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { useUser } from "@auth0/nextjs-auth0/client";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import { callApi } from "@/utils/callApi";

interface JoinGameButtonProps {
  onModalOpen: () => void;
  onModalClose: () => void;
}

interface JoinGameResponse {
  id: string;
  detail?: string;
}

export default function JoinGameButton({
  onModalOpen,
  onModalClose,
}: JoinGameButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [gameId, setGameId] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [showAlert, setShowAlert] = useState(false);
  const { user } = useUser();

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

  const handleCloseAlert = () => {
    setShowAlert(false);
  };

  const handleJoinGame = async () => {
    if (!user?.sub) {
      setError("User must be logged in");
      setShowAlert(true);
      return;
    }

    if (!gameId.trim()) {
      setError("Please enter a game ID");
      setShowAlert(true);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const joinResult = await callApi<JoinGameResponse>(
        "post",
        `api/game/${gameId}/join/`,
        {
          user_id: user.sub,
        },
      );

      if (!joinResult.success) {
        setError(
          `Failed to join game: ${joinResult.data?.detail || "Unknown error"}`,
        );
        setShowAlert(true);
        return;
      }

      handleClose();
    } catch (err: any) {
      setError(`An unexpected error occurred: ${err.message}`);
      setShowAlert(true);
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
        disabled={isLoading || !user}
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

      <Snackbar
        open={showAlert}
        autoHideDuration={6000}
        onClose={handleCloseAlert}
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      >
        <Alert
          onClose={handleCloseAlert}
          severity="error"
          sx={{ width: "100%" }}
        >
          {error}
        </Alert>
      </Snackbar>
    </>
  );
}
