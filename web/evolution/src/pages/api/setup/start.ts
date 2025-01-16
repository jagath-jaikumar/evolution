import { NextApiRequest, NextApiResponse } from "next";
import { apiHandler } from "../../../utils/apiHandler";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { game_id } = req.body;
  if (!game_id) {
    res.status(400).json({ error: "Game ID is required" });
    return;
  }

  await apiHandler(req, res, {
    method: "POST",
    url: "/api/setup/start/",
    body: { game_id },
  });
}
