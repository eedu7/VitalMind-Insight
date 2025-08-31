import z from "zod";

export const loginFormSchema = z.object({
	email: z.email("Invalid email address"),
	password: z
		.string()
		.min(6, "Password must be at least 6 characters")
		.max(100, "Password must be at most 100 characters"),
});

export const registerFormSchema = loginFormSchema.extend({
	username: z
		.string()
		.min(3, "Username must be at least 3 characters")
		.max(20, "Username must be at most 20 characters"),
});
