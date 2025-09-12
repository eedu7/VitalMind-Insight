export type MessageRoleType = "user" | "assistant" | "system" | "tool";

export type Message = {
	role: MessageRoleType;
	content: string;
};
