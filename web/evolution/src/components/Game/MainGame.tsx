import { useContext } from "react";
import GameContext from "@/context/GameContext";
import { Box } from "@mui/material";
import Welcome from "./Components/Blurb/Welcome";
import GameBoard from "./Components/Board/GameBoard";
export default function MainGame() {
  const { game, setGame } = useContext(GameContext);

  return <Box>{!game ? <Welcome /> : <GameBoard />}</Box>;
}
