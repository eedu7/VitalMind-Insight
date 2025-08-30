import React from "react";

interface LayoutProps {
	children: React.ReactElement;
}

export default function Layout({ children }: LayoutProps) {
	return (
		<div className="flex h-screen flex-col">
			<main className="flex h-full flex-1 items-center justify-center">{children}</main>
		</div>
	);
}
