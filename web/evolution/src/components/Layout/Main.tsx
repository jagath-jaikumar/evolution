
import React, { useEffect, useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import axios from 'axios';
import GameDrawer from './GameDrawer';
import { Game } from '../../types/Game';



export default function Main({ children }: { children: React.ReactNode }) {
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [games, setGames] = useState<Game[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchGames = async () => {
      setIsLoading(true);
      try {
        const userId = sessionStorage.getItem('userId');
        const response = await axios.get(`/api/game/all?user_id=${userId}`);
        console.log(response.data);
        setGames(response.data);
      } catch (error) {
        console.error('Failed to fetch games:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchGames();
  }, []);

  const handleDrawerClose = () => {
    setDrawerOpen(false);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={() => setDrawerOpen(true)}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Evolution
          </Typography>
        </Toolbar>
      </AppBar>
      <GameDrawer 
        open={drawerOpen}
        onClose={handleDrawerClose}
        games={games}
        isLoading={isLoading}
      />
      <Box
        component="main"
        sx={{ flexGrow: 1, p: 3, mt: 8, width: '100%' }}
      >
        <Container>{children}</Container>
      </Box>
    </Box>
  );
}
