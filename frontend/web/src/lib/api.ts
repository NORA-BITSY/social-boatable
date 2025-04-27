import axios from "axios";
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000"
});
export function setAuth(token: string) {
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}
