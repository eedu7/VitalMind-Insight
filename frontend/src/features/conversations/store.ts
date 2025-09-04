import { create } from "zustand";

type ActionType = "rename" | "delete" | "share";

interface ConversationActionState {
	targetId: string | null;
	title: string | null;
	action: ActionType | null;
	isOpen: boolean;
	setAction: (id: string, title: string, action: ActionType) => void;
	closeModal: () => void;
}

export const useConversationActions = create<ConversationActionState>((set) => ({
	targetId: null,
	title: null,
	action: null,
	isOpen: false,
	setAction: (id, title, action) => set({ targetId: id, action, title, isOpen: true }),
	closeModal: () => set({ targetId: null, action: null, isOpen: false }),
}));
