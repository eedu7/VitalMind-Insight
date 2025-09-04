import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getAllConversationApi } from "./api";

export function useConversations() {
	const queryClient = useQueryClient();

	const allConversationsQuery = useQuery({
		queryKey: ["getAllConversations"],
		queryFn: getAllConversationApi,
	});



	return {
		allConversationsQuery,
	};
}
