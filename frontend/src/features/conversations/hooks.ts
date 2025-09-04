import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { deleteConversationApi, getAllConversationApi, updateConversationApi } from "./api";

export function useConversations() {
	const queryClient = useQueryClient();

	const allConversationsQuery = useQuery({
		queryKey: ["getAllConversations"],
		queryFn: getAllConversationApi,
	});

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
		updateConversation,
		deleteConversation,
	};
}
