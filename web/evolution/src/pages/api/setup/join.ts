import { NextApiRequest, NextApiResponse } from "next";
import { apiHandler } from "../../../utils/apiHandler";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { game_id, user_id } = req.body;
  if (!game_id || !user_id) {
    res.status(400).json({ error: "Game ID and User ID are required" });
    return;
  }

  await apiHandler(req, res, {
    method: "POST",
    url: "/api/setup/join/",
    body: { game_id, user_id },
  });
}
