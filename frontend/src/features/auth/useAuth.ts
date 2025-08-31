"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { loginUser, registerUser } from "./api";

export function useAuth() {
	const router = useRouter();

	const register = useMutation({
		mutationKey: ["newUser", "registerUser"],
		mutationFn: registerUser,
		onSuccess: () => {
			router.push("/");
		},
	});

	const login = useMutation({
		mutationKey: ["existingUser", "loginUser"],
		mutationFn: loginUser,
		onSuccess: () => {
			router.push("/");
		},
	});

	return {
		register,
		login,
	};
}
