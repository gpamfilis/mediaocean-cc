import { Inter } from "next/font/google";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { ThemeProvider as MaterialThemeProvider } from "@mui/material/styles";
import theme from "../../theme";
import { CssBaseline } from "@mui/material";
import { Toaster } from "react-hot-toast";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Ad Insights",
  description:
    "Ad Insights Explorer Lite allows you to detect frodulent posts.",
};

export default async function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <MaterialThemeProvider theme={theme}>
          <CssBaseline />
          <Toaster position="top-center" /> {children}
        </MaterialThemeProvider>
      </body>
    </html>
  );
}
