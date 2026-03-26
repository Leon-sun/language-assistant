"use client";

import { useEffect } from "react";

const DJANGO_APP_URL =
  process.env.NEXT_PUBLIC_DJANGO_APP_URL || "http://localhost:8000";

export default function HomePage() {
  useEffect(() => {
    window.location.href = DJANGO_APP_URL;
  }, []);

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 text-zinc-400">
      <p className="text-sm">Redirecting to the original frontend…</p>
      <a
        href={DJANGO_APP_URL}
        className="text-sm text-zinc-300 underline hover:text-zinc-100"
      >
        Click here if you are not redirected
      </a>
    </div>
  );
}
