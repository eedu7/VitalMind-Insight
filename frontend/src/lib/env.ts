import z from "zod";

const envSchema = z.object({
	NODE_ENV: z.string(),
	NEXT_PUBLIC_BASE_API_URL: z.url().describe("The base URL for API requests, exposed to the browser"),
});

const env = envSchema.parse(process.env);

export default env;
