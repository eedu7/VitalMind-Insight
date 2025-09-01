import { Card, CardContent } from "@/components/ui/card";
import * as TablerIcon from "@tabler/icons-react";

const iconsList = [
	{
		icon: TablerIcon.IconEdit,
		name: "IconEdit",
	},
	{
		icon: TablerIcon.IconEditOff,
		name: "IconEditOff",
	},
	{
		icon: TablerIcon.IconEditCircle,
		name: "IconEditCircle",
	},
	{
		icon: TablerIcon.IconEditCircleOff,
		name: "IconEditCircleOff",
	},
	{
		icon: TablerIcon.IconPencilExclamation,
		name: "IconPencilExclamation",
	},
	{
		icon: TablerIcon.IconPencilCancel,
		name: "IconPencilCancel",
	},
	{
		icon: TablerIcon.IconPencilHeart,
		name: "IconPencilHeart",
	},
	{
		icon: TablerIcon.IconPencil,
		name: "IconPencil",
	},
	{
		icon: TablerIcon.IconPencilSearch,
		name: "IconPencilSearch",
	},
	{
		icon: TablerIcon.IconSearch,
		name: "IconSearch",
	},
	{
		icon: TablerIcon.IconSearchOff,
		name: "IconSearchOff",
	},
	{
		icon: TablerIcon.IconEyeSearch,
		name: "IconEyeSearch",
	},
	{
		icon: TablerIcon.IconMapSearch,
		name: "IconMapSearch",
	},
];

export default function Page() {
	return (
		<div className="flex h-screen w-full items-center justify-center border p-4 shadow-md">
			<div className="grid grid-cols-6 gap-4">
				{iconsList.map(({ icon: Icon, name }, index) => (
					<IconCard key={index} name={name}>
						<Icon />
					</IconCard>
				))}
			</div>
		</div>
	);
}

const IconCard = ({ children, name }: { children: React.ReactElement; name: string }) => {
	return (
		<Card className="transform cursor-pointer opacity-70 transition-all duration-300 ease-in-out hover:translate-x-1.5 hover:translate-y-1 hover:opacity-100 hover:shadow-lg">
			<CardContent className="flex flex-col items-center justify-center gap-2">
				{children}
				<small className="text-xs">{name}</small>
			</CardContent>
		</Card>
	);
};
