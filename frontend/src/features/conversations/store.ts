import { create } from "zustand";

type ActionType = "reanme" | "delete" | "share";

interface ConversationActionState {
	targetId: string | null;
	action: ActionType | null;
	isOpen: boolean;
	setAction: (id: string, action: ActionType) => void;
	closeModal: () => void;
}

export const useConversationActions = create<ConversationActionState>((set) => ({
	targetId: null,
	action: null,
	isOpen: false,
	setAction: (id, action) => set({ targetId: id, action: action, isOpen: true }),
	closeModal: () => set({ targetId: null, action: null, isOpen: false }),
}));
