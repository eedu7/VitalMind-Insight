import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getAllConversation } from "./api";

export function useConversations() {
	const queryClient = useQueryClient();

	const allConversationsQuery = useQuery({
		queryKey: ["getAllConversations"],
		queryFn: getAllConversation,
	});

	return {
		allConversationsQuery,
	};
}
