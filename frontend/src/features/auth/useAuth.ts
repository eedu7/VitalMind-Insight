"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { loginUser, registerUser } from "./api";

export function useAuth() {
	const queryClient = useQueryClient();

	const register = useMutation({
		mutationKey: ["newUser", "registerUser"],
		mutationFn: registerUser,
	});

	const login = useMutation({
		mutationKey: ["existingUser", "loginUser"],
		mutationFn: loginUser,
	});

	return {
		register,
		login,
	};
}
