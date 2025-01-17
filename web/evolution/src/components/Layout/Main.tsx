import React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import GameDrawer from "./GameDrawer";
import MainGame from "@/components/Game/MainGame";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Button from "@mui/material/Button";
import Avatar from "@mui/material/Avatar";
import { useUser } from "@auth0/nextjs-auth0/client";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import GameContext from "@/context/GameContext";
import { Game } from "@/types/types";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
    background: {
      default: "#121212",
      paper: "#1e1e1e",
    },
  },
});

interface NavbarProps {
  onMenuClick: () => void;
}

function Navbar({ onMenuClick }: NavbarProps) {
  const { user } = useUser();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar
      position="fixed"
      sx={{
        background: "linear-gradient(45deg, #000000 30%, #1a1a1a 90%)",
        boxShadow: "0 3px 5px 2px rgba(0, 0, 0, .3)",
      }}
    >
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={onMenuClick}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          Evolution
        </Typography>
        {user ? (
          <>
            <IconButton
              onClick={handleClick}
              size="small"
              aria-controls={open ? "account-menu" : undefined}
              aria-haspopup="true"
              aria-expanded={open ? "true" : undefined}
            >
              <Avatar
                alt={user.name || "User"}
                src={user.picture || undefined}
                sx={{ width: 32, height: 32 }}
              />
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              id="account-menu"
              open={open}
              onClose={handleClose}
              onClick={handleClose}
              transformOrigin={{ horizontal: "right", vertical: "top" }}
              anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
            >
              <MenuItem component="a" href="/api/auth/logout">
                Logout
              </MenuItem>
            </Menu>
          </>
        ) : (
          <Button color="inherit" component="a" href="/api/auth/login">
            Login
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default function Main() {
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [game, setGame] = React.useState<Game | null>(null);

  const handleDrawerClose = () => {
    setDrawerOpen(false);
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <GameContext.Provider value={{ game, setGame }}>
        <Box
          sx={{
            display: "flex",
            bgcolor: "background.default",
            minHeight: "100vh",
          }}
        >
          <CssBaseline />
          <Navbar onMenuClick={() => setDrawerOpen(true)} />
          <GameDrawer
            open={drawerOpen}
            onClose={handleDrawerClose}
            games={[]}
            isLoading={false}
          />
          <Box
            component="main"
            sx={{ flexGrow: 1, p: 3, mt: 8, width: "100%" }}
          >
            <MainGame />
          </Box>
        </Box>
      </GameContext.Provider>
    </ThemeProvider>
  );
}
