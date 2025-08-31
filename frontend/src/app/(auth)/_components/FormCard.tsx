import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import React from "react";

interface Props {
	title: string;
	className?: string;
	description: string;
	children: React.ReactNode;
}

export const FormCard = ({ title, className, description, children }: Props) => {
	return (
		<Card className={cn("w-[95%] md:w-[384px]", className)}>
			<CardHeader>
				<CardTitle>{title}</CardTitle>
				<CardDescription>{description}</CardDescription>
			</CardHeader>
			<CardContent>{children}</CardContent>
			<Footer />
		</Card>
	);
};

const Footer = () => {
	return <CardFooter className="text-xs text-blue-500"></CardFooter>;
};
