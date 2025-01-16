// utils/apiHandler.ts
import { NextApiRequest, NextApiResponse } from "next";
import axiosInstance from "./axiosInstance";

export const apiHandler = async (
  req: NextApiRequest,
  res: NextApiResponse,
  options: {
    method: string;
    url: string;
    body?: any;
    queryParams?: any;
  },
) => {
  const { method, url, body, queryParams } = options;

  if (req.method !== method) {
    res.setHeader("Allow", [method]);
    res.status(405).json({ error: `Method ${req.method} Not Allowed` });
    return;
  }

  try {
    const response = await axiosInstance({
      method,
      url,
      data: body,
      params: queryParams,
    });
    res.status(response.status).json(response.data);
  } catch (error: any) {
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.error || "Request failed.",
    });
  }
};
