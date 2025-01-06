import { NextApiRequest, NextApiResponse } from "next";
import axiosInstance from "../../../utils/axiosInstance";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  if (req.method === "POST") {
    try {
      const { username, password } = req.body;

      // Proxy the login request to the Django backend
      const response = await axiosInstance.post("/login/", {
        username,
        password,
      });

      // Return the Django response
      res.status(response.status).json(response.data);
    } catch (error) {
      res
        .status(error.response?.status || 500)
        .json({ error: "Login failed." });
    }
  } else {
    res.setHeader("Allow", ["POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
