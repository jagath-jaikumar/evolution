import { NextApiRequest, NextApiResponse } from "next";
import { apiHandler } from "../../../utils/apiHandler";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { game_id } = req.query;
  await apiHandler(req, res, {
    method: "GET",
    url: "/api/observe/game/",
    queryParams: { game_id },
  });
}
