import { NextApiRequest, NextApiResponse } from "next";
import axiosInstance from "../../../utils/axiosInstance";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const game_id = req.query.game_id;

  try {
    const response = await axiosInstance.get(
      `/api/observe/game/?game_id=${game_id}`,
    );
    res.status(response.status).json(response.data);
  } catch (error: any) {
    res
      .status(error.response?.status || 500)
      .json({ error: "Request failed." });
  }
}
