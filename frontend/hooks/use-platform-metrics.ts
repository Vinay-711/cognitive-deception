"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchPlatformMetrics, type PlatformMetrics } from "@/services/api-client";

export function usePlatformMetrics() {
  const [metrics, setMetrics] = useState<PlatformMetrics | null>(null);

  useEffect(() => {
    let mounted = true;

    const load = async () => {
      try {
        const result = await fetchPlatformMetrics();
        if (mounted) {
          setMetrics(result);
        }
      } catch {
        // Fallback is handled by component-level defaults.
      }
    };

    load();
    const timer = setInterval(load, 5000);

    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  const topAttackerType = useMemo(() => {
    if (!metrics) {
      return "N/A";
    }

    let topLabel = "N/A";
    let topCount = -1;
    Object.entries(metrics.attacker_type_counts).forEach(([label, count]) => {
      if (count > topCount) {
        topLabel = label;
        topCount = count;
      }
    });

    return topLabel;
  }, [metrics]);

  return { metrics, topAttackerType };
}
