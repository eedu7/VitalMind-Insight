"use client";

import { useConversations } from "@/features/conversations";

interface Props {
	chatId: string;
}

export const PageView = ({ chatId }: Props) => {
	const { getConversationById } = useConversations();

	const conversation = getConversationById(chatId);

	return (
		<div>
			<pre>{JSON.stringify(conversation, null, 2)}</pre>
		</div>
	);
};
