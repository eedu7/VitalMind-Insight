import z from "zod";

const envSchema = z.object({
	NEXT_PUBLIC_BASE_API_URL: z.url().describe("The base URL for API requests, exposed to the browser"),
});

const env = envSchema.parse({
	NEXT_PUBLIC_BASE_API_URL: process.env.NEXT_PUBLIC_BASE_API_URL!,
});

export default env;
