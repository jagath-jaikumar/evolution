import React from "react";
import { Box, Paper } from "@mui/material";

interface HandTrayProps {
  game: any;
  visible: boolean;
}

const HandTray: React.FC<HandTrayProps> = ({ game, visible }) => {
  return (
    <Paper
      elevation={3}
      sx={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        height: 200,
        backgroundColor: "#f0f0f0",
        boxShadow: "0px -2px 5px rgba(0, 0, 0, 0.2)",
        transform: visible ? "translateY(0)" : "translateY(100%)",
        transition: "transform 0.3s ease-in-out",
        zIndex: 1000,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Box sx={{ display: "flex", gap: 2 }}>
        {/* {game.hand.map((card: string, index: number) => (
          <Paper
            key={index}
            sx={{
              width: 80,
              height: 120,
              backgroundColor: "#ffffff",
              border: "1px solid #ccc",
              borderRadius: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)",
            }}
          >
            {card}
          </Paper>
        ))} */}
      </Box>
    </Paper>
  );
};

export default HandTray;
