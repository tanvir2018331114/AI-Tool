import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const registerTool = (tool: any) => api.post("/register_tool", tool);
export const runTask = (task: string) => api.post("/run_task", { task });
