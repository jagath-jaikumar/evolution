import { NextApiRequest, NextApiResponse } from "next";
import { apiHandler } from "../../../utils/apiHandler";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { username, password } = req.body;
  await apiHandler(req, res, {
    method: "POST",
    url: "/login/",
    body: { username, password },
  });
}
