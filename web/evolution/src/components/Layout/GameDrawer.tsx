import NewGameButton from "@/components/Game/Components/Buttons/NewGameButton";
import JoinGameButton from "@/components/Game/Components/Buttons/JoinGameButton";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { Game } from "@/types/types";
import { useState, useContext } from "react";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import IconButton from "@mui/material/IconButton";
import { useUser } from "@auth0/nextjs-auth0/client";
import { callApi } from "@/utils/callApi";
import { useEffect } from "react";
import GameContext from "@/context/GameContext";

interface GameDrawerProps {
  open: boolean;
  onClose: () => void;
  games: Game[];
  isLoading: boolean;
}

export default function GameDrawer({
  open,
  onClose,
  games,
  isLoading,
}: GameDrawerProps) {
  const { user } = useUser();
  const { setGame } = useContext(GameContext);
  const [isJoinModalOpen, setIsJoinModalOpen] = useState(false);
  const [localGames, setLocalGames] = useState<Game[]>(games);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const refreshGames = async () => {
    setIsRefreshing(true);
    try {
      const response = await callApi<Game[]>("get", "api/game/");
      if (response.success && response.data) {
        setLocalGames(response.data);
      }
    } finally {
      setIsRefreshing(false);
    }
  };

  // Initial load when component mounts
  useEffect(() => {
    refreshGames();
  }, []);

  // Set up polling only when drawer is open
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (open) {
      interval = setInterval(() => {
        refreshGames();
      }, 5000);
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [open]);

  const handleDrawerClose = () => {
    if (!isJoinModalOpen) {
      onClose();
    }
  };

  const handleGameClick = (game: Game) => {
    setGame(game);
    onClose();
  };

  const handleCopyClick = (e: React.MouseEvent, gameId: string) => {
    e.stopPropagation();
    navigator.clipboard.writeText(gameId.toString());
  };

  const getGameStatus = (game: Game) => {
    if (game.ended) return "Ended";
    if (game.started) return "In Progress";
    return "Waiting to Start";
  };

  const getBorderColor = (game: Game) => {
    if (game.ended) return "grey.400";
    if (game.started) return "success.main";
    return "warning.main"; // Orange for waiting to start
  };

  return (
    <Drawer anchor="left" open={open} onClose={handleDrawerClose}>
      <Box
        sx={{
          width: 250,
          height: "100%",
          display: "flex",
          flexDirection: "column",
        }}
        role="presentation"
        onKeyDown={handleDrawerClose}
      >
        {user ? (
          <>
            <Box sx={{ p: 2, display: "flex", gap: 1 }}>
              <NewGameButton onGameCreated={refreshGames} />
              <JoinGameButton
                onModalOpen={() => setIsJoinModalOpen(true)}
                onModalClose={() => {
                  setIsJoinModalOpen(false);
                  refreshGames();
                }}
              />
            </Box>
            <Box sx={{ px: 2, py: 1 }}>
              <Typography variant="h6">Games</Typography>
            </Box>
            <List
              sx={{
                flexGrow: 1,
                overflow: "auto",
                maxHeight: "calc(100vh - 200px)",
              }}
            >
              {isLoading ? (
                <ListItem>
                  <ListItemText primary="Loading games..." />
                </ListItem>
              ) : localGames.length === 0 ? (
                <ListItem>
                  <ListItemText primary="No games available" />
                </ListItem>
              ) : (
                [...localGames].reverse().map((game) => (
                  <ListItem
                    key={game.id}
                    onClick={() => handleGameClick(game)}
                    sx={{
                      border: "2px solid",
                      borderColor: getBorderColor(game),
                      borderRadius: 1,
                      mb: 1,
                      cursor: "pointer",
                      "&:hover": {
                        borderColor: "primary.main",
                        backgroundColor: "action.hover",
                      },
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box sx={{ display: "flex", alignItems: "center" }}>
                          <Typography component="span">
                            {game.id.substring(0, 8)}
                          </Typography>
                          {!game.started && !game.ended && (
                            <IconButton
                              size="small"
                              onClick={(e) => handleCopyClick(e, game.id)}
                              sx={{ ml: 1 }}
                            >
                              <ContentCopyIcon fontSize="small" />
                            </IconButton>
                          )}
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="body2" component="span">
                            Players: {game.player_count} • Epoch:{" "}
                            {game.current_epoch?.epoch_number || "N/A"}
                          </Typography>
                          <br />
                          <Typography
                            variant="body2"
                            component="span"
                            color="text.secondary"
                          >
                            Status: {getGameStatus(game)}
                          </Typography>
                        </>
                      }
                    />
                  </ListItem>
                ))
              )}
            </List>
          </>
        ) : (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
            }}
          >
            <Typography variant="h6">Log in to play!</Typography>
          </Box>
        )}
      </Box>
    </Drawer>
  );
}
