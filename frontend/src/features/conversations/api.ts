import apiClient from "@/lib/api";
import { DeleteResponse, UpdateResponse } from "../types";
import { Conversation, DeleteConversation, UpdateConversation } from "./types";

const CONVERSATION_URL = "/api/conversation";

export async function getAllConversationApi(): Promise<Conversation[]> {
	const res = await apiClient.get<Conversation[]>(`${CONVERSATION_URL}/`);
	return res.data;
}

export async function updateConversationApi({ title, uuid }: UpdateConversation): Promise<UpdateResponse> {
	const res = await apiClient.put<UpdateResponse>(`${CONVERSATION_URL}/${uuid}`, {
		title,
	});
	return res.data;
}

export async function deleteConversationApi({ uuid }: DeleteConversation): Promise<DeleteResponse> {
	const res = await apiClient.delete<DeleteResponse>(`${CONVERSATION_URL}/${uuid}`);
	return res.data;
}
