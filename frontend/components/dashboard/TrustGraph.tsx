"use client";

import { useEffect, useRef } from "react";
import * as d3 from "d3";

interface Node {
  id: string;
  label: string;
  platform: string;
  credibility_score: number;
  total_shared: number;
  flagged_count: number;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
}

interface Edge {
  source: string | Node;
  target: string | Node;
  weight: number;
}

interface Props {
  nodes: Node[];
  edges: Edge[];
}

export default function TrustGraph({ nodes, edges }: Props) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || nodes.length === 0) return;

    const width = svgRef.current.clientWidth || 800;
    const height = 480;

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    // Background
    svg
      .append("rect")
      .attr("width", width)
      .attr("height", height)
      .attr("fill", "#0A0E1A")
      .attr("rx", 12);

    const simulation = d3
      .forceSimulation<Node>(nodes)
      .force(
        "link",
        d3
          .forceLink<Node, Edge>(edges)
          .id((d) => d.id)
          .distance(120)
          .strength(0.3)
      )
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(40));

    // Edges
    const link = svg
      .append("g")
      .selectAll("line")
      .data(edges)
      .enter()
      .append("line")
      .attr("stroke", "#FF3B5C")
      .attr("stroke-opacity", 0.3)
      .attr("stroke-width", (d) => Math.max(1, (d.weight as number) * 0.5))
      .attr("stroke-dasharray", "4 2");

    // Node groups
    const node = svg
      .append("g")
      .selectAll("g")
      .data(nodes)
      .enter()
      .append("g")
      .call(
        d3
          .drag<SVGGElement, Node>()
          .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    // Node circles
    node
      .append("circle")
      .attr("r", (d) => 8 + Math.sqrt(d.total_shared) * 0.8)
      .attr("fill", (d) => {
        const score = d.credibility_score;
        if (score > 0.8) return "#00D67E";
        if (score > 0.5) return "#FFB833";
        if (score > 0.2) return "#FF7B3C";
        return "#FF3B5C";
      })
      .attr("fill-opacity", 0.85)
      .attr("stroke", "#0A0E1A")
      .attr("stroke-width", 2);

    // Glow for bad actors
    node
      .filter((d) => d.credibility_score < 0.2)
      .append("circle")
      .attr("r", (d) => 16 + Math.sqrt(d.total_shared) * 0.8)
      .attr("fill", "none")
      .attr("stroke", "#FF3B5C")
      .attr("stroke-width", 1)
      .attr("stroke-opacity", 0.4)
      .attr("class", "animate-ping");

    // Platform icon
    node
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "0.35em")
      .attr("font-size", "10px")
      .attr("fill", "#0A0E1A")
      .attr("font-weight", "bold")
      .text((d) => (d.platform === "youtube" ? "YT" : "FB"));

    // Label
    node
      .append("text")
      .attr("dy", (d) => -(12 + Math.sqrt(d.total_shared) * 0.8) - 4)
      .attr("text-anchor", "middle")
      .attr("font-size", "10px")
      .attr("fill", "#8B95A9")
      .text((d) =>
        d.label.length > 16 ? d.label.substring(0, 16) + "…" : d.label
      );

    // Tooltip
    const tooltip = d3
      .select("body")
      .append("div")
      .style("position", "fixed")
      .style("background", "#13192A")
      .style("border", "1px solid #2A3354")
      .style("border-radius", "8px")
      .style("padding", "8px 12px")
      .style("font-size", "12px")
      .style("color", "#E8ECF7")
      .style("pointer-events", "none")
      .style("opacity", 0)
      .style("z-index", "9999")
      .style("font-family", "monospace");

    node
      .on("mouseover", (event, d) => {
        tooltip
          .style("opacity", 1)
          .html(
            `<div style="font-weight:bold;margin-bottom:4px">${d.label}</div>
             <div>Platform: ${d.platform}</div>
             <div>Credibility: <span style="color:${d.credibility_score > 0.5 ? "#00D67E" : "#FF3B5C"}">${(d.credibility_score * 100).toFixed(0)}%</span></div>
             <div>Total shared: ${d.total_shared}</div>
             <div>Flagged: ${d.flagged_count}</div>`
          )
          .style("left", event.clientX + 12 + "px")
          .style("top", event.clientY - 10 + "px");
      })
      .on("mousemove", (event) => {
        tooltip
          .style("left", event.clientX + 12 + "px")
          .style("top", event.clientY - 10 + "px");
      })
      .on("mouseout", () => tooltip.style("opacity", 0));

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => (d.source as Node).x!)
        .attr("y1", (d) => (d.source as Node).y!)
        .attr("x2", (d) => (d.target as Node).x!)
        .attr("y2", (d) => (d.target as Node).y!);

      node.attr("transform", (d) => `translate(${d.x},${d.y})`);
    });

    return () => {
      simulation.stop();
      tooltip.remove();
    };
  }, [nodes, edges]);

  return (
    <div className="w-full bg-[#0A0E1A] rounded-xl border border-[#2A3354] overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#2A3354]">
        <div className="flex items-center gap-2">
          <span className="text-white font-mono text-sm font-bold">
            SOURCE TRUST GRAPH
          </span>
          <span className="text-gray-500 font-mono text-xs">
            — সন্দেহজনক নেটওয়ার্ক
          </span>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-[#FF3B5C] inline-block" />
            <span className="text-gray-400">Low trust</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-[#FFB833] inline-block" />
            <span className="text-gray-400">Medium</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-[#00D67E] inline-block" />
            <span className="text-gray-400">Trusted</span>
          </span>
        </div>
      </div>
      <svg ref={svgRef} className="w-full" style={{ height: "480px" }} />
    </div>
  );
}
