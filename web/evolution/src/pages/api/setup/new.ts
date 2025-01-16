import { NextApiRequest, NextApiResponse } from "next";
import axiosInstance from "../../../utils/axiosInstance";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const game_id = req.body.game_id;
  const user_id = req.body.user_id;

  try {
    const response = await axiosInstance.post("/api/setup/new/", {
      game_id,
      user_id,
    });
    res.status(response.status).json(response.data);
  } catch (error: any) {
    res
      .status(error.response?.status || 500)
      .json({ error: "Failed to join game" });
  }
}
