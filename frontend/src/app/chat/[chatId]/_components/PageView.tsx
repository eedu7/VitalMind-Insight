"use client";

import { useConversations } from "@/features/conversations";
import { Prompt } from "@/features/prompts";

interface Props {
	chatId: string;
}

export const PageView = ({ chatId }: Props) => {
	const { getConversationById } = useConversations();

	const conversation = getConversationById(chatId);

	return (
		<div className="mx-auto flex h-screen flex-col place-items-center p-2 py-4 md:max-w-2xl lg:max-w-4xl">
			<div className="flex-1"></div>
			<Prompt />
		</div>
	);
};
