import { useRouter } from "next/router";
import LoginForm from "../components/Authentication/LoginForm";
import "../styles/globals.css";
import { useEffect, useState } from "react";
import Main from "../components/Layout/Main";
import UserContext from "../context/UserContext";
import Game from "../components/Game/Game";
import GameContext from "../context/GameContext";

export default function Home() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);
  const [game, setGame] = useState<Game | null>(null);

  useEffect(() => {
    if (sessionStorage.getItem("userId")) {
      setUserId(sessionStorage.getItem("userId"));
    }
  }, [router]);

  return (
    <UserContext.Provider value={{ userId, setUserId }}>
      <GameContext.Provider value={{ game, setGame }}>
        <div>
          {userId ? (
            <Main>
              <Game />
            </Main>
          ) : (
            <LoginForm />
          )}
        </div>
      </GameContext.Provider>
    </UserContext.Provider>
  );
}
