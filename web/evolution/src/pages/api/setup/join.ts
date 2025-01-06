import { NextApiRequest, NextApiResponse } from "next";
import axiosInstance from "../../../utils/axiosInstance";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const game_id = req.body.game_id;
  const user_id = req.body.user_id;

  if (!game_id) {
    res.status(400).json({ error: "Game ID is required" });
    return;
  }

  if (!user_id) {
    res.status(400).json({ error: "User ID is required" });
    return;
  }

  try {
    const response = await axiosInstance.post("/api/setup/join/", {
      game_id,
      user_id,
    });
    res.status(response.status).json(response.data);
  } catch (error: any) {
    res
      .status(error.response?.status || 500)
      .json({ error: error.response?.data?.error || "Failed to join game" });
  }
}
