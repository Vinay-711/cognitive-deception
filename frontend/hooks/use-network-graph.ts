"use client";

import { useEffect, useState } from "react";

import { fetchNetworkGraph, type NetworkGraph } from "@/services/api-client";
import { mockNetworkGraph } from "@/services/mock-data";

export function useNetworkGraph() {
  const [graph, setGraph] = useState<NetworkGraph>(mockNetworkGraph);

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      try {
        const data = await fetchNetworkGraph();
        if (mounted) {
          setGraph(data);
        }
      } catch {
        // fallback
      }
    };
    load();
    const timer = setInterval(load, 12000);
    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  return { graph };
}
