import z from "zod";
import { loginFormSchema, registerFormSchema } from "./schemas";

export type LoginFormValues = z.infer<typeof loginFormSchema>;
export type RegisterFormValues = z.infer<typeof registerFormSchema>;

export type AuthResponse = {
	message: string;
};
