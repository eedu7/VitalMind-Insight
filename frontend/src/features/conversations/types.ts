import { Message } from "../messages";

export type Conversation = {
	uuid: string;
	title: string;
	messages?: Message[];
};

export type DeleteConversation = Pick<Conversation, "uuid">;
