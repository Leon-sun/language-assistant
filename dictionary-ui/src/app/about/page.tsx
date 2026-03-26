"use client";

import Link from "next/link";
import { Info } from "lucide-react";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const featureKeys = [
  "modernUI",
  "cleanStructure",
  "readyForDev",
  "sqliteConfigured",
  "adminPanel",
] as const;

const techItems = [
  { nameKey: "django" as const, descKey: "webFramework" as const },
  { nameKey: "python" as const, descKey: "programmingLanguage" as const },
  { nameKey: "gemini" as const, descKey: "aiService" as const },
  { nameKey: "sqlite" as const, descKey: "database" as const },
  { nameKey: "htmlCss" as const, descKey: "frontend" as const },
];

export default function AboutPage() {
  const { lang } = useLanguage();
  return (
    <>
      <div className="mb-6">
        <h1 className="flex items-center gap-2 text-3xl font-semibold tracking-tight text-zinc-100 md:text-4xl">
          <Info className="h-8 w-8 text-zinc-400" />
          {t(lang, "aboutTitle")}
        </h1>
        <div className="mt-1 h-0.5 w-12 rounded-full bg-gradient-to-r from-zinc-500 to-zinc-700" />
      </div>
      <p className="text-base text-zinc-400 leading-relaxed">
        {t(lang, "aboutSubtitle")}
      </p>

      <Card className="mt-8 transition-all duration-200 hover:scale-[1.005] hover:shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg">{t(lang, "featureList")}</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-inside list-disc space-y-1 text-sm text-zinc-400">
            {featureKeys.map((key) => (
              <li key={key}>{t(lang, key)}</li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <Card className="mt-6 transition-all duration-200 hover:scale-[1.005] hover:shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg">{t(lang, "techStack")}</CardTitle>
          <p className="text-sm text-zinc-400">{t(lang, "techUses")}</p>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-sm">
            {techItems.map(({ nameKey, descKey }) => (
              <li key={nameKey} className="text-zinc-400">
                <strong className="text-zinc-200">{t(lang, nameKey)}</strong>
                {" — "}
                {t(lang, descKey)}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <div className="mt-8">
        <Link
          href="/"
          className="inline-flex h-10 items-center justify-center rounded-lg bg-white px-4 text-sm font-medium text-zinc-900 shadow-sm transition-all duration-200 hover:scale-[1.01] hover:bg-zinc-100 hover:shadow"
        >
          {t(lang, "backToHome")}
        </Link>
      </div>
    </>
  );
}
