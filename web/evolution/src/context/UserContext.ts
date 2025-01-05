import { createContext, useContext } from "react";

interface UserContextType {
  userId: string | null;
  setUserId: (userId: string | null) => void;
}

const UserContext = createContext<UserContextType>({
  userId: null,
  setUserId: () => {},
});

export const useUser = () => useContext(UserContext);

export default UserContext;
