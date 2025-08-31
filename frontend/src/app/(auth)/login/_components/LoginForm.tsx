"use client";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { loginFormSchema, LoginFormValues, useAuth } from "@/features/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2, MailIcon } from "lucide-react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import z from "zod";
import IconInput from "../../_components/ui/IconInput";
import { PasswordInput } from "../../_components/ui/PasswordInput";

export const LoginForm = () => {
	const form = useForm<LoginFormValues>({
		resolver: zodResolver(loginFormSchema),
		defaultValues: {
			password: "",
			email: "",
		},
	});

	const { login } = useAuth();

	const onSubmit = async (values: z.infer<typeof loginFormSchema>) => {
		login.mutateAsync(values);
	};
	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
				<FormField
					control={form.control}
					name="email"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Email</FormLabel>
							<FormControl>
								<IconInput icon={MailIcon} {...field} placeholder="Enter your email address" />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="password"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Password</FormLabel>
							<FormControl>
								<PasswordInput {...field} placeholder="Password" />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>

				<Button className="w-full" disabled={login.isPending}>
					{login.isPending ? <Loader2 className="repeat-infinite animate-spin" /> : <span>Login</span>}
				</Button>
				<div className="flex w-full items-center justify-between">
					<Link href="#" className="text-muted-foreground hover:text-primary text-sm">
						Forget password
					</Link>
					<Link href="/register" className="text-muted-foreground hover:text-primary text-sm">
						New user? Register
					</Link>
				</div>
			</form>
		</Form>
	);
};
