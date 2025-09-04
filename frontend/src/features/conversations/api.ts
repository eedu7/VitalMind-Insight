import apiClient from "@/lib/api";
import { Conversation, DeleteConversation } from "./types";

const CONVERSATION_URL = "/api/conversation";

export async function getAllConversationApi(): Promise<Conversation[]> {
	const res = await apiClient.get<Conversation[]>(`${CONVERSATION_URL}/`);
	return res.data;
}

export async function deleteConversationApi({ uuid }: DeleteConversation) {
	const res = await apiClient.delete(`${CONVERSATION_URL}/${uuid}`);
	return res.data;
}
