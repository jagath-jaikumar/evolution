import { NextApiRequest, NextApiResponse } from "next";
import { apiHandler } from "../../../utils/apiHandler";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { game_id, user_id, action } = req.body;
  if (!game_id || !user_id || !action) {
    res.status(400).json({ error: "Game ID, User ID, and Action are required" });
    return;
  }

  await apiHandler(req, res, {
    method: "POST",
    url: "/api/play/basic_action/",
    body: { game_id, user_id, action },
  });
}
