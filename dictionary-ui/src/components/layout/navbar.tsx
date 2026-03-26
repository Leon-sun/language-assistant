"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", labelKey: "home" as const },
  { href: "/lookup", labelKey: "lookupWord" as const },
  { href: "/stories", labelKey: "stories" as const },
  { href: "/about", labelKey: "about" as const },
];

export function Navbar() {
  const pathname = usePathname();
  const { lang, setLang } = useLanguage();

  return (
    <header className="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-900/70 backdrop-blur-xl">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="flex items-center gap-2 text-zinc-100 font-semibold text-base tracking-tight"
        >
          <span className="flex h-7 w-7 items-center justify-center rounded-md bg-zinc-700 text-xs font-bold text-zinc-200">
            D
          </span>
          <span className="hidden sm:inline">{t(lang, "siteName")}</span>
        </Link>

        <nav className="hidden md:flex items-center gap-1">
          {navItems.map(({ href, labelKey }) => {
            const isActive =
              href === "/"
                ? pathname === "/"
                : pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200",
                  isActive
                    ? "text-zinc-100 bg-zinc-800/80"
                    : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/50"
                )}
              >
                {t(lang, labelKey)}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-0.5 rounded-lg border border-zinc-700 bg-zinc-800/50 p-0.5">
            <button
              type="button"
              onClick={() => setLang("en")}
              className={cn(
                "rounded-md px-2.5 py-1 text-xs font-medium transition-all duration-200",
                lang === "en"
                  ? "bg-zinc-700 text-zinc-100"
                  : "text-zinc-400 hover:text-zinc-200"
              )}
            >
              EN
            </button>
            <button
              type="button"
              onClick={() => setLang("fr")}
              className={cn(
                "rounded-md px-2.5 py-1 text-xs font-medium transition-all duration-200",
                lang === "fr"
                  ? "bg-zinc-700 text-zinc-100"
                  : "text-zinc-400 hover:text-zinc-200"
              )}
            >
              FR
            </button>
          </div>
          <Link
            href="/sign-in"
            className="hidden sm:inline-flex h-9 items-center justify-center rounded-lg border border-zinc-700 bg-zinc-800 px-3 text-sm font-medium text-zinc-200 hover:bg-zinc-700 hover:border-zinc-600 transition-all duration-200"
          >
            {t(lang, "signIn")}
          </Link>
          <Link
            href="/sign-up"
            className="hidden sm:inline-flex h-9 items-center justify-center rounded-lg bg-white px-3 text-sm font-medium text-zinc-900 shadow-sm hover:bg-zinc-100 hover:scale-[1.02] transition-all duration-200"
          >
            {t(lang, "signUp")}
          </Link>
        </div>
      </div>
    </header>
  );
}
