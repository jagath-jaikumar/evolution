import { withApiAuthRequired, getAccessToken } from "@auth0/nextjs-auth0";
import { NextApiRequest, NextApiResponse } from "next";

export default withApiAuthRequired(async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  try {
    const { accessToken } = await getAccessToken(req, res);

    // Extract the dynamic path from the request
    const path = req.query.path as string[];

    // Reconstruct the Django backend URL
    const djangoBaseUrl = process.env.NEXT_PUBLIC_DJANGO_BACKEND_URL;
    const djangoUrl = `${djangoBaseUrl}/${path.join("/")}${path.length > 0 && !path[path.length - 1].endsWith("/") ? "/" : ""}`;

    // Forward the request to the Django backend
    const response = await fetch(djangoUrl, {
      method: req.method || "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type":
          req.headers["content-type"]?.toString() || "application/json",
      },
      body: ["GET", "HEAD"].includes(req.method?.toUpperCase() || "")
        ? undefined
        : JSON.stringify(req.body),
    });

    // Forward the response back to the client
    const responseBody = await response.text();
    res.status(response.status).send(responseBody);
  } catch (error: unknown) {
    console.error("Proxy error:", error);
    const err = error as { status?: number; message?: string };
    res.status(err.status || 500).json({
      error: err.message || "Internal server error",
    });
  }
});
