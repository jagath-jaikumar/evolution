import { NextApiRequest, NextApiResponse } from "next";
import { apiHandler } from "../../../utils/apiHandler";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { user_id } = req.query;
  await apiHandler(req, res, {
    method: "GET",
    url: "/api/observe/games_for_user/",
    queryParams: { user_id },
  });
}
