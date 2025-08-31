interface Props {
	params: Promise<{ chatId: string }>;
}

export default async function page({ params }: Props) {
	const { chatId } = await params;
	return <div>ChatId: {chatId}</div>;
}
