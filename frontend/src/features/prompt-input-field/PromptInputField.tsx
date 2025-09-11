import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { IconAdjustmentsHorizontal, IconPlus } from "@tabler/icons-react";

interface Props {
	className?: string;
}

export const PromptInputField = ({ className }: Props) => {
	return (
		<div className={cn("w-full max-w-4xl", className)}>
			<div className="space-y-4 rounded-lg border p-2 shadow shadow-orange-200 outline">
				<Textarea
					className="max-w-full border-none shadow-none outline-none focus-visible:ring-0"
					placeholder="How can I help you today?"
				/>
				<div className="flex items-center justify-between px-3 py-1">
					<div className="space-x-2">
						<Button variant="outline" size="icon" className="size-8">
							<IconPlus />
						</Button>
						<Button variant="outline" size="icon" className="size-8">
							<IconAdjustmentsHorizontal />
						</Button>
					</div>
					<div>
						<Button variant="outline">Send</Button>
					</div>
				</div>
			</div>
		</div>
	);
};
