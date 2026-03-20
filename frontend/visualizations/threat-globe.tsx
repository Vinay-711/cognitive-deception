"use client";

import { useMemo, useRef } from "react";

import { OrbitControls, Points, PointMaterial, Sphere, Stars } from "@react-three/drei";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

export type GeoPoint = [number, number];
export type AttackArc = {
  source: GeoPoint;
  target: GeoPoint;
  weight: number;
};
const attackArcs: AttackArc[] = [
  { source: [-74.006, 40.7128], target: [77.209, 28.6139], weight: 62 },
  { source: [13.405, 52.52], target: [-0.1278, 51.5074], weight: 74 },
  { source: [103.8198, 1.3521], target: [139.6917, 35.6895], weight: 54 },
  { source: [37.6173, 55.7558], target: [151.2093, -33.8688], weight: 39 }
];

function RotatingGlobe() {
  const globeRef = useRef<THREE.Mesh>(null);

  useFrame((_, delta) => {
    if (!globeRef.current) {
      return;
    }
    globeRef.current.rotation.y += delta * 0.12;
  });

  const points = useMemo(() => {
    const flatPoints = attackArcs.flatMap((arc) => {
      const [lng, lat] = arc.target;
      const phi = (90 - lat) * (Math.PI / 180);
      const theta = (lng + 180) * (Math.PI / 180);
      const radius = 1.03;
      return [
        -(radius * Math.sin(phi) * Math.cos(theta)),
        radius * Math.cos(phi),
        radius * Math.sin(phi) * Math.sin(theta)
      ];
    });
    return new Float32Array(flatPoints);
  }, []);

  return (
    <group>
      <Sphere ref={globeRef} args={[1, 64, 64]}>
        <meshStandardMaterial
          color="#0d1320"
          emissive="#00e5ff"
          emissiveIntensity={0.14}
          roughness={0.4}
          metalness={0.5}
          wireframe
        />
      </Sphere>
      <Points positions={points} stride={3} frustumCulled>
        <PointMaterial color="#00E5FF" size={0.03} sizeAttenuation depthWrite={false} />
      </Points>
    </group>
  );
}

export function ThreatGlobe() {
  return (
    <div className="h-[340px] w-full overflow-hidden rounded-2xl border border-cyan-400/20 bg-gradient-to-b from-cyan-950/10 to-transparent">
      <Canvas camera={{ position: [0, 0, 2.8], fov: 45 }}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[4, 4, 2]} intensity={1} color="#00E5FF" />
        <Stars radius={70} depth={60} count={1800} factor={2} saturation={0.1} fade speed={1} />
        <RotatingGlobe />
        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.45} />
      </Canvas>
    </div>
  );
}
