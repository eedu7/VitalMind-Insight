import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
	createConversation,
	deleteConversation,
	getAllConversation,
	getConversationById,
	updateConversation,
} from "./api";
import { UpdateConversation } from "./types";

export function useConversations({ conversationId }: { conversationId?: string }) {
	const queryClient = useQueryClient();
	const getAll = useQuery({
		queryKey: ["getAllConversations"],
		queryFn: getAllConversation,
	});

	const getById = useQuery({
		queryKey: ["getConversation", conversationId],
		queryFn: async () => {
			await getConversationById({ conversationId: conversationId! });
		},
		enabled: !!conversationId,
	});

	const create = useMutation({
		mutationKey: ["createConversation"],
		mutationFn: createConversation,
	});

	const update = useMutation({
		mutationKey: ["updateconversation", conversationId],
		mutationFn: async (data: UpdateConversation) =>
			await updateConversation({ ...data, conversationId: conversationId! }),
	});

	const removeConversation = useMutation({
		mutationKey: ["deleteConversation", conversationId],
		mutationFn: deleteConversation,
	});

	return {
		getAll,
		getById,
		create,
		update,
		removeConversation,
	};
}
