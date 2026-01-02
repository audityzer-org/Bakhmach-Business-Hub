'use client';

import React, { useEffect, useState } from 'react';

interface HealthMetrics {
  nodeId: string;
  nodeName: string;
  health: number;
  readiness: number;
  latency: number;
  status: 'healthy' | 'degraded' | 'critical';
}

interface SystemStats {
  totalNodes: number;
  healthyNodes: number;
  avgHealth: number;
  avgLatency: number;
  requestsPerSecond: number;
}

const RealtimeDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<HealthMetrics[]>([]);
  const [stats, setStats] = useState<SystemStats>({
    totalNodes: 0,
    healthyNodes: 0,
    avgHealth: 0,
    avgLatency: 0,
    requestsPerSecond: 0,
  });
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const mockMetrics: HealthMetrics[] = [
      { nodeId: 'frontend', nodeName: 'Frontend Layer', health: 100, readiness: 95, latency: 45, status: 'healthy' },
      { nodeId: 'api-gateway', nodeName: 'API Gateway', health: 98, readiness: 99, latency: 12, status: 'healthy' },
      { nodeId: 'auth-service', nodeName: 'Auth Service', health: 99, readiness: 100, latency: 8, status: 'healthy' },
      { nodeId: 'ml-pipeline', nodeName: 'ML Pipeline', health: 95, readiness: 85, latency: 250, status: 'degraded' },
      { nodeId: 'database', nodeName: 'PostgreSQL DB', health: 100, readiness: 100, latency: 5, status: 'healthy' },
    ];

    setMetrics(mockMetrics);
    setIsConnected(true);

    const healthyCount = mockMetrics.filter((m) => m.status === 'healthy').length;
    const avgHealth = mockMetrics.reduce((sum, m) => sum + m.health, 0) / mockMetrics.length;
    const avgLatency = mockMetrics.reduce((sum, m) => sum + m.latency, 0) / mockMetrics.length;

    setStats({
      totalNodes: mockMetrics.length,
      healthyNodes: healthyCount,
      avgHealth: Math.round(avgHealth),
      avgLatency: Math.round(avgLatency),
      requestsPerSecond: 15234,
    });
    setLastUpdate(new Date());
  }, []);

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'healthy':
        return '#10b981';
      case 'degraded':
        return '#f59e0b';
      case 'critical':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'system-ui' }}>
      <div style={{ marginBottom: '30px' }}>
        <h1>System Health Dashboard</h1>
        <div style={{ color: isConnected ? '#10b981' : '#ef4444', fontSize: '14px' }}>
          {isConnected ? 'Connected' : 'Disconnected'} - Updated {lastUpdate.toLocaleTimeString()}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '30px' }}>
        <div style={{ border: '1px solid #e5e7eb', padding: '15px', borderRadius: '8px' }}>
          <div style={{ fontSize: '12px', color: '#6b7280' }}>Overall Health</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', color: stats.avgHealth > 95 ? '#10b981' : '#f59e0b' }}>
            {stats.avgHealth}%
          </div>
        </div>
        <div style={{ border: '1px solid #e5e7eb', padding: '15px', borderRadius: '8px' }}>
          <div style={{ fontSize: '12px', color: '#6b7280' }}>Healthy Nodes</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold' }}>
            {stats.healthyNodes}/{stats.totalNodes}
          </div>
        </div>
        <div style={{ border: '1px solid #e5e7eb', padding: '15px', borderRadius: '8px' }}>
          <div style={{ fontSize: '12px', color: '#6b7280' }}>Avg Latency</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold' }}>{stats.avgLatency}ms</div>
        </div>
        <div style={{ border: '1px solid #e5e7eb', padding: '15px', borderRadius: '8px' }}>
          <div style={{ fontSize: '12px', color: '#6b7280' }}>Requests/Sec</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold' }}>{stats.requestsPerSecond.toLocaleString()}</div>
        </div>
      </div>

      <div>
        <h2>Node Metrics</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #e5e7eb' }}>
              <th style={{ textAlign: 'left', padding: '10px', fontWeight: 'bold' }}>Node</th>
              <th style={{ textAlign: 'left', padding: '10px', fontWeight: 'bold' }}>Health</th>
              <th style={{ textAlign: 'left', padding: '10px', fontWeight: 'bold' }}>Readiness</th>
              <th style={{ textAlign: 'left', padding: '10px', fontWeight: 'bold' }}>Latency</th>
              <th style={{ textAlign: 'left', padding: '10px', fontWeight: 'bold' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {metrics.map((metric) => (
              <tr key={metric.nodeId} style={{ borderBottom: '1px solid #f3f4f6' }}>
                <td style={{ padding: '10px' }}>{metric.nodeName}</td>
                <td style={{ padding: '10px' }}>
                  <div style={{ display: 'inline-block', width: '60px', height: '20px', backgroundColor: '#e5e7eb', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${metric.health}%`, backgroundColor: getStatusColor(metric.status) }} />
                  </div>
                  {metric.health}%
                </td>
                <td style={{ padding: '10px' }}>{metric.readiness}%</td>
                <td style={{ padding: '10px' }}>{metric.latency}ms</td>
                <td style={{ padding: '10px' }}>
                  <span style={{ display: 'inline-block', padding: '4px 12px', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', color: 'white', backgroundColor: getStatusColor(metric.status) }}>
                    {metric.status.charAt(0).toUpperCase() + metric.status.slice(1)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RealtimeDashboard;
export { HealthMetrics, SystemStats };
