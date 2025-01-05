import NewGameButton from "../Game/NewGameButton";
import JoinGameButton from "../Game/JoinGameButton";
import LogoutButton from "../Authentication/LogoutButton";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { Game } from "../../types/Game";
import { useState, useContext } from "react";
import GameContext from "../../context/GameContext";

interface GameDrawerProps {
  open: boolean;
  onClose: () => void;
  games: Game[];
  isLoading: boolean;
}

export default function GameDrawer({ open, onClose, games, isLoading }: GameDrawerProps) {
  const [isJoinModalOpen, setIsJoinModalOpen] = useState(false);
  const { setGame } = useContext(GameContext);

  const handleDrawerClose = () => {
    if (!isJoinModalOpen) {
      onClose();
    }
  };

  const handleGameClick = (game: Game) => {
    setGame(game);
    console.log(game);
    onClose();
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
        <Box sx={{ p: 2 }}>
          <NewGameButton />
        </Box>
        <Box sx={{ p: 2 }}>
          <JoinGameButton onModalOpen={() => setIsJoinModalOpen(true)} onModalClose={() => setIsJoinModalOpen(false)} />
        </Box>
        <Typography variant="h6" sx={{ px: 2, py: 1 }}>
          Games
        </Typography>
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
          ) : games.length === 0 ? (
            <ListItem>
              <ListItemText primary="No games available" />
            </ListItem>
          ) : (
            games.map((game) => (
              <ListItem
                key={game.id}
                onClick={() => handleGameClick(game)}
                sx={{
                  border: "1px solid",
                  borderColor: "divider",
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
                  primary={`${game.id}`}
                  secondary={
                    <Box>
                      <Typography variant="body2" component="span">
                        Players: {game.players.length} • Epoch: {game.epoch}
                      </Typography>
                      <br />
                      <Typography
                        variant="body2"
                        component="span"
                        color="text.secondary"
                      >
                        {game.ended ?? " Ended"}
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            ))
          )}
        </List>
        <Box sx={{ p: 2 }}>
          <LogoutButton />
        </Box>
      </Box>
    </Drawer>
  );
}
