import { Metadata } from "next";
import { RegisterForm } from "../_components/RegisterForm";

export const metadata: Metadata = {
	title: "Register - VitalMind Insight",
	description: "Register for a new VitalMind Insight account.",
};

export default function Page() {
	return <RegisterForm />;
}
