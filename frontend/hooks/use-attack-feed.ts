"use client";

import { useEffect, useState } from "react";

import { fetchAttacks, type AttackFeedRecord } from "@/services/api-client";
import { mockAttackFeed } from "@/services/mock-data";

export function useAttackFeed() {
  const [events, setEvents] = useState<AttackFeedRecord[]>(mockAttackFeed);

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      try {
        const data = await fetchAttacks();
        if (mounted) {
          setEvents(data);
        }
      } catch {
        // fallback
      }
    };
    load();
    const timer = setInterval(load, 6000);
    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  return { events };
}
