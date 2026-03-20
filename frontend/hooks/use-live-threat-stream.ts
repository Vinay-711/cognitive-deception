"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchLatestEvents, type AttackEventRecord } from "@/services/api-client";

export function useLiveThreatStream() {
  const [events, setEvents] = useState<AttackEventRecord[]>([]);

  useEffect(() => {
    let mounted = true;

    const load = async () => {
      try {
        const result = await fetchLatestEvents();
        if (mounted) {
          setEvents(result);
        }
      } catch {
        // Fallback
      }
    };

    load();
    const timer = setInterval(load, 3000);

    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  const liveCount = useMemo(
    () => events.filter((event) => event.attack_label !== "reconnaissance").length,
    [events]
  );

  return { events, liveCount };
}
