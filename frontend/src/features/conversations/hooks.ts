import { useQuery, useQueryClient } from "@tanstack/react-query";

export function useConversations({ conversationId }: { conversationId: string }) {
    const queryClient = useQueryClient()
    const getAll = useQuery({
        queryKey: ["getAllConversations"],
        queryFn: 
    })


}
