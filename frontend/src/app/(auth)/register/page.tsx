import { Metadata } from "next";
import { FormCard } from "../_components/FormCard";
import { RegisterForm } from "./_components/RegisterForm";

export const metadata: Metadata = {
	title: "Register - VitalMind Insight | AI-Powered Healthcare Assistant",
	description:
		"Create a new account on VitalMind Insight, an AI-powered healthcare assistant that uses LLMs and OCR to analyze medical records, provide intelligent chat support, and assist in early disease detection and diagnosis.",
};

export default function Page() {
	return (
		<FormCard
			title="Create Your VitalMind Account"
			description="Sign up to use our AI healthcare assistant for smart medical insights."
		>
			<RegisterForm />
		</FormCard>
	);
}
