"use client";

import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";

export function Footer() {
  const { lang } = useLanguage();
  return (
    <footer className="border-t border-zinc-800 py-6">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <p className="text-sm text-zinc-500">
          {t(lang, "copyright")} {t(lang, "builtWith")}.
        </p>
      </div>
    </footer>
  );
}
