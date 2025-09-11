import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { IconAdjustmentsHorizontal, IconPlus } from "@tabler/icons-react";

interface Props {
	prompt: string;
	setPrompt: (val: string) => void;
	onSubmit: () => void;
	isPending: boolean;
	className?: string;
}

export const PromptInputField = ({ prompt, setPrompt, onSubmit, className, isPending }: Props) => {
	return (
		<form
			onSubmit={(e: React.FormEvent) => {
				e.preventDefault();
				e.stopPropagation();
				onSubmit();
			}}
			className={cn("w-full p-2 ", className)}
		>
			<div className="space-y-2 rounded-lg border p-2 shadow shadow-orange-200 outline">
				<Textarea
					value={prompt}
					onChange={(e) => setPrompt(e.target.value)}
					className="max-h-64 min-h-[3rem] w-full resize-y overflow-y-auto border-none shadow-none outline-none focus-visible:ring-0"
					placeholder="How can I help you today?"
				/>
				<div className="flex items-center justify-between px-3 py-1">
					<div className="space-x-2">
						<Button variant="outline" size="icon" className="size-8" disabled>
							<IconPlus />
						</Button>
						<Button variant="outline" size="icon" className="size-8" disabled>
							<IconAdjustmentsHorizontal />
						</Button>
					</div>
					<div>
						<Button variant="outline" type="submit" disabled={isPending || prompt === ""}>
							Send
						</Button>
					</div>
				</div>
			</div>
		</form>
	);
};
