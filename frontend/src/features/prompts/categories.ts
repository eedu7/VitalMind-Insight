import { IconBulb, IconCoffee, IconHeart, IconPencil, IconSchool, TablerIcon } from "@tabler/icons-react";

export type QuickPromptCategory = {
	title: string;
	icon: TablerIcon;
};

export const categories: QuickPromptCategory[] = [
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
