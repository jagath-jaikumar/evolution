import Home from "./index";
import "../styles/globals.css";
import { AppProps } from "next/app";
export default function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps}><Home /></Component>
}
