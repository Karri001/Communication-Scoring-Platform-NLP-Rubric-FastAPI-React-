import { useState } from 'react'
import ToggleTheme from './components/ToggleTheme'
import UploadOrPaste from './components/UploadOrPaste'
import { evaluateTranscript } from './services/api'
import { EvaluationResponse } from './types'
import toast, { Toaster } from 'react-hot-toast'

export default function App() {
  const [text, setText] = useState('')
  const [duration, setDuration] = useState('')
  const [result, setResult] = useState<EvaluationResponse | null>(null)
  const [loading, setLoading] = useState(false)

  const onSubmit = async () => {
    const wc = text.trim().split(/\s+/).filter(Boolean).length
    if (wc === 0) {
      toast.error('Transcript empty')
      return
    }
    if (wc < 40) {
      toast('Warning: Transcript is short (<40 words), scores may be low.', { icon: '⚠️' })
    }
    const durVal = duration.trim() ? parseFloat(duration) : undefined
    if (durVal !== undefined && (isNaN(durVal) || durVal <= 0)) {
      toast.error('Duration must be a positive number')
      return
    }
    setLoading(true)
    try {
      const data = await evaluateTranscript(text, durVal)
      setResult(data)
      toast.success('Evaluated')
    } catch (e: any) {
      toast.error(e?.response?.data?.detail || 'Error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <Toaster position="top-right" />
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-brand">Communication Scoring Platform (v2.1)</h1>
        <ToggleTheme />
      </header>

      <div className="space-y-4 bg-white dark:bg-gray-800 p-5 rounded-lg shadow border border-gray-200 dark:border-gray-700">
        <UploadOrPaste transcript={text} setTranscript={setText} />
        <div className="flex gap-3 items-end">
          <div className="flex flex-col">
            <label className="text-xs mb-1">Duration (seconds, optional)</label>
            <input
              value={duration}
              onChange={e => setDuration(e.target.value)}
              placeholder="e.g. 52"
              className="px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-sm w-28 focus:outline-none focus:ring-2 focus:ring-brand"
            />
          </div>
          <button
            onClick={onSubmit}
            disabled={loading}
            className="px-5 py-2 rounded-md bg-brand dark:bg-brand-dark text-white text-sm disabled:opacity-50"
          >
            {loading ? 'Scoring...' : 'Score'}
          </button>
        </div>
      </div>

      {result && (
        <div className="space-y-4">
          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow border border-gray-200 dark:border-gray-700">
            <h2 className="font-semibold mb-2">Overall</h2>
            <div className="flex flex-wrap gap-4 text-sm">
              <Stat label="Total" value={`${result.total_score} / ${result.max_total}`} />
              <Stat label="Words" value={result.word_count.toString()} />
              <Stat label="Sentences" value={result.sentence_count.toString()} />
              <Stat label="WPM" value={result.wpm ? result.wpm.toString() : '—'} />
              <Stat label="Version" value={result.version} />
              <Stat label="Time (ms)" value={result.performance_ms?.toString() || '—'} />
            </div>
            <div className="mt-3 text-xs space-y-1 text-gray-600 dark:text-gray-300">
              {result.extracted.name && <div>Name: {result.extracted.name}</div>}
              {result.extracted.age && <div>Age: {result.extracted.age}</div>}
              {result.extracted.school_class && <div>School/Class: {result.extracted.school_class}</div>}
              <div>Preview: {result.transcript_preview}</div>
              {result.notes && <div className="italic">Note: {result.notes}</div>}
            </div>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {result.metrics.map(m => (
              <div key={m.id} className="p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-semibold">{m.name}</h3>
                  <span className="text-xs font-medium bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded">
                    {m.raw_score} / {m.max_score}
                  </span>
                </div>
                <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded">
                  <div
                    className="h-2 rounded bg-brand dark:bg-brand-dark"
                    style={{ width: `${(m.raw_score / m.max_score) * 100}%` }}
                  />
                </div>
                <p className="text-[11px] mt-2 text-gray-600 dark:text-gray-300">{m.feedback}</p>
                <details className="text-[11px] mt-2">
                  <summary className="cursor-pointer text-brand">Details</summary>
                  <pre className="mt-1 bg-gray-100 dark:bg-gray-900 p-2 rounded overflow-auto max-h-44">
{JSON.stringify(m.details, null, 2)}
                  </pre>
                </details>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col px-3 py-2 rounded bg-gray-100 dark:bg-gray-700">
      <span className="text-[10px] uppercase tracking-wide opacity-70">{label}</span>
      <span className="text-sm font-semibold">{value}</span>
    </div>
  )
}