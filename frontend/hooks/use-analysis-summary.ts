"use client";

import { useEffect, useState } from "react";

import { fetchAnalysis, type AnalysisSummary } from "@/services/api-client";

export function useAnalysisSummary() {
  const [summary, setSummary] = useState<AnalysisSummary | null>(null);

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      try {
        const data = await fetchAnalysis();
        if (mounted) {
          setSummary(data);
        }
      } catch {
        // ignore
      }
    };
    load();
    const timer = setInterval(load, 8000);
    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  return { summary };
}
