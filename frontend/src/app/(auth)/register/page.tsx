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
			title="Join VitalMind Insight"
			description="Create an account to explore AI-powered healthcare assistance, smart medical insights, and early disease detection tools."
		>
			<RegisterForm />
		</FormCard>
	);
}
