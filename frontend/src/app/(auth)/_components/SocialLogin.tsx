import { Button } from "@/components/ui/button";
import { RiFacebookFill, RiGithubFill, RiGoogleFill, RiTwitterXFill } from "@remixicon/react";

export const SocialLogin = () => {
	return (
		<div className="flex flex-wrap gap-2">
			<Button className="flex-1" variant="outline" aria-label="Login with Google" size="icon" disabled>
				<RiGoogleFill className="dark:text-primary text-[#DB4437]" size={16} aria-hidden="true" />
			</Button>
			<Button className="flex-1" variant="outline" aria-label="Login with Facebook" size="icon" disabled>
				<RiFacebookFill className="dark:text-primary text-[#1877f2]" size={16} aria-hidden="true" />
			</Button>
			<Button className="flex-1" variant="outline" aria-label="Login with X" size="icon" disabled>
				<RiTwitterXFill className="dark:text-primary text-[#14171a]" size={16} aria-hidden="true" />
			</Button>
			<Button className="flex-1" variant="outline" aria-label="Login with GitHub" size="icon" disabled>
				<RiGithubFill className="dark:text-primary text-black" size={16} aria-hidden="true" />
			</Button>
		</div>
	);
};
