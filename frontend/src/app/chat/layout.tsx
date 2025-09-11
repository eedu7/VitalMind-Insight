import { SidebarProvider } from "@/components/ui/sidebar";
import React from "react";
import { AppSidebar } from "./_components/AppSidebar";

interface LayoutProps {
	children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
	return (
		<SidebarProvider defaultOpen={false}>
			<AppSidebar />
			<main className="mx-auto w-full max-w-lg sm:max-w-xl md:max-w-2xl lg:max-w-4xl">{children}</main>
		</SidebarProvider>
	);
}
