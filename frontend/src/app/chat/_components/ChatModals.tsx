"use client";

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useConversationActions } from "@/features/conversations";

export const ChatModals = () => {
	const { action, targetId, title, isOpen, closeModal } = useConversationActions();

	if (!isOpen || !action || !targetId || !title) return null;

	switch (action) {
		case "rename":
			return <RenameModal chatId={targetId} chatTitle={title} closeModal={closeModal} isOpen={isOpen} />;

		case "delete":
			return (
				<DeleteConfirmationModal chatId={targetId} chatTitle={title} closeModal={closeModal} isOpen={isOpen} />
			);

		case "share":
			return <ShareModal chatId={targetId} chatTitle={title} closeModal={closeModal} isOpen={isOpen} />;

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

const RenameModal = ({ chatId, chatTitle, isOpen, closeModal }: ModalProps) => {
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
				<h1 className="text-xl font-bold hover:transform-3d">Rename</h1>

				<div>ChatId: {chatId}</div>
				<div>ChatId: {chatTitle}</div>
			</DialogContent>
		</Dialog>
	);
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

const ShareModal = ({ chatId, chatTitle, isOpen, closeModal }: ModalProps) => {
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
				<h1 className="text-xl font-bold hover:transform-3d">Share</h1>
				<div>ChatId: {chatId}</div>
				<div>ChatId: {chatTitle}</div>
			</DialogContent>
		</Dialog>
	);
};
