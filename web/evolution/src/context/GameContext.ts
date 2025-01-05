import { createContext, useContext } from "react";
import { Game } from "../types/Game";

interface GameContextType {
  game: Game | null;
  setGame: (game: Game | null) => void;
}

const GameContext = createContext<GameContextType>({
  game: null,
  setGame: () => {},
});

export const useGame = () => useContext(GameContext);

export default GameContext;
