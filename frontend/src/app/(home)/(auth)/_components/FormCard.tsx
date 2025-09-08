import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import Link from "next/link";
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
		<Card className={ cn("max-auto w-[95%] max-w-md", className) }>
			<CardHeader>
				<CardTitle>{ title }</CardTitle>
				<CardDescription>{ description }</CardDescription>
			</CardHeader>
			<CardContent className="space-y-2">
				{ children }
				{ /* TODO: Add the privacy policy link */ }

				<div className="flex items-center">
					<hr className="flex-grow border-t border-gray-300" />
					<span className="px-3 text-gray-400">or</span>
					<hr className="flex-grow border-t border-gray-300" />
				</div>
			</CardContent>

			<CardFooter className="flex w-full flex-col items-center justify-center space-y-4">
				<SocialLogin />
				<div>
					<p className="text-xs text-gray-400">
						By continuing, you acknowledge VitalMind Insight&nbsp;s{ " " }
						<Link
							href="#"
							className="hover:text-bold hover:text-primary text-gray-800 transition-all duration-300 hover:underline"
						>
							Privacy Policy
						</Link>
						.
					</p>
				</div>
			</CardFooter>
		</Card>
	);
};
