import { useRouter } from "next/router";
import LoginForm from "../components/Authentication/LoginForm";
import { useEffect, useState } from "react";
import Main from "../components/Layout/Main";
import UserContext from "../context/UserContext";
import GameComponent from "../components/Game/GameComponent";
import GameContext from "../context/GameContext";
import { Game } from "../types/Game";

export default function Home() {
  const router = useRouter();
  const [userId, setUserId] = useState<number | null>(null);
  const [game, setGame] = useState<Game | null>(null);

  useEffect(() => {
    if (sessionStorage.getItem("userId")) {
      setUserId(parseInt(sessionStorage.getItem("userId") || "0"));
    }
  }, [router]);

  return (
    <UserContext.Provider value={{ userId, setUserId }}>
      <GameContext.Provider value={{ game, setGame }}>
        <div>
          {userId ? (
            <Main>
              <GameComponent />
            </Main>
          ) : (
            <LoginForm />
          )}
        </div>
      </GameContext.Provider>
    </UserContext.Provider>
  );
}
