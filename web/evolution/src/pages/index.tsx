import { UserProvider } from "@auth0/nextjs-auth0/client";
import Main from "@/components/Layout/Main";

export default function Home() {
  return (
    <UserProvider>
      <Main />
    </UserProvider>
  );
}
