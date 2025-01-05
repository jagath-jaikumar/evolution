import { useState } from "react";
import { useUser } from "../../context/UserContext";
import Button from "@mui/material/Button";

export default function LogoutButton() {
  const [isLoading, setIsLoading] = useState(false);
  const { setUserId } = useUser();

  const handleLogout = async () => {
    setIsLoading(true);
    try {
      sessionStorage.removeItem("userId");
      setUserId(null);
    } catch (error) {
      console.error("Failed to logout:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Button
      variant="contained"
      color="error"
      onClick={handleLogout}
      disabled={isLoading}
      sx={{
        textTransform: "none",
        "&:hover": {
          transform: "scale(1.05)",
          transition: "transform 0.2s",
        },
      }}
    >
      {isLoading ? "Logging out..." : "Log Out"}
    </Button>
  );
}
