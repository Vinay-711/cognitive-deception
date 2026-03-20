import { cva } from "class-variance-authority";
import { type ButtonHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-300/60 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-cyan-400/20 text-cyan-100 hover:bg-cyan-400/30",
        ghost: "bg-transparent text-slate-300 hover:bg-white/5",
        danger: "bg-red-500/20 text-red-100 hover:bg-red-500/30"
      }
    },
    defaultVariants: {
      variant: "default"
    }
  }
);

export function Button({
  className,
  variant = "default",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "default" | "ghost" | "danger" }) {
  return <button className={cn(buttonVariants({ variant }), className)} {...props} />;
}
