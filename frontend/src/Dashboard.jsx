import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, ScatterChart, Scatter, ZAxis
} from 'recharts';
import { 
  Activity, Users, Globe, Award, TrendingUp, Filter, RefreshCw, AlertCircle
} from 'lucide-react';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterRegion, setFilterRegion] = useState('All');

  const fetchData = async () => {
    setLoading(true);
    try {
      const [statsRes, vendorsRes] = await Promise.all([
        fetch('http://localhost:8000/stats'),
        fetch('http://localhost:8000/vendors')
      ]);

      if (!statsRes.ok || !vendorsRes.ok) throw new Error('Failed to fetch dashboard data');

      const statsData = await statsRes.json();
      const vendorsData = await vendorsRes.json();

      setStats(statsData);
      setVendors(vendorsData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredVendors = filterRegion === 'All' 
    ? vendors 
    : vendors.filter(v => v.Region === filterRegion);

  if (loading) return (
    <div className="dashboard-loading">
      <RefreshCw className="animate-spin" size={48} />
      <p>Analyzing Vendor Ecosystem...</p>
    </div>
  );

  if (error) return (
    <div className="dashboard-error">
      <AlertCircle size={48} />
      <p>Error: {error}</p>
      <button onClick={fetchData} className="btn-retry">Retry Connection</button>
    </div>
  );

  return (
    <div className="dashboard-content">
      {/* KPI Section */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon blue"><Users /></div>
          <div className="kpi-info">
            <span className="kpi-label">Total Vendors</span>
            <span className="kpi-value">{stats.total_vendors}</span>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon green"><Award /></div>
          <div className="kpi-info">
            <span className="kpi-label">Avg Quality</span>
            <span className="kpi-value">{stats.averages.quality}/10</span>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon yellow"><TrendingUp /></div>
          <div className="kpi-info">
            <span className="kpi-label">Avg Delivery</span>
            <span className="kpi-value">{stats.averages.delivery} days</span>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon purple"><Globe /></div>
          <div className="kpi-info">
            <span className="kpi-label">Avg Cost Score</span>
            <span className="kpi-value">{stats.averages.cost}/10</span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        <div className="chart-card glass-panel">
          <h3>Performance Distribution</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats.class_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {stats.class_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card glass-panel">
          <h3>Regional Distribution</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats.region_distribution}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card glass-panel wide">
          <div className="chart-header">
            <h3>Quality vs Cost Correlation</h3>
            <div className="chart-legend">
              <span className="dot high"></span> High
              <span className="dot medium"></span> Medium
              <span className="dot low"></span> Low
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 10 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                <XAxis 
                  type="number" 
                  dataKey="Quality_Score" 
                  name="Quality" 
                  domain={[0, 10]} 
                  label={{ value: 'Quality Score', position: 'insideBottom', offset: -10, fill: '#94a3b8' }}
                  tick={{fill: '#94a3b8'}}
                />
                <YAxis 
                  type="number" 
                  dataKey="Cost_Score" 
                  name="Cost" 
                  domain={[0, 10]}
                  label={{ value: 'Cost Score', angle: -90, position: 'insideLeft', fill: '#94a3b8' }}
                  tick={{fill: '#94a3b8'}}
                />
                <ZAxis type="number" dataKey="Performance_Score" range={[60, 400]} name="Performance" />
                <Tooltip 
                  cursor={{ strokeDasharray: '3 3' }} 
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="custom-tooltip">
                          <p className="label">{`Performance: ${data.Performance_Score.toFixed(2)}`}</p>
                          <p className="desc">{`Quality: ${data.Quality_Score} | Cost: ${data.Cost_Score}`}</p>
                          <p className={`cat ${data.Category.toLowerCase()}`}>{data.Category} Tier</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Scatter 
                  name="High" 
                  data={stats.scatter_data.filter(d => d.Category === 'High')} 
                  fill="#10b981" 
                />
                <Scatter 
                  name="Medium" 
                  data={stats.scatter_data.filter(d => d.Category === 'Medium')} 
                  fill="#f59e0b" 
                />
                <Scatter 
                  name="Low" 
                  data={stats.scatter_data.filter(d => d.Category === 'Low')} 
                  fill="#ef4444" 
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Data Table Section */}
      <div className="table-section glass-panel">
        <div className="table-header">
          <h3>Vendor Directory</h3>
          <div className="table-actions">
            <Filter size={18} />
            <select value={filterRegion} onChange={(e) => setFilterRegion(e.target.value)}>
              <option value="All">All Regions</option>
              <option value="North">North</option>
              <option value="South">South</option>
              <option value="East">East</option>
              <option value="West">West</option>
            </select>
          </div>
        </div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Quality</th>
                <th>Delivery (Days)</th>
                <th>Cost</th>
                <th>Terms</th>
                <th>Region</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredVendors.slice(0, 10).map((vendor, i) => (
                <tr key={i}>
                  <td><div className="badge quality">{vendor.Quality_Score}</div></td>
                  <td>{vendor.Delivery_Time_Days}</td>
                  <td>{vendor.Cost_Score}</td>
                  <td>{vendor.Payment_Terms}</td>
                  <td>{vendor.Region}</td>
                  <td>
                    <span className={`status-pill ${vendor.Performance_Score > 7 ? 'high' : vendor.Performance_Score > 4 ? 'medium' : 'low'}`}>
                      {vendor.Performance_Score > 7 ? 'Optimal' : vendor.Performance_Score > 4 ? 'Stable' : 'Risk'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
