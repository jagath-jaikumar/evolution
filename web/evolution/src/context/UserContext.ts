import { createContext, useContext } from "react";

interface UserContextType {
  userId: number | null;
  setUserId: (userId: number | null) => void;
}

const UserContext = createContext<UserContextType>({
  userId: null,
  setUserId: () => {},
});

export const useUser = () => useContext(UserContext);

export default UserContext;
