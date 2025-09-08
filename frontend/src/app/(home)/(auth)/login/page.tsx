import { Metadata } from "next";
import { FormCard } from "../_components/FormCard";
import { LoginForm } from "./_components/LoginForm";

export const metadata: Metadata = {
	title: "Login - VitalMind Insight | AI-Powered Healthcare Assistant",
	description:
		"Login to your VitalMind Insight account to access AI-powered healthcare assistance, medical record analysis, and intelligent support for early disease detection.",
};

export default function Page() {
	return (
		<FormCard
			title="Welcome Back to VitalMind"
			description="Sign in to access your personalized AI healthcare assistant and continue your medical insights journey."
		>
			<LoginForm />
		</FormCard>
	);
}
