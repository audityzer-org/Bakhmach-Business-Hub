'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

interface Node {
  id: string;
  name: string;
  type: 'presentation' | 'middleware' | 'service' | 'data' | 'analytics' | 'research';
  layer: string;
  health: number;
  readiness: number;
}

interface Edge {
  source: string;
  target: string;
  latency: number;
  type: string;
}

const ARCHITECTURE_DATA = {
  nodes: [
    { id: 'frontend', name: 'Frontend (Next.js)', type: 'presentation', layer: 'presentation', health: 85, readiness: 20 },
    { id: 'gateway', name: 'API Gateway', type: 'middleware', layer: 'application', health: 88, readiness: 30 },
    { id: 'business', name: 'Business Logic', type: 'service', layer: 'business', health: 80, readiness: 25 },
    { id: 'auth', name: 'Auth Service', type: 'service', layer: 'security', health: 92, readiness: 40 },
    { id: 'integration', name: 'Integration', type: 'service', layer: 'integration', health: 75, readiness: 20 },
    { id: 'data', name: 'Data Layer', type: 'data', layer: 'persistence', health: 95, readiness: 35 },
    { id: 'ml', name: 'ML Pipeline', type: 'analytics', layer: 'analytics', health: 70, readiness: 15 },
    { id: 'consciousness', name: 'Consciousness AGI', type: 'research', layer: 'research', health: 65, readiness: 10 },
  ],
  edges: [
    { source: 'frontend', target: 'gateway', latency: 100, type: 'HTTPS/REST' },
    { source: 'gateway', target: 'business', latency: 20, type: 'gRPC' },
    { source: 'gateway', target: 'auth', latency: 10, type: 'JWT' },
    { source: 'business', target: 'data', latency: 50, type: 'PostgreSQL' },
    { source: 'business', target: 'integration', latency: 200, type: 'REST/Webhook' },
    { source: 'business', target: 'ml', latency: 500, type: 'Kafka/gRPC' },
    { source: 'consciousness', target: 'ml', latency: 1000, type: 'Python IPC' },
  ],
};

const ArchitectureVisualizer: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [filter, setFilter] = useState<string | null>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;

    // Filter data
    const filteredNodes = filter
      ? ARCHITECTURE_DATA.nodes.filter(n => n.layer === filter)
      : ARCHITECTURE_DATA.nodes;
    const nodeIds = new Set(filteredNodes.map(n => n.id));
    const filteredEdges = ARCHITECTURE_DATA.edges.filter(
      e => nodeIds.has(e.source) && nodeIds.has(e.target)
    );

    // D3 Simulation
    const simulation = d3.forceSimulation(filteredNodes as any)
      .force('link', d3.forceLink(filteredEdges as any).id((d: any) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(40));

    // Clear previous
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    // Edges
    const link = svg.selectAll('line')
      .data(filteredEdges)
      .enter()
      .append('line')
      .attr('stroke', '#666')
      .attr('stroke-width', 2)
      .attr('opacity', 0.6);

    // Nodes
    const node = svg.selectAll('circle')
      .data(filteredNodes)
      .enter()
      .append('circle')
      .attr('r', (d: any) => 20 + d.readiness / 5)
      .attr('fill', (d: any) => {
        const healthColor = d3.interpolateRdYlGn(d.health / 100);
        return healthColor;
      })
      .attr('opacity', 0.8)
      .attr('stroke', (d: any) => d.id === selectedNode ? '#fff' : '#333')
      .attr('stroke-width', (d: any) => d.id === selectedNode ? 3 : 1)
      .on('click', (e: any, d: any) => setSelectedNode(d.id))
      .call(d3.drag()
        .on('start', dragStarted as any)
        .on('drag', dragged as any)
        .on('end', dragEnded as any)
      );

    // Labels
    const label = svg.selectAll('text')
      .data(filteredNodes)
      .enter()
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '.3em')
      .attr('font-size', '12px')
      .attr('fill', '#fff')
      .text((d: any) => d.name.split(' ')[0]);

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      label
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    });

    function dragStarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragEnded(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  }, [selectedNode, filter]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="bg-gray-800 p-4 flex gap-4 flex-wrap">
        <button
          onClick={() => setFilter(null)}
          className={`px-4 py-2 rounded ${!filter ? 'bg-blue-600' : 'bg-gray-700'}`}
        >
          All Layers
        </button>
        {['presentation', 'application', 'business', 'security', 'integration', 'persistence', 'analytics', 'research'].map(layer => (
          <button
            key={layer}
            onClick={() => setFilter(layer)}
            className={`px-4 py-2 rounded ${filter === layer ? 'bg-blue-600' : 'bg-gray-700'}`}
          >
            {layer}
          </button>
        ))}
      </div>
      <svg ref={svgRef} className="flex-1 bg-gray-900" />
      {selectedNode && (
        <div className="bg-gray-800 p-4 border-t border-gray-700">
          <h3 className="text-white font-bold mb-2">Selected: {selectedNode}</h3>
          <button
            onClick={() => setSelectedNode(null)}
            className="px-4 py-2 bg-gray-700 rounded hover:bg-gray-600"
          >
            Clear Selection
          </button>
        </div>
      )}
    </div>
  );
};

export default ArchitectureVisualizer;
