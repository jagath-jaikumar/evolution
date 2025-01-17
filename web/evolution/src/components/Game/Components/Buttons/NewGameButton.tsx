import { useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import { useUser } from "@auth0/nextjs-auth0/client";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import { callApi } from "@/utils/callApi";

interface NewGameButtonProps {
  onGameCreated?: () => void;
}

interface CreateGameResponse {
  id: string;
  detail?: string;
  error?: string;
}

export default function NewGameButton({ onGameCreated }: NewGameButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAlert, setShowAlert] = useState(false);
  const { user } = useUser();

  const handleNewGame = async () => {
    if (!user?.sub) {
      setError("User must be logged in");
      setShowAlert(true);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Create new game
      const createResult = await callApi<CreateGameResponse>(
        "post",
        "api/game/",
        {
          user_id: user.sub,
        },
      );

      if (!createResult.success || !createResult.data?.id) {
        setError(
          `Failed to create game: ${createResult.data?.detail || createResult.data?.error || ""}`,
        );
        setShowAlert(true);
        return;
      }

      // Call the onGameCreated callback if provided
      if (onGameCreated) {
        onGameCreated();
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
        onClick={handleNewGame}
        disabled={isLoading || !user}
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
