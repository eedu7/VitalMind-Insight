import apiClient from "@/lib/api";
import { DeleteResponse, UpdateResponse } from "../types";
import { Conversation, CreateConversation, DeleteConversation, GetConversationByID, UpdateConversation } from "./types";

const CONVERSATIONAL_URL = "/api/conversation";

export async function getAllConversation(): Promise<Conversation[]> {
	const res = await apiClient.get<Conversation[]>(`${CONVERSATIONAL_URL}/`);
	return res.data;
}

export async function getConversationById({ conversationId }: GetConversationByID): Promise<Conversation> {
	const res = await apiClient.get<Conversation>(`${CONVERSATIONAL_URL}/${conversationId}`);
	return res.data;
}

export async function createConversation(data: CreateConversation): Promise<Conversation> {
	const res = await apiClient.post<Conversation>(`${CONVERSATIONAL_URL}/`, data);
	return res.data;
}

export async function updateConversation({ conversationId, ...data }: UpdateConversation): Promise<UpdateResponse> {
	const res = await apiClient.put<UpdateResponse>(`${CONVERSATIONAL_URL}/${conversationId}`, data);
	return res.data;
}

export async function deleteConversation({ conversationId }: DeleteConversation): Promise<DeleteResponse> {
	const res = await apiClient.delete<DeleteResponse>(`${CONVERSATIONAL_URL}/${conversationId}`);
	return res.data;
}
