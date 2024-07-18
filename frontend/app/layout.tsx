import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "./markdown.css";

const inter = Inter({ subsets: ["latin"] });

//export const dynamic = "force-dynamic";
//export const revalidate = true;

export const metadata: Metadata = {
  title: "McKesson Fiscal Navigator",
  description: "Powered By EXL",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
