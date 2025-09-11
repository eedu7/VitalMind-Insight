"use client";
import { Prompt } from "@/features/prompts";
import { cn } from "@/lib/utils";
import { Merriweather_Sans } from "next/font/google";

const merriweatherSans = Merriweather_Sans({
	variable: "--font-merriweather-sans",
	subsets: ["latin"],
});

export default function Page() {
	return (
		<div className="mx-auto grid h-screen place-items-center p-2 md:max-w-2xl lg:max-w-4xl">
			<div className="flex h-full w-full flex-col items-center justify-center gap-y-8">
				<div>
					<h1
						className={cn(
							"text-center text-2xl font-bold tracking-wide md:text-4xl lg:tracking-wider",
							merriweatherSans.className
						)}
					>
						Ready when you are.
					</h1>
				</div>
				<Prompt />
			</div>
		</div>
	);
}
