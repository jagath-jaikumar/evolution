import { NextApiRequest, NextApiResponse } from "next";
import { apiHandler } from "../../../utils/apiHandler";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { game_id, user_id } = req.body;
  await apiHandler(req, res, {
    method: "POST",
    url: "/api/setup/new/",
    body: { game_id, user_id },
  });
}
