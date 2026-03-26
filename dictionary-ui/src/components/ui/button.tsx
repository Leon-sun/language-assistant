import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "ghost" | "outline";
  size?: "default" | "sm" | "lg";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    return (
      <button
        className={cn(
          "inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-500 focus-visible:ring-offset-0 disabled:pointer-events-none disabled:opacity-50",
          variant === "default" &&
            "bg-white text-zinc-900 shadow-sm hover:bg-zinc-100 hover:scale-[1.01] hover:shadow",
          variant === "secondary" &&
            "bg-zinc-800 text-zinc-100 border border-zinc-700 hover:bg-zinc-700 hover:border-zinc-600",
          variant === "ghost" &&
            "text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100",
          variant === "outline" &&
            "border border-zinc-700 bg-transparent text-zinc-100 hover:bg-zinc-800",
          size === "default" && "h-10 px-4 py-2",
          size === "sm" && "h-8 px-3 text-xs",
          size === "lg" && "h-11 px-6 text-base",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button };
