import { Message } from "../messages";

export type GetConversationByID = {
	conversationId: string;
};

export type CreateConversation = {
	title: string;
};

export type UpdateConversation = CreateConversation & {
	conversationId: string;
};

export type DeleteConversation = {
	conversationId: string;
};

export type Conversation = {
	uuid: string;
	title: string;
	messages: Message[];
};
