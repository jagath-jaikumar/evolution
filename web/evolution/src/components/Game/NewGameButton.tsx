import { useState } from "react";
import axios from "axios";
import Button from "@mui/material/Button";

export default function NewGameButton() {
  const [isLoading, setIsLoading] = useState(false);

  const handleNewGame = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post("/api/game/new");
      // Handle successful game creation
      console.log("New game created:", response.data);
    } catch (error) {
      console.error("Failed to create new game:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
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
  );
}
