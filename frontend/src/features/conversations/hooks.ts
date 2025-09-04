import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { deleteConversationApi, getAllConversationApi, getConversationByIdApi, updateConversationApi } from "./api";

export function useConversations() {
	const queryClient = useQueryClient();

	const allConversationsQuery = useQuery({
		queryKey: ["getAllConversations"],
		queryFn: getAllConversationApi,
	});

	const getConversationById = (conversationId: string) => {
		return useQuery({
			queryKey: ["getConversationById", conversationId],
			queryFn: async () => {
				await getConversationByIdApi({ uuid: conversationId });
			},
		});
	};

	const updateConversation = useMutation({
		mutationKey: ["updateConversation"],
		mutationFn: updateConversationApi,
		onSuccess: () => {
			queryClient.invalidateQueries({
				queryKey: ["getAllConversations"],
			});
		},
	});

	const deleteConversation = useMutation({
		mutationKey: ["deleteConversation"],
		mutationFn: deleteConversationApi,
		onSuccess: () => {},
	});

	return {
		allConversationsQuery,
		getConversationById,
		updateConversation,
		deleteConversation,
	};
}
