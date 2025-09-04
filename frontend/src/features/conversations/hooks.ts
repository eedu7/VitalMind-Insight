import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { deleteConversationApi, getAllConversationApi } from "./api";
import { DeleteConversation } from "./types";

export function useConversations() {
	const queryClient = useQueryClient();

	const allConversationsQuery = useQuery({
		queryKey: ["getAllConversations"],
		queryFn: getAllConversationApi,
	});

	const deleteConversation = useMutation({
		mutationKey: ["deleteConversation"],
		mutationFn: async ({ uuid }: DeleteConversation) => await deleteConversationApi({ uuid }),
		onSuccess: () => {
			queryClient.invalidateQueries({
				queryKey: ["getAllConversations"],
			});
		},
	});

	return {
		allConversationsQuery,
		deleteConversation,
	};
}
