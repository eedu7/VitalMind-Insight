import { PageView } from "./_components/PageView";

interface Props {
	params: Promise<{ chatId: string }>;
}

export default async function page({ params }: Props) {
	const { chatId } = await params;
	return <PageView chatId={chatId} />;
}
