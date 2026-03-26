"use client";

import { Search } from "lucide-react";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { WarningBanner } from "@/components/lookup/warning-banner";
import { LookupForm } from "@/components/lookup/lookup-form";

export default function LookupPage() {
  const { lang } = useLanguage();
  return (
    <>
      <div className="mb-6">
        <h1 className="flex items-center gap-2 text-3xl font-semibold tracking-tight text-zinc-100 md:text-4xl">
          <Search className="h-8 w-8 text-zinc-400" />
          {t(lang, "wordLookup")}
        </h1>
        <div className="mt-1 h-0.5 w-12 rounded-full bg-gradient-to-r from-zinc-500 to-zinc-700" />
      </div>
      <p className="text-base text-zinc-400 leading-relaxed">
        {t(lang, "lookupSubtitle")}
      </p>

      <div className="mt-6">
        <WarningBanner />
      </div>

      <div className="mt-8">
        <LookupForm />
      </div>
    </>
  );
}
