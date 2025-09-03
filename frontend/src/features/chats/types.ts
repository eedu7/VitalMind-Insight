import { Message } from "../messages";

export type GetChatByID = {
	chatId: string;
};

export type CreateConversation = {
	title: string;
};

export type UpdateConversation = CreateConversation & {};

export type DeleteConversation = {
	chatId: string;
};

export type Conversation = {
	uuid: string;
	title: string;
	messages: Message[];
};
