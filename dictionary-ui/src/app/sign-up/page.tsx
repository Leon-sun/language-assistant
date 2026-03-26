"use client";

import Link from "next/link";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function SignUpPage() {
  const { lang } = useLanguage();
  return (
    <>
      <div className="mb-6">
        <h1 className="text-3xl font-semibold tracking-tight text-zinc-100 md:text-4xl">
          {t(lang, "signUp")}
        </h1>
        <div className="mt-1 h-0.5 w-12 rounded-full bg-gradient-to-r from-zinc-500 to-zinc-700" />
      </div>
      <p className="text-base text-zinc-400 leading-relaxed">
        {t(lang, "signUpSubtitle")}
      </p>

      <Card className="mt-8 max-w-md transition-all duration-200 hover:scale-[1.005] hover:shadow-lg">
        <CardHeader>
          <CardTitle className="sr-only">{t(lang, "signUp")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <form className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">{t(lang, "email")} *</Label>
              <Input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="nickname">{t(lang, "nickname")} *</Label>
              <Input
                id="nickname"
                name="nickname"
                type="text"
                autoComplete="username"
                className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="native_language">{t(lang, "nativeLanguage")} *</Label>
              <Input
                id="native_language"
                name="native_language"
                type="text"
                className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="target_language">{t(lang, "learningLanguage")} *</Label>
              <Input
                id="target_language"
                name="target_language"
                type="text"
                className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password1">{t(lang, "password")} *</Label>
              <Input
                id="password1"
                name="password1"
                type="password"
                autoComplete="new-password"
                className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
              />
              <p className="text-xs text-zinc-500">{t(lang, "passwordHint")}</p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="password2">{t(lang, "passwordAgain")} *</Label>
              <Input
                id="password2"
                name="password2"
                type="password"
                autoComplete="new-password"
                className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
              />
            </div>
            <Button type="submit" size="lg" className="w-full">
              {t(lang, "signUp")}
            </Button>
          </form>
          <div className="border-t border-zinc-700 pt-4 text-sm text-zinc-400">
            <p>
              {t(lang, "alreadyHaveAccount")}{" "}
              <Link href="/sign-in" className="text-zinc-200 underline hover:text-zinc-100">
                {t(lang, "signInLink")}
              </Link>
            </p>
          </div>
        </CardContent>
      </Card>
    </>
  );
}
