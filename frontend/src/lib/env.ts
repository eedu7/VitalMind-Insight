import z from "zod";

const envSchema = z.object({
	NEXT_PUBLIC_BASE_API_URL: z.url().describe("The base URL for API requests, exposed to the browser"),
	NEXT_PUBLIC_AFTER_SIGN_UP_URL: z.string().describe("Relative path to redirect users after successful sign-up"),
	NEXT_PUBLIC_AFTER_SIGN_IN_URL: z.string().describe("Relative path to redirect users after successful sign-in"),
	NEXT_PUBLIC_AFTER_SIGN_OUT_URL: z.string().describe("Relative path to redirect users after signing out"),
});

const env = envSchema.parse({
	NEXT_PUBLIC_BASE_API_URL: process.env.NEXT_PUBLIC_BASE_API_URL!,
	NEXT_PUBLIC_AFTER_SIGN_UP_URL: process.env.NEXT_PUBLIC_AFTER_SIGN_UP_URL!,
	NEXT_PUBLIC_AFTER_SIGN_IN_URL: process.env.NEXT_PUBLIC_AFTER_SIGN_IN_URL!,
	NEXT_PUBLIC_AFTER_SIGN_OUT_URL: process.env.NEXT_PUBLIC_AFTER_SIGN_OUT_URL!,
});

export default env;
