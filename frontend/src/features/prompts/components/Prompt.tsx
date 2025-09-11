"use client";
import { PromptInputField } from "@/components/PromptInputField";
import { useConversations } from "@/features/conversations";
import { useState } from "react";

export const Prompt = () => {
	const { createConversation } = useConversations();
	const [prompt, setPrompt] = useState("");

	const onSubmit = () => {
		createConversation.mutateAsync({
			title: prompt,
		});
	};

	return (
		<PromptInputField
			prompt={prompt}
			setPrompt={setPrompt}
			onSubmit={onSubmit}
			isPending={createConversation.isPending}
		/>
	);
};
