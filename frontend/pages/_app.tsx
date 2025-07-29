import "@/styles/globals.css";
import {
  ClerkProvider,
} from "@clerk/nextjs";
import type { AppProps } from "next/app";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ClerkProvider
      {...pageProps}
      appearance={{
        cssLayerName: "clerk",
      }}
    >
      <div className="flex flex-col p-5 py-10">
        <Component {...pageProps} />
      </div>
    </ClerkProvider>
  );
}

export default MyApp;
