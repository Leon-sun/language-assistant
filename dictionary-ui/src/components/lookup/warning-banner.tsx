"use client";

import { AlertTriangle } from "lucide-react";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { cn } from "@/lib/utils";

export function WarningBanner({ className }: { className?: string }) {
  const { lang } = useLanguage();
  return (
    <div
      role="alert"
      className={cn(
        "flex gap-3 rounded-xl border border-amber-500/30 bg-zinc-800 p-6",
        className
      )}
    >
      <AlertTriangle className="h-5 w-5 shrink-0 text-amber-500" />
      <p className="text-sm text-zinc-300">
        {t(lang, "warningBanner")}
      </p>
    </div>
  );
}
