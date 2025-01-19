import { useContext, useEffect, useState } from "react";
import GameContext from "@/context/GameContext";
import { Box, CircularProgress, Typography } from "@mui/material";
import Welcome from "./Components/Blurb/Welcome";
import GameBoard from "./Components/Board/GameBoard";
import { callApi } from "@/utils/callApi";
import { Game } from "@/types/types";
import { useUser } from "@auth0/nextjs-auth0/client";

export default function MainGame() {
  const { setGame } = useContext(GameContext);
  const { user, isLoading: userLoading } = useUser();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const loadGames = async () => {
      if (!user) return;
      
      setIsLoading(true);
      try {
        const response = await callApi<Game[]>("get", "api/game/");
        if (response.success && response.data && response.data.length > 0) {
          // Find most recent non-ended game
          const activeGame = [...response.data]
            .reverse()
            .find(game => !game.ended);
            
          if (activeGame) {
            setGame(activeGame);
          }
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadGames();
  }, [setGame, user]);

  if (userLoading) {
    return <Box />;
  }

  if (!user) {
    return <Box><Welcome /></Box>;
  }

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', gap: 2 }}>
        <CircularProgress />
        <Typography>Getting your games...</Typography>
      </Box>
    );
  }

  return <Box><GameBoard /></Box>;
}
