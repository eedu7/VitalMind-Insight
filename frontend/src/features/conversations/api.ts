import apiClient from "@/lib/api";
import { Conversation } from "./types";

const CONVERSATION_URL = "/api/conversation";

export async function getAllConversation(): Promise<Conversation[]> {
	const res = await apiClient.get<Conversation[]>(`${CONVERSATION_URL}/`);
	return res.data;
}
