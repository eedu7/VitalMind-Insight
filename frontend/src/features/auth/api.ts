import apiClient from "@/lib/api";
import { AuthResponse, LoginFormValues, RegisterFormValues } from "./types";

const AUTH_URL = "/api/auth/web";

export async function registerUser(data: RegisterFormValues): Promise<AuthResponse> {
	try {
		const res = await apiClient.post<AuthResponse>(`${AUTH_URL}/register`, data);
		return res.data;
	} catch (err) {
		throw err;
	}
}

export async function loginUser(data: LoginFormValues): Promise<AuthResponse> {
	try {
		const res = await apiClient.post<AuthResponse>(`${AUTH_URL}/login`, data);
		return res.data;
	} catch (err) {
		throw err;
	}
}

export async function logoutUser(): Promise<AuthResponse> {
	try {
		const res = await apiClient.post<AuthResponse>(`${AUTH_URL}/logout`);
		return res.data;
	} catch (err) {
		throw err;
	}
}
