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
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { useConversationActions, useConversations } from "@/features/conversations";
import { useState } from "react";

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

const RenameModal = ({ isOpen, closeModal, chatTitle, chatId }: ModalProps) => {
	const [value, setValue] = useState(chatTitle);

	const { updateConversation } = useConversations();

	const onSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		e.stopPropagation();
		updateConversation.mutateAsync({
			title: value,
			uuid: chatId,
		});
		closeModal();
	};

	return (
		<Dialog open={isOpen} onOpenChange={closeModal}>
			<DialogContent>
				<DialogHeader>
					<DialogTitle>Edit chat title</DialogTitle>
				</DialogHeader>
				<form onSubmit={onSubmit} className="space-y-4">
					<div className="space-y-2">
						<Label>Chat Title</Label>
						<Input placeholder="Edit title" value={value} onChange={(e) => setValue(e.target.value)} />
					</div>
					<div className="flex w-full justify-end gap-x-2">
						<Button type="button" variant="outline" onClick={closeModal}>
							Cancel
						</Button>
						<Button>Update</Button>
					</div>
				</form>
			</DialogContent>
		</Dialog>
	);
};

const DeleteConfirmationModal = ({ chatId, isOpen, closeModal }: ModalProps) => {
	const { deleteConversation } = useConversations();

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
					<AlertDialogAction onClick={() => deleteConversation.mutateAsync({ uuid: chatId })}>
						Continue
					</AlertDialogAction>
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
