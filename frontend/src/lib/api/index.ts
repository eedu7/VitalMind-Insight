import env from "@/lib/env";
import axios from "axios";

const apiClient = axios.create({
	baseURL: env.NEXT_PUBLIC_BASE_API_URL,
	headers: {
		"Content-Type": "application/json",
		Accept: "application/json",
	},
	withCredentials: true,
});

export default apiClient;
