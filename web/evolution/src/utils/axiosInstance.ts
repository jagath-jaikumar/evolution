import axios from "axios";

const axiosInstance = axios.create({
  baseURL: process.env.DJANGO_BACKEND_URL,
});

// Add the Authorization header to all requests
axiosInstance.interceptors.request.use((config) => {
  const token = process.env.DJANGO_AUTH_TOKEN;
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default axiosInstance;
