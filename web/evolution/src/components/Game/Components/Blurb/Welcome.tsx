import React from "react";
import { Card, CardContent, Typography, Box, Button } from "@mui/material";
import { useUser } from "@auth0/nextjs-auth0/client";

export default function Welcome() {
  const { user } = useUser();

  return (
    <Box
      sx={{
        maxWidth: 800,
        mx: "auto",
        mt: 8,
        px: 3,
      }}
    >
      <Card
        sx={{
          background:
            "linear-gradient(145deg, rgba(30,30,30,0.9) 0%, rgba(20,20,20,0.95) 100%)",
          backdropFilter: "blur(10px)",
          boxShadow: "0 8px 32px rgba(0,0,0,0.3)",
          borderRadius: 4,
          border: "1px solid rgba(255,255,255,0.1)",
          overflow: "hidden",
          position: "relative",
        }}
      >
        <Box
          sx={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: "4px",
            background: "linear-gradient(90deg, #00c6ff 0%, #0072ff 100%)",
          }}
        />

        <CardContent sx={{ p: 6 }}>
          <Typography
            variant="h3"
            component="h1"
            gutterBottom
            sx={{
              fontWeight: 700,
              background: "linear-gradient(90deg, #fff 0%, #e0e0e0 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              mb: 4,
            }}
          >
            Welcome to Evolution Online
          </Typography>

          <Typography
            variant="h6"
            sx={{
              color: "rgba(255,255,255,0.9)",
              lineHeight: 1.6,
              mb: 4,
            }}
          >
            Evolution is a strategy game where you adapt and evolve your species
            to survive in a dynamic ecosystem. Compete with other players,
            develop unique traits, and build the most successful species.
          </Typography>

          {!user && (
            <Box
              sx={{
                mt: 4,
                p: 4,
                borderRadius: 2,
                background:
                  "linear-gradient(145deg, rgba(0,198,255,0.1) 0%, rgba(0,114,255,0.1) 100%)",
                border: "1px solid rgba(0,198,255,0.2)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 3,
              }}
            >
              <Typography
                variant="body1"
                sx={{ color: "rgba(255,255,255,0.9)", textAlign: "center" }}
              >
                Ready to start your evolutionary journey? Sign in to create or
                join games!
              </Typography>
              <Button
                variant="contained"
                href="/api/auth/login"
                sx={{
                  background:
                    "linear-gradient(90deg, #00c6ff 0%, #0072ff 100%)",
                  px: 4,
                  py: 1.5,
                  borderRadius: 2,
                  textTransform: "none",
                  fontSize: "1.1rem",
                  fontWeight: 500,
                  "&:hover": {
                    background:
                      "linear-gradient(90deg, #00b4e6 0%, #0066e6 100%)",
                  },
                }}
              >
                Sign In to Play
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
