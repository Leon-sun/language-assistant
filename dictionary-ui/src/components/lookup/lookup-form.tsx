"use client";

import { useState } from "react";
import { Search } from "lucide-react";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

export function LookupForm() {
  const { lang } = useLanguage();
  const [word, setWord] = useState("");

  return (
    <Card className="overflow-hidden transition-all duration-200 hover:scale-[1.005] hover:shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">{t(lang, "translateWord")}</CardTitle>
      </CardHeader>
      <CardContent>
        <form
          method="post"
          action="/lookup"
          className="space-y-4"
          onSubmit={(e) => e.preventDefault()}
        >
          <div className="space-y-2">
            <Label htmlFor="word">{t(lang, "wordLabel")}</Label>
            <Input
              id="word"
              name="word"
              type="text"
              placeholder="e.g. bonjour, hello"
              value={word}
              onChange={(e) => setWord(e.target.value)}
              className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
            />
          </div>
          <Button type="submit" size="default" className="w-full sm:w-auto">
            <Search className="mr-2 h-4 w-4" />
            {t(lang, "lookupButton")}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
