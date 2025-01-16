import { useState } from "react";
import { useUser } from "../../context/UserContext";

export default function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { setUserId } = useUser();

  const handleLogin = async () => {
    setError("");
    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem("userId", data.user_id);
        sessionStorage.setItem("username", data.username);
        setUserId(data.user_id);
      } else {
        const errorData = await response.json();
        setError(errorData.error || "Login failed.");
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && username && password) {
      handleLogin();
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Log In</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        onKeyPress={handleKeyPress}
        className="block w-full px-4 py-2 mb-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        onKeyPress={handleKeyPress}
        className="block w-full px-4 py-2 mb-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        onClick={handleLogin}
        className="w-full bg-gradient-to-r from-blue-500 to-blue-700 text-white py-2 rounded-lg hover:from-blue-600 hover:to-blue-800 transition-transform transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-300"
      >
        Log In
      </button>
      {error && <p className="text-red-500 mt-2 text-sm">{error}</p>}
    </div>
  );
}
