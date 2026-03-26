"use client";

import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import type { CopyKey } from "@/lib/i18n";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type CardSectionProps = {
  titleKey?: CopyKey;
  children: React.ReactNode;
  className?: string;
};

export function CardSection({ titleKey, children, className }: CardSectionProps) {
  const { lang } = useLanguage();
  return (
    <Card className={cn("transition-all duration-200 hover:scale-[1.005] hover:shadow-lg", className)}>
      {titleKey && (
        <CardHeader className="pb-2">
          <CardTitle className="text-lg">{t(lang, titleKey)}</CardTitle>
        </CardHeader>
      )}
      <CardContent className={titleKey ? undefined : "p-6"}>
        {children}
      </CardContent>
    </Card>
  );
}
