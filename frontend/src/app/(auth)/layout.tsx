import React from "react";

interface LayoutProps {
	child: React.ReactNode;
}

export default function Layout({ child }: LayoutProps) {
	return (
		<div className="flex h-screen flex-col">
			<main className="flex-grow">{child}</main>
		</div>
	);
}
