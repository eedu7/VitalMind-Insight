import { Message } from "../messages";
import { updateConversationApi } from "./api";

export type Conversation = {
	uuid: string;
	title: string;
	messages?: Message[];
};

export type GetConversationById = Pick<Conversation, "uuid">;
export type UpdateConversation = Omit<Conversation, "messages">;
export type DeleteConversation = Pick<Conversation, "uuid">;
