import axios from 'axios'
import { EvaluationResponse } from '../types'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

export const evaluateTranscript = async (
  transcript: string,
  durationSeconds?: number
): Promise<EvaluationResponse> => {
  const res = await axios.post(`${API_BASE}/api/v2/evaluate`, {
    transcript,
    duration_seconds: durationSeconds
  })
  return res.data
}