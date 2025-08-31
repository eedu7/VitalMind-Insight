import { useId } from "react";

import { Input } from "@/components/ui/input";

interface Props extends React.InputHTMLAttributes<HTMLInputElement> {
	icon: React.ComponentType<{ size?: number; [key: string]: any }>;
}

export default function IconInput({ icon: Icon, ...props }: Props) {
	const id = useId();
	return (
		<div className="*:not-first:mt-2">
			<div className="relative">
				<Input id={id} className="peer ps-9" {...props} />
				<div className="text-muted-foreground/80 pointer-events-none absolute inset-y-0 start-0 flex items-center justify-center ps-3 peer-disabled:opacity-50">
					<Icon size={16} aria-hidden="true" />
				</div>
			</div>
		</div>
	);
}
