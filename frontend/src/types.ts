export interface MetricScore {
  id: string
  name: string
  raw_score: number
  max_score: number
  details: Record<string, any>
  feedback: string
}

export interface ExtractedDetails {
  name?: string | null
  age?: number | null
  school_class?: string | null
}

export interface EvaluationResponse {
  total_score: number
  max_total: number
  word_count: number
  sentence_count: number
  duration_seconds?: number
  wpm?: number | null
  metrics: MetricScore[]
  extracted: ExtractedDetails
  transcript_preview: string
  version: string
  performance_ms?: number
  notes?: string
}