import { Button } from "@/components/ui/button";
import { categories } from "../categories";

export const QuickPrompts = () => {
	return (
		<div className="flex flex-wrap items-center justify-center gap-1 md:gap-2">
			{categories.map(({ title, icon: Icon }) => (
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
	);
};
