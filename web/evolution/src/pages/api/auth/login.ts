import axios from "axios";
import { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  if (req.method === "POST") {
    try {
      const { username, password } = req.body;

      // Proxy the login request to the Django backend
      const response = await axios.post(
        `${process.env.DJANGO_BACKEND_URL}/login/`,
        {
          username,
          password,
        },
      );

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
