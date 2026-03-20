"use client";

import { useEffect, useState } from "react";

import { useLiveThreatStream } from "./use-live-threat-stream";

export function useTerminalReplay() {
  const { events } = useLiveThreatStream();
  const [index, setIndex] = useState(0);

  const commands = events.map(e => e.command).reverse();

  useEffect(() => {
    if (commands.length === 0) return;
    const timer = setInterval(() => {
      setIndex((current) => (current + 1) % commands.length);
    }, 2800);

    return () => clearInterval(timer);
  }, [commands.length]);

  return {
    commands: commands.slice(0, index + 1),
    cursor: index
  };
}
