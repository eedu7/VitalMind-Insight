"use client";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { MailIcon, User } from "lucide-react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import z from "zod";
import IconInput from "../../_components/ui/IconInput";
import { PasswordInput } from "../../_components/ui/PasswordInput";

const registerFormSchema = z.object({
	username: z
		.string()
		.min(3, "Username must be at least 3 characters")
		.max(20, "Username must be at most 20 characters"),
	email: z.string().email("Invalid email address"),
	password: z
		.string()
		.min(6, "Password must be at least 6 characters")
		.max(100, "Password must be at most 100 characters"),
});

export const RegisterForm = () => {
	const form = useForm<z.infer<typeof registerFormSchema>>({
		resolver: zodResolver(registerFormSchema),
		defaultValues: {
			username: "",
			password: "",
			email: "",
		},
	});

	const onSubmit = async (values: z.infer<typeof registerFormSchema>) => {
		console.table(values);
	};
	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
				<FormField
					control={form.control}
					name="username"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Username</FormLabel>
							<FormControl>
								<IconInput icon={User} {...field} placeholder="Enter your username" />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
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

				<Button className="w-full">Register</Button>
				<div className="w-full text-center">
					<Link href="/login" className="text-muted-foreground hover:text-primary text-sm">
						Have an account? Login
					</Link>
				</div>
			</form>
		</Form>
	);
};
