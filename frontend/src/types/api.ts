export interface FilterOptions {
  cities: string[]
  bhk_min: number
  bhk_max: number
}

export interface Kpis {
  avg_rent: number
  median_size: number
  count: number
}

export interface Histogram {
  labels: string[]
  values: number[]
}

export interface ScatterPoint {
  x: number
  y: number
}

export interface Regression {
  slope: number
  intercept: number
  r_squared: number
  p_value: number
  std_err: number
}

export interface DashboardData {
  kpis: Kpis
  histogram: Histogram
  scatter: ScatterPoint[]
  regression: Regression
}

export interface InsightResponse {
  conclusion: string
}
