"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { cn } from "@/lib/utils";

import type { CopyKey } from "@/lib/i18n";

export type CardSectionItem = {
  href: string;
  titleKey: CopyKey;
  descKey: CopyKey;
};

const sidebarItems: CardSectionItem[] = [
  { href: "/", titleKey: "home", descKey: "homeDesc" },
  { href: "/lookup", titleKey: "lookupWord", descKey: "lookupDesc" },
  { href: "/stories", titleKey: "stories", descKey: "storiesDesc" },
  { href: "/about", titleKey: "about", descKey: "aboutDesc" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { lang } = useLanguage();

  return (
    <aside className="space-y-2">
      <h2 className="px-2 text-xs font-semibold uppercase tracking-wider text-zinc-500">
        {t(lang, "sections")}
      </h2>
      <nav className="flex flex-col gap-2">
        {sidebarItems.map((item) => {
          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "group block rounded-xl border p-4 text-left transition-all duration-200 hover:scale-[1.01] hover:border-zinc-600 hover:shadow-md",
                isActive
                  ? "border-l-4 border-l-white/90 border-zinc-600 bg-zinc-800/80"
                  : "border-zinc-700 bg-zinc-800/40 hover:bg-zinc-800/60"
              )}
            >
              <h3 className="text-sm font-semibold text-zinc-100">
                {t(lang, item.titleKey)}
              </h3>
              <p className="mt-1 text-xs text-zinc-400">
                {t(lang, item.descKey)}
              </p>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
