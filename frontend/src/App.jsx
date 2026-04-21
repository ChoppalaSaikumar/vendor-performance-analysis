import { useState } from 'react'
import { LayoutDashboard, BrainCircuit } from 'lucide-react'
import Dashboard from './Dashboard'

function App() {
  const [activeView, setActiveView] = useState('dashboard') // Default to dashboard
  const [formData, setFormData] = useState({
    Quality_Score: 8.5,
    Delivery_Time_Days: 14,
    Cost_Score: 7.5,
    Payment_Terms: 'Net 30',
    Region: 'North'
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: ['Quality_Score', 'Delivery_Time_Days', 'Cost_Score'].includes(name) 
        ? parseFloat(value) 
        : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      
      if (!response.ok) {
        const errData = await response.json()
        throw new Error(errData.detail || 'Failed to get prediction')
      }
      
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h1>Vendor Intelligence</h1>
      <p className="subtitle">Interactive Analysis & AI Performance Prediction</p>

      <div className="nav-container">
        <button 
          className={`nav-btn ${activeView === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveView('dashboard')}
        >
          <LayoutDashboard size={18} /> Dashboard
        </button>
        <button 
          className={`nav-btn ${activeView === 'predictor' ? 'active' : ''}`}
          onClick={() => setActiveView('predictor')}
        >
          <BrainCircuit size={18} /> Predictor
        </button>
      </div>
      
      {activeView === 'dashboard' ? (
        <Dashboard />
      ) : (
        <div className="app-container">
          {/* Form Panel */}
          <div className="glass-panel">
            <h2 style={{marginTop: 0, marginBottom: '1.5rem', fontSize: '1.25rem'}}>New Vendor Assessment</h2>
            {error && <div className="error-message">{error}</div>}
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="Quality_Score">Quality Score (1-10)</label>
                <input 
                  type="number" 
                  id="Quality_Score" 
                  name="Quality_Score" 
                  min="1" max="10" step="0.1" 
                  value={formData.Quality_Score} 
                  onChange={handleChange} 
                  required 
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="Delivery_Time_Days">Delivery Time (Days)</label>
                <input 
                  type="number" 
                  id="Delivery_Time_Days" 
                  name="Delivery_Time_Days" 
                  min="1" max="100" 
                  value={formData.Delivery_Time_Days} 
                  onChange={handleChange} 
                  required 
                />
              </div>

              <div className="form-group">
                <label htmlFor="Cost_Score">Cost Score (1-10)</label>
                <input 
                  type="number" 
                  id="Cost_Score" 
                  name="Cost_Score" 
                  min="1" max="10" step="0.1" 
                  value={formData.Cost_Score} 
                  onChange={handleChange} 
                  required 
                />
              </div>

              <div className="form-group">
                <label htmlFor="Payment_Terms">Payment Terms</label>
                <select 
                  id="Payment_Terms" 
                  name="Payment_Terms" 
                  value={formData.Payment_Terms} 
                  onChange={handleChange}
                >
                  <option value="Net 30">Net 30</option>
                  <option value="Net 60">Net 60</option>
                  <option value="Net 90">Net 90</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="Region">Region</label>
                <select 
                  id="Region" 
                  name="Region" 
                  value={formData.Region} 
                  onChange={handleChange}
                >
                  <option value="North">North</option>
                  <option value="South">South</option>
                  <option value="East">East</option>
                  <option value="West">West</option>
                </select>
              </div>

              <button type="submit" className="btn-submit" disabled={loading}>
                {loading ? 'Analyzing...' : 'Generate Prediction'}
              </button>
            </form>
          </div>

          {/* Results Panel */}
          <div className="glass-panel">
            <div className="results-container">
              {loading ? (
                <div className="loading-spinner"></div>
              ) : result ? (
                <>
                  <div className="result-label">Predicted Performance</div>
                  <div className={`score-circle score-${result.prediction_class}`}>
                    {result.prediction_class}
                  </div>
                  <div className="result-label">Classification</div>
                  <div className={`result-value value-${result.prediction_class}`}>
                    Tier {result.prediction_code + 1}
                  </div>
                </>
              ) : (
                <div className="result-placeholder">
                  Complete the vendor details to generate an AI-powered performance assessment.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default App
