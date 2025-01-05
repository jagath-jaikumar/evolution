import { NextApiRequest, NextApiResponse } from "next";
import axiosInstance from "../../../utils/axiosInstance";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const user_id = req.query.user_id;

  try {
    const response = await axiosInstance.get(
      `/api/observe/games_for_user/?user_id=${user_id}`,
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json({ error: "Request failed." });
  }
}
