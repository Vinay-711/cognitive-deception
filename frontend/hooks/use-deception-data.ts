"use client";

import { useEffect, useState } from "react";

import { fetchDeceptionSessions, type DeceptionSessionOverview } from "@/services/api-client";
import { mockDeceptionSessions } from "@/services/mock-data";

export function useDeceptionData() {
  const [sessions, setSessions] = useState<DeceptionSessionOverview[]>(mockDeceptionSessions);

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      try {
        const data = await fetchDeceptionSessions();
        if (mounted) {
          setSessions(data);
        }
      } catch {
        // fallback to mock data
      }
    };
    load();
    const timer = setInterval(load, 8000);
    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  return { sessions };
}
