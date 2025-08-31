import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import React from "react";
import { SocialLogin } from "./SocialLogin";

interface Props {
	title: string;
	className?: string;
	description: string;
	children: React.ReactNode;
}

export const FormCard = ({ title, className, description, children }: Props) => {
	return (
		<Card className={cn("max-auto w-[95%] max-w-md", className)}>
			<CardHeader>
				<CardTitle>{title}</CardTitle>
				<CardDescription>{description}</CardDescription>
			</CardHeader>
			<CardContent>{children}</CardContent>
			<div className="flex items-center">
				<hr className="flex-grow border-t border-gray-300" />
				<span className="px-3 text-gray-500">OR</span>
				<hr className="flex-grow border-t border-gray-300" />
			</div>
			<CardFooter className="flex w-full justify-center">
				<SocialLogin />
			</CardFooter>
		</Card>
	);
};
