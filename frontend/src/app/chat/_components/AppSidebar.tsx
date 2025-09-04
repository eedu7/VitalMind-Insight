"use client";
import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarGroup,
	SidebarGroupContent,
	SidebarGroupLabel,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuAction,
	SidebarMenuButton,
	SidebarMenuItem,
	SidebarTrigger,
	useSidebar,
} from "@/components/ui/sidebar";
import Link from "next/link";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuGroup,
	DropdownMenuItem,
	DropdownMenuLabel,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { useAuth } from "@/features/auth";
import { useConversations } from "@/features/conversations";
import {
	IconCreditCard,
	IconDotsVertical,
	IconEdit,
	IconLogout,
	IconPencil,
	IconSearch,
	IconShare,
	IconTrash,
	IconUserCircle,
} from "@tabler/icons-react";
import { Loader2, MoreHorizontal } from "lucide-react";
import React from "react";

export const AppSidebar = () => {
	return (
		<Sidebar collapsible="icon">
			<SidebarHeader className="gap-0 p-0">
				<SidebarHeaderSection />
			</SidebarHeader>

			<SidebarContent className="flex flex-col gap-6 overflow-hidden">
				<ChatActionGroup />
				<ChatSidebarGroup />
			</SidebarContent>
			<SidebarFooter>
				<UserAccountGroup />
			</SidebarFooter>
		</Sidebar>
	);
};

const SidebarHeaderSection = () => {
	return (
		<SidebarGroup>
			<SidebarGroupContent>
				<SidebarMenu>
					<SidebarMenuItem className="cursor-pointer">
						<SidebarMenuButton asChild className="hover:bg-transparent">
							<div className="flex w-full items-center justify-start gap-2">
								<SidebarTrigger />
								<Link href="/chat/new">VitalMind</Link>
							</div>
						</SidebarMenuButton>
					</SidebarMenuItem>
				</SidebarMenu>
			</SidebarGroupContent>
		</SidebarGroup>
	);
};

const ChatActionGroup = () => {
	return (
		<SidebarGroup>
			<SidebarGroupLabel>Actions</SidebarGroupLabel>
			<SidebarGroupContent>
				<SidebarMenu>
					<SidebarMenuItem>
						<SidebarMenuButton asChild>
							<Link prefetch={false} href="/chat/new">
								<IconEdit />
								<span>New chat</span>
							</Link>
						</SidebarMenuButton>
					</SidebarMenuItem>
					<SidebarMenuItem>
						<SidebarMenuButton asChild>
							{/* TODO: Add proper url */}
							<Link prefetch={false} href="#">
								<IconSearch />
								<span>Search chat</span>
							</Link>
						</SidebarMenuButton>
					</SidebarMenuItem>
				</SidebarMenu>
			</SidebarGroupContent>
		</SidebarGroup>
	);
};

const ChatSidebarGroup = () => {
	return (
		<SidebarGroup className="flex-1 overflow-hidden">
			<SidebarGroupLabel>Chats</SidebarGroupLabel>
			<ScrollArea className="h-full">
				<SidebarGroupContent className="h-full">
					<SidebarMenu className="space-y-2">
						<ChatListContent />
					</SidebarMenu>
				</SidebarGroupContent>
				<ScrollBar orientation="vertical" />
			</ScrollArea>
		</SidebarGroup>
	);
};

const ChatListContent = () => {
	const { allConversationsQuery } = useConversations();
	const { state } = useSidebar();

	if (state === "collapsed") return null;

	if (allConversationsQuery.isPending) {
		return (
			<div className="flex items-center justify-between p-2">
				<span>Loading...</span>
				<Loader2 className="animate-spin" />
			</div>
		);
	}
	if (allConversationsQuery.isError) {
		return <div className="p-2 text-red-500">Failed to load chats</div>;
	}

	if (!allConversationsQuery.data?.length) {
		return <div className="text-muted-foreground p-2">No chats yet</div>;
	}

	return allConversationsQuery.data?.map((conversation) => (
		<SidebarMenuItem key={conversation.uuid} className="group/item">
			<SidebarMenuButton asChild>
				<Link prefetch={false} href={`/chat/${conversation.uuid}`}>
					{conversation.title}
				</Link>
			</SidebarMenuButton>
			<ChatActionDropDown chatId={conversation.uuid} chatTitle={conversation.title} />
		</SidebarMenuItem>
	));
};

