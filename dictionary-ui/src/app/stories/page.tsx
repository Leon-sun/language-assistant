"use client";

import Link from "next/link";
import { Newspaper } from "lucide-react";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const feeds = [
  { labelKey: "actualites" as const, url: "https://www.lemonde.fr/rss/une.xml" },
  { labelKey: "economie" as const, url: "https://www.lemonde.fr/economie/rss_full.xml" },
  { labelKey: "culture" as const, url: "https://www.lemonde.fr/culture/rss_full.xml" },
  { labelKey: "idees" as const, url: "https://www.lemonde.fr/idees/rss_full.xml" },
];

export default function StoriesPage() {
  const { lang } = useLanguage();
  return (
    <>
      <div className="mb-6">
        <h1 className="flex items-center gap-2 text-3xl font-semibold tracking-tight text-zinc-100 md:text-4xl">
          <Newspaper className="h-8 w-8 text-zinc-400" />
          {t(lang, "storiesTitle")}
        </h1>
        <div className="mt-1 h-0.5 w-12 rounded-full bg-gradient-to-r from-zinc-500 to-zinc-700" />
      </div>
      <p className="text-base text-zinc-400 leading-relaxed">
        {t(lang, "storiesSubtitle")}
      </p>

      <div className="mt-6">
        <Button size="default" className="transition-all duration-200 hover:scale-[1.01]">
          {t(lang, "saveAllArticles")}
        </Button>
      </div>

      <div className="mt-8 space-y-6">
        {feeds.map((feed) => (
          <Card key={feed.labelKey} className="transition-all duration-200 hover:scale-[1.005] hover:shadow-lg">
            <CardHeader className="pb-2">
              <CardTitle className="text-base">{t(lang, feed.labelKey)}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-zinc-500">{t(lang, "noArticles")}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="mt-8 p-6">
        <p className="text-sm text-zinc-400">
          <strong className="text-zinc-300">{t(lang, "rssFeeds")}</strong>
          <br />
          <Link href="https://www.lemonde.fr/rss/une.xml" target="_blank" rel="noopener noreferrer" className="text-zinc-300 underline hover:text-zinc-100">
            Actualités
          </Link>
          <br />
          <Link href="https://www.lemonde.fr/economie/rss_full.xml" target="_blank" rel="noopener noreferrer" className="text-zinc-300 underline hover:text-zinc-100">
            Économie
          </Link>
          <br />
          <Link href="https://www.lemonde.fr/culture/rss_full.xml" target="_blank" rel="noopener noreferrer" className="text-zinc-300 underline hover:text-zinc-100">
            Culture
          </Link>
          <br />
          <Link href="https://www.lemonde.fr/idees/rss_full.xml" target="_blank" rel="noopener noreferrer" className="text-zinc-300 underline hover:text-zinc-100">
            Idées
          </Link>
        </p>
      </Card>
    </>
  );
}
