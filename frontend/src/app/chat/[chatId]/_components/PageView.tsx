"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import { useConversations } from "@/features/conversations";
import { Message } from "@/features/messages";
import { Prompt } from "@/features/prompts";
import { cn } from "@/lib/utils";

interface Props {
	chatId: string;
}

export const PageView = ({ chatId }: Props) => {
	const { getConversationById } = useConversations(chatId);
	const { data } = getConversationById;

	return (
		<div className="mx-auto flex h-screen max-h-screen flex-col overflow-hidden p-2 py-4 md:max-w-2xl lg:max-w-4xl">
			{/* TODO: ScrollArea is not working properly  */}
			<ScrollArea className="flex-1 overflow-auto">
				{data?.messages ? <ChatMessage messages={data.messages} /> : null}
			</ScrollArea>

			<div className="pt-2">
				<Prompt />
			</div>
		</div>
	);
};

interface ChatMessageProps {
	messages: Message[];
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ messages }) => {
	return (
		<div className="flex w-full flex-col gap-y-4 pr-4">
			{messages.map(({ content, role }, index) => (
				<div key={index} className={cn("flex w-full", role === "user" ? "justify-end" : "justify-start")}>
					<p className={cn("w-full rounded-lg p-2", role === "user" && "bg-accent max-w-[75%]")}>{content}</p>
				</div>
			))}
		</div>
	);
};
