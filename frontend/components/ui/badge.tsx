import { cva } from "class-variance-authority";
import { type HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wide",
  {
    variants: {
      variant: {
        default: "border-cyan-400/30 bg-cyan-400/10 text-cyan-200",
        alert: "border-red-400/30 bg-red-400/10 text-red-200",
        purple: "border-violet-400/30 bg-violet-400/10 text-violet-200"
      }
    },
    defaultVariants: {
      variant: "default"
    }
  }
);

export function Badge({
  className,
  variant = "default",
  ...props
}: HTMLAttributes<HTMLDivElement> & { variant?: "default" | "alert" | "purple" }) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}
