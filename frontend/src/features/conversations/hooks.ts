import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import {
	createConversationApi,
	deleteConversationApi,
	getAllConversationApi,
	getConversationByIdApi,
	updateConversationApi,
} from "./api";

export function useConversations() {
	const queryClient = useQueryClient();

	const router = useRouter();

	const allConversationsQuery = useQuery({
		queryKey: ["getAllConversations"],
		queryFn: getAllConversationApi,
	});

	const getConversationById = (conversationId: string) => {
		return useQuery({
			queryKey: ["getConversationById", conversationId],
			queryFn: () => getConversationByIdApi({ uuid: conversationId }),
			enabled: !!conversationId,
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
		onError: (err) => {
			toast.error(err.message);
		},
	});

	const deleteConversation = useMutation({
		mutationKey: ["deleteConversation"],
		mutationFn: deleteConversationApi,
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["getAllConversations"] });
		},
		onError: (err) => {
			toast.error(err.message);
		},
	});
	const createConversation = useMutation({
		mutationKey: ["createConversation"],
		mutationFn: createConversationApi,
		onSuccess: (data) => {
			queryClient.invalidateQueries({ queryKey: ["getAllConversations"] });
			router.push(`/chat/${data.uuid}`);
		},
		onError: (err) => {
			toast.error(err.message);
		},
	});

	return {
		allConversationsQuery,
		getConversationById,
		updateConversation,
		deleteConversation,
		createConversation,
	};
}
