import { ScoreResponse } from '../types'

interface Props {
  data: ScoreResponse | null
  loading: boolean
  onExport: () => void
}

export default function ResultSummary({ data, loading, onExport }: Props) {
  if (loading) return <div className="animate-pulse text-sm">Scoring transcript...</div>
  if (!data) return null
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Results</h2>
        <button
          onClick={onExport}
            className="px-3 py-1.5 text-xs rounded-md bg-brand dark:bg-brand-dark text-white hover:opacity-90 shadow"
        >
          Export JSON
        </button>
      </div>
      <div className="flex flex-wrap gap-4">
        <SummaryCard label="Overall Score" value={`${data.overall_score.toFixed(2)}`} accent="bg-brand text-white" />
        <SummaryCard label="Word Count" value={data.word_count.toString()} />
        <SummaryCard label="Criteria Count" value={data.criteria.length.toString()} />
        <SummaryCard label="API Version" value={data.version} />
      </div>
      <div className="text-xs text-gray-500 dark:text-gray-400">
        Preview: {data.transcript_preview}
      </div>
    </div>
  )
}

function SummaryCard({ label, value, accent }: { label: string; value: string; accent?: string }) {
  return (
    <div className={`rounded-md border border-gray-200 dark:border-gray-700 p-3 flex flex-col ${accent ? accent : 'bg-gray-100 dark:bg-gray-800'}`}>
      <span className="text-[11px] uppercase tracking-wide opacity-80">{label}</span>
      <span className="text-sm font-semibold">{value}</span>
    </div>
  )
}