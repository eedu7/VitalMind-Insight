import apiClient from "@/lib/api";
import { DeleteResponse, UpdateResponse } from "../types";
import { Conversation, CreateConversation, DeleteConversation, GetChatByID, UpdateConversation } from "./types";

const CHAT_URL = "/api/conversation";

export async function getAllChats(): Promise<Conversation[]> {
	const res = await apiClient.get<Conversation[]>(`${CHAT_URL}/`);
	return res.data;
}

export async function getChatById({ chatId }: GetChatByID): Promise<Conversation> {
	const res = await apiClient.get<Conversation>(`${CHAT_URL}/${chatId}`);
	return res.data;
}

export async function createConversation(data: CreateConversation): Promise<Conversation> {
	const res = await apiClient.post<Conversation>(`${CHAT_URL}/`, data);
	return res.data;
}

export async function updateConversation(data: UpdateConversation): Promise<UpdateResponse> {
	const res = await apiClient.put<UpdateResponse>(`${CHAT_URL}/`, data);
	return res.data;
}

export async function deleteConversation({ chatId }: DeleteConversation): Promise<DeleteResponse> {
	const res = await apiClient.delete<DeleteResponse>(`${CHAT_URL}/${chatId}`);
	return res.data;
}
