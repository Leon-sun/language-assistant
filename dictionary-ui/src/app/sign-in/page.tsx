"use client";

import Link from "next/link";
import { useLanguage } from "@/contexts/language-context";
import { t } from "@/lib/i18n";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function SignInPage() {
  const { lang } = useLanguage();
  return (
    <>
      <div className="mb-6">
        <h1 className="text-3xl font-semibold tracking-tight text-zinc-100 md:text-4xl">
          {t(lang, "signIn")}
        </h1>
        <div className="mt-1 h-0.5 w-12 rounded-full bg-gradient-to-r from-zinc-500 to-zinc-700" />
      </div>
      <p className="text-base text-zinc-400 leading-relaxed">
        {t(lang, "signInSubtitle")}
      </p>

      <Card className="mt-8 max-w-md transition-all duration-200 hover:scale-[1.005] hover:shadow-lg">
        <CardHeader>
          <CardTitle className="sr-only">{t(lang, "signIn")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <form className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="login">{t(lang, "nickname")}</Label>
              <Input
                id="login"
                name="login"
                type="text"
                autoComplete="username"
                className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">{t(lang, "password")}</Label>
              <Input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                className="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500"
              />
              <p className="text-xs text-zinc-500">{t(lang, "passwordHint")}</p>
            </div>
            <div className="flex items-center gap-2">
              <input
                id="remember"
                name="remember"
                type="checkbox"
                className="h-4 w-4 rounded border-zinc-600 bg-zinc-900 text-white focus:ring-zinc-500"
              />
              <Label htmlFor="remember" className="font-normal text-zinc-400">
                {t(lang, "rememberMe")}
              </Label>
            </div>
            <Button type="submit" size="lg" className="w-full">
              {t(lang, "signIn")}
            </Button>
          </form>
          <div className="space-y-1 border-t border-zinc-700 pt-4 text-sm text-zinc-400">
            <p>
              {t(lang, "dontHaveAccount")}{" "}
              <Link href="/sign-up" className="text-zinc-200 underline hover:text-zinc-100">
                {t(lang, "signUpLink")}
              </Link>
            </p>
            <p>
              <Link href="#" className="text-zinc-200 underline hover:text-zinc-100">
                {t(lang, "forgotPassword")}
              </Link>
            </p>
          </div>
        </CardContent>
      </Card>
    </>
  );
}
