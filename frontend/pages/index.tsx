import { Geist, Geist_Mono } from "next/font/google";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function Home() {
  return (
    <div
      className={`${geistSans.className} ${geistMono.className} font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center`}
    >
      <main className="flex flex-col justify-center align-middle row-start-2 items-center sm:items-start">
        <h1>PathOn AI Takehome Project</h1>

        <SignedOut>
          <div className="w-full flex justify-center align-middle items-center">
            <Button>
              <SignInButton />
            </Button>
          </div>
        </SignedOut>
        <SignedIn>
          <div className="w-full flex justify-center align-middle items-center gap-x-2">
            <UserButton />
            <Link href="/manage-jobs" className="text-cyan-600 underline hover:cursor-pointer">
              Train some models
            </Link>
          </div>
        </SignedIn>
      </main>
    </div>
  );
}
