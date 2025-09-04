"use client";

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useConversationActions } from "@/features/conversations";

export const ChatModals = () => {
	const { action, targetId, title, isOpen, closeModal } = useConversationActions();

	if (!isOpen || !action || !targetId || !title) return null;

	switch (action) {
		case "rename":
			break;

		case "delete":
			return (
				<DeleteConfirmationModal chatId={targetId} chatTitle={title} closeModal={closeModal} isOpen={isOpen} />
			);

		case "share":
			break;

		default:
			break;
	}
};

interface ModalProps {
	chatId: string;
	chatTitle: string;
	isOpen: boolean;
	closeModal: () => void;
}

const RenameModal = () => {
	return <div>Delete Confirmation modal</div>;
};

const DeleteConfirmationModal = ({ chatId, chatTitle, isOpen, closeModal }: ModalProps) => {
	return (
		<Dialog open={isOpen} onOpenChange={closeModal}>
			<DialogContent>
				<DialogHeader>
					<DialogTitle>Are you absolutely sure?</DialogTitle>
					<DialogDescription>
						This action cannot be undone. This will permanently delete your account and remove your data
						from our servers.
					</DialogDescription>
				</DialogHeader>
				<div>ChatId: {chatId}</div>
				<div>ChatId: {chatTitle}</div>
			</DialogContent>
		</Dialog>
	);
};

const ShareModal = () => {
	return <div>Share Modal</div>;
};
