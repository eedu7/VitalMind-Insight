import { Message } from "../messages";

export type Conversation = {
	uuid: string;
	title: string;
	messages?: Message[];
};

export type GetConversationById = Pick<Conversation, "uuid">;
export type UpdateConversation = Omit<Conversation, "messages">;
export type DeleteConversation = Pick<Conversation, "uuid">;
export type CreateConversation = Pick<Conversation, "title">;

