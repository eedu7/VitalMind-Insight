import { NextRequest, NextResponse } from "next/server";

const PUBLIC_ROUTES = ["/login", "/register"];
const EXCLUDED_PATHS = ["/_next", "/favicon.ico"];

const isPublicRoute = (pathname: string) => PUBLIC_ROUTES.some((route) => pathname.startsWith(route));

const isExcludedPath = (pathname: string) =>
	EXCLUDED_PATHS.some((path) => pathname.startsWith(path)) || pathname.includes(".");

export async function middleware(req: NextRequest) {
	// const { pathname } = req.nextUrl;

	// if (isExcludedPath(pathname)) {
	// 	return NextResponse.next();
	// }
	// const token = req.cookies.get("access_token")?.value;
	// if (token) {
	// 	return NextResponse.next();
	// }

	// if (isPublicRoute(pathname) || pathname === "/") {
	// 	return NextResponse.next();
	// }

	// const loginUrl = new URL("/login", req.url);
	// return NextResponse.redirect(loginUrl);
	return NextResponse.next();
}

export const config = {
	matcher: [
		/*
		 * Match all paths except:
		 * - API routes: /api/*
		 * - static files: /_next/* and files with extensions
		 */
		"/((?!api|_next/static|_next/image|favicon.ico).*)",
	],
};
