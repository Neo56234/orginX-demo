"use client";

import { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { motion } from "framer-motion";
import { useInvestigationStore } from "@/lib/store";
import { t } from "@/lib/i18n";

// Demo coordinates for countries/cities to simulate geocoding
const MOCK_COORDS: Record<string, [number, number]> = {
  "Bangladesh": [90.4125, 23.8103],
  "Dhaka": [90.4125, 23.8103],
  "Pakistan": [73.0479, 33.6844],
  "India": [77.2090, 28.6139],
  "Default Claimed": [90.4125, 23.8103],
};

export default function MapView() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const geolocator = useInvestigationStore(state => state.agents.geolocator);
  const verdict = useInvestigationStore(state => state.verdict);
  const lang = useInvestigationStore(state => state.language);
  
  const actualCountry = verdict?.actual_origin_country;
  
  let fallbackCountry = null;
  if (geolocator.status === 'complete' && geolocator.findings.length > 0) {
    const finding = geolocator.findings.find(f => f.value && MOCK_COORDS[f.value]);
    if (finding) fallbackCountry = finding.value;
    else fallbackCountry = "Pakistan"; // Mock for demo if none found but complete
  }

  const originPlace = actualCountry || fallbackCountry;
  
  const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || 'pk.eyJ1IjoidmFsaWR0b2tlbnVzZXIiLCJhIjoiY2xwMG1wYWk2MG95aTJycWt6ZjMxdnEyaCJ9.invalidtoken';
  
  useEffect(() => {
    if (!mapContainer.current || !originPlace) return;

    if (!map.current) {
      mapboxgl.accessToken = token;
      try {
        map.current = new mapboxgl.Map({
          container: mapContainer.current,
          style: "mapbox://styles/mapbox/dark-v11",
          center: MOCK_COORDS["Default Claimed"] || [90.4, 23.8],
          zoom: 2,
          interactive: false
        });
        
        map.current.on('load', () => {
          const actualCoords = MOCK_COORDS[originPlace] || [90.4, 23.8];
          
          map.current?.flyTo({
            center: actualCoords,
            zoom: 5,
            speed: 1.2,
            curve: 1.5,
            easing(t) {
              return t;
            }
          });

          // Add Actual Marker (Green)
          const elGreen = document.createElement('div');
          elGreen.className = 'w-6 h-6 bg-[#00D67E] rounded-full border-4 border-[#13192A] shadow-[0_0_20px_rgba(0,214,126,0.8)] flex items-center justify-center relative';
          
          const ring = document.createElement('div');
          ring.className = 'absolute -inset-4 border-2 border-[#00D67E] rounded-full animate-ping opacity-75';
          elGreen.appendChild(ring);
          
          new mapboxgl.Marker(elGreen)
            .setLngLat(actualCoords)
            .addTo(map.current!);
            
          // Add Claimed Marker (Red) if they differ
          const claimedCoords = MOCK_COORDS["Default Claimed"];
          if (claimedCoords && (claimedCoords[0] !== actualCoords[0] || claimedCoords[1] !== actualCoords[1])) {
             const elRed = document.createElement('div');
             elRed.className = 'w-4 h-4 bg-[#FF3B5C] rounded-full border-2 border-[#13192A] shadow-[0_0_10px_rgba(255,59,92,0.8)]';
             new mapboxgl.Marker(elRed)
               .setLngLat(claimedCoords)
               .addTo(map.current!);
               
             map.current?.addSource('route', {
               type: 'geojson',
               data: {
                 type: 'Feature',
                 properties: {},
                 geometry: {
                   type: 'LineString',
                   coordinates: [claimedCoords, actualCoords]
                 }
               }
             });
             
             map.current?.addLayer({
               id: 'route',
               type: 'line',
               source: 'route',
               layout: {
                 'line-join': 'round',
                 'line-cap': 'round'
               },
               paint: {
                 'line-color': '#FF3B5C',
                 'line-width': 2,
                 'line-dasharray': [2, 4]
               }
             });
          }
        });
      } catch (err) {
        console.error("Mapbox init failed", err);
      }
    }
    
    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, [originPlace, token]);

  if (geolocator.status !== 'complete' || !originPlace) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="w-full max-w-5xl mx-auto mt-8 bg-card/30 p-1 rounded-2xl border border-gray-800 overflow-hidden relative"
    >
      <div className="absolute top-4 left-4 z-10 bg-[#0A0E1A]/80 backdrop-blur-md px-4 py-2 rounded-lg border border-gray-700 shadow-lg">
        <h3 className="text-gray-300 text-sm font-sans flex items-center gap-2">
          🌍 {lang === 'bn' ? 'ভৌগোলিক উৎস' : 'Geographic Origin'}: 
          <span className="text-truth font-bold text-lg">{originPlace}</span>
        </h3>
      </div>
      <div ref={mapContainer} className="w-full h-80 rounded-xl overflow-hidden bg-gray-900" />
    </motion.div>
  );
}
