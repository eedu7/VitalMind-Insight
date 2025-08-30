import React from "react";

interface LayoutProps {
	child: React.ReactNode;
}

export default function Layout({ child }: LayoutProps) {
	return (
		<div>
			<main className="h-4 w-4 border bg-green-500 text-blue-500 shadow-lg">{child}</main>
		</div>
	);
}