const ChatActionDropDown = ({ chatId, chatTitle }: { chatId: string; chatTitle: string }) => {
	const handleAction = (e: React.MouseEvent<HTMLDivElement>) => {
		const target = e.target as HTMLElement;

		const actionBtn = target.closest<HTMLElement>("[data-action]");

		const action = actionBtn?.dataset.action;

		if (action === "edit") {
			alert(`Edit: ${chatTitle} ${chatId}`);
		}
		if (action === "delete") {
			alert(`Delete: ${chatTitle} ${chatId}`);
		}
		if (action === "share") {
			alert(`Share: ${chatTitle} ${chatId}`);
		}
	};

	return (
		<div
			className="opacity-100 transition-opacity duration-200 group-hover/item:opacity-100 md:opacity-0"
			onClick={handleAction}
		>
			<DropdownMenu>
				<DropdownMenuTrigger asChild className="mx-2 cursor-pointer">
					<SidebarMenuAction>
						<MoreHorizontal />
					</SidebarMenuAction>
				</DropdownMenuTrigger>
				<DropdownMenuContent side="right" align="start">
					<DropdownMenuItem data-action="edit">
						<IconPencil />
						<span>Rename</span>
					</DropdownMenuItem>
					<DropdownMenuItem data-action="delete">
						<IconTrash />
						<span>Delete</span>
					</DropdownMenuItem>
					<DropdownMenuSeparator />
					<DropdownMenuItem data-action="share">
						<IconShare />
						<span>Share</span>
					</DropdownMenuItem>
				</DropdownMenuContent>
			</DropdownMenu>
		</div>
	);
};

const UserAccountGroup = () => {
	const { logout } = useAuth();

	return (
		<SidebarMenu>
			<SidebarMenuItem>
				<DropdownMenu>
					<DropdownMenuTrigger asChild>
						<SidebarMenuButton
							size="lg"
							className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
						>
							<Avatar className="h-8 w-8 rounded-lg">
								<AvatarImage src={"https://github.com/shadcn.png"} alt={"shadcn"} />
								<AvatarFallback className="rounded-lg">CN</AvatarFallback>
							</Avatar>
							<div className="grid flex-1 text-left text-sm leading-tight">
								<span className="truncate font-medium">shadcn</span>
								<span className="text-muted-foreground truncate text-xs">m@example.com</span>
							</div>
							<IconDotsVertical className="ml-auto size-4" />
						</SidebarMenuButton>
					</DropdownMenuTrigger>
					<DropdownMenuContent
						className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
						side="top"
						align="end"
						sideOffset={4}
					>
						<DropdownMenuLabel className="p-0 font-normal">
							<div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
								<Avatar className="h-8 w-8 rounded-lg">
									<AvatarImage src={"https://github.com/shadcn.png"} alt="shadcn" />
									<AvatarFallback className="rounded-lg">CN</AvatarFallback>
								</Avatar>
								<div className="grid flex-1 text-left text-sm leading-tight">
									<span className="truncate font-medium">shadcn</span>
									<span className="text-muted-foreground truncate text-xs">m@example.com</span>
								</div>
							</div>
						</DropdownMenuLabel>
						<DropdownMenuSeparator />
						<DropdownMenuGroup>
							<DropdownMenuItem>
								<IconUserCircle />
								Account
							</DropdownMenuItem>
							<DropdownMenuItem>
								<IconCreditCard />
								Billing
							</DropdownMenuItem>
						</DropdownMenuGroup>
						<DropdownMenuSeparator />
						<DropdownMenuItem onClick={async () => logout.mutateAsync()}>
							<IconLogout />
							Log out
						</DropdownMenuItem>
					</DropdownMenuContent>
				</DropdownMenu>
			</SidebarMenuItem>
		</SidebarMenu>
	);
};
