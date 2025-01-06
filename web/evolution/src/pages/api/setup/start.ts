import { NextApiRequest, NextApiResponse } from "next";
import axiosInstance from "../../../utils/axiosInstance";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const game_id = req.body.game_id;

  if (!game_id) {
    res.status(400).json({ error: "Game ID is required" });
    return;
  }

  try {
    const response = await axiosInstance.post("/api/setup/start/", {
      game_id,
    });
    res.status(response.status).json(response.data);
  } catch (error: any) {
    res
      .status(error.response?.status || 500)
      .json({ error: error.response?.data?.error || "Failed to join game" });
  }
}
