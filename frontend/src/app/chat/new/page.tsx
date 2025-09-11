import { Button } from "@/components/ui/button";
import { PromptInputField } from "@/features/prompt-input-field";
import { cn } from "@/lib/utils";
import { IconBulb, IconCoffee, IconHeart, IconPencil, IconSchool, TablerIcon } from "@tabler/icons-react";
import { Merriweather_Sans } from "next/font/google";

const merriweatherSans = Merriweather_Sans({
	variable: "--font-merriweather-sans",
	subsets: ["latin"],
});

type Option = {
	title: string;
	icon: TablerIcon;
};

const options: Option[] = [
	{
		title: "Write",
		icon: IconPencil,
	},
	{
		title: "Learn",
		icon: IconSchool,
	},

	{
		title: "Life stuff",
		icon: IconCoffee,
	},
	{
		title: "Our choice",
		icon: IconBulb,
	},
	{
		title: "Ideas",
		icon: IconBulb,
	},
	{
		title: "Design",
		icon: IconPencil,
	},
	{
		title: "Health",
		icon: IconHeart,
	},
	{
		title: "Explore",
		icon: IconSchool,
	},
];

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
				<PromptInputField />
				<div className="flex flex-wrap items-center justify-center gap-1 md:gap-2">
					{options.map(({ title, icon: Icon }) => (
						<Button
							variant="outline"
							key={title}
							className="flex transform items-center transition-transform hover:scale-105 hover:-rotate-1"
							disabled
						>
							<Icon />
							<span>{title}</span>
						</Button>
					))}
				</div>
			</div>
		</div>
	);
}
