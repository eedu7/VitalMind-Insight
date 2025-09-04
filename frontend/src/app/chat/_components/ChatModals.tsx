"use client";

import { useConversationActions } from "@/features/conversations";

const ChatModals = () => {
	const { action, targetId, title, isOpen, closeModal } = useConversationActions();

	if (!isOpen || !action || !targetId || !title) return null;

	switch (action) {
		case "rename":
			break;

		case "delete":
			break;

		case "share":
			break;

		default:
			break;
	}
};

const RenameModal = () => {
	return <div>Rename modal</div>;
};

const DeleteConfirmationModal = () => {
	return <div>Delete Confirmation modal</div>;
};

const ShareModal = () => {
	return <div>Share Modal</div>;
};
