"use client";
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from "@/components/ui/alert-dialog";
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
			return null;
	}
};

interface ModalProps {
	chatId: string;
	chatTitle: string;
	isOpen: boolean;
	closeModal: () => void;
}

const RenameModal = ({ isOpen, closeModal }: ModalProps) => {
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
			</DialogContent>
		</Dialog>
	);
};

const DeleteConfirmationModal = ({ isOpen, closeModal }: ModalProps) => {
	return (
		<AlertDialog open={isOpen} onOpenChange={closeModal}>
			<AlertDialogContent>
				<AlertDialogHeader>
					<AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
					<AlertDialogDescription>
						This action cannot be undone. This will permanently delete your account and remove your data
						from our servers.
					</AlertDialogDescription>
				</AlertDialogHeader>

				<AlertDialogFooter>
					<AlertDialogCancel>Cancel</AlertDialogCancel>
					<AlertDialogAction>Continue</AlertDialogAction>
				</AlertDialogFooter>
			</AlertDialogContent>
		</AlertDialog>
	);
};

const ShareModal = ({ isOpen, closeModal }: ModalProps) => {
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
			</DialogContent>
		</Dialog>
	);
};
