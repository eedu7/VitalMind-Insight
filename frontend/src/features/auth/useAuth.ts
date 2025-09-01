"use client";

import env from "@/lib/env";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { loginUser, logoutUser, registerUser } from "./api";

export function useAuth() {
	const router = useRouter();

	const register = useMutation({
		mutationKey: ["newUser", "registerUser"],
		mutationFn: registerUser,
		onSuccess: () => {
			router.push(env.NEXT_PUBLIC_AFTER_SIGN_UP_URL);
		},
	});

	const login = useMutation({
		mutationKey: ["existingUser", "loginUser"],
		mutationFn: loginUser,
		onSuccess: () => {
			// router.push(env.NEXT_PUBLIC_AFTER_SIGN_IN_URL);
		},
		onError: (err) => {
			alert(err);
		},
	});

	const logout = useMutation({
		mutationKey: ["existingUser", "logoutUser"],
		mutationFn: logoutUser,
		onSuccess: () => {
			router.push(env.NEXT_PUBLIC_AFTER_SIGN_OUT_URL);
		},
	});

	return {
		register,
		login,
		logout,
	};
}
