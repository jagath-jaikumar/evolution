import { useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import { callApi } from "@/utils/callApi";

interface StartGameButtonProps {
  gameId: string;
  onGameStarted?: () => void;
}

interface StartGameResponse {
  detail?: string;
  error?: string;
}

export default function StartGameButton({
  gameId,
  onGameStarted,
}: StartGameButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAlert, setShowAlert] = useState(false);

  const handleStartGame = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const startResult = await callApi<StartGameResponse>(
        "post",
        `api/game/${gameId}/start`,
      );

      if (!startResult.success) {
        console.log(startResult);
        setError(
          `Failed to start game: ${startResult.data?.detail || startResult?.error || ""}`,
        );
        setShowAlert(true);
        return;
      }

      if (onGameStarted) {
        onGameStarted();
      }
    } catch (err: any) {
      setError(`An unexpected error occurred: ${err.message}`);
      setShowAlert(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCloseAlert = () => {
    setShowAlert(false);
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
    </Box>
  );
}
