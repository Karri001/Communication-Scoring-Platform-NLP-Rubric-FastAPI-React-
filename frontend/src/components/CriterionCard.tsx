import { CriterionScore } from '../types'
import { clsx } from 'clsx'
import { CheckCircle, AlertCircle } from 'lucide-react'

interface Props {
  c: CriterionScore
}

export default function CriterionCard({ c }: Props) {
  const bandColor = {
    High: 'bg-green-100 text-green-700 dark:bg-green-800 dark:text-green-200',
    Moderate: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-800 dark:text-yellow-200',
    Low: 'bg-red-100 text-red-700 dark:bg-red-800 dark:text-red-200'
  }[c.alignment_band]

  return (
    <div className="rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800 shadow-sm space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-sm">{c.name}</h3>
        <span className={clsx("px-2 py-0.5 rounded text-xs font-medium", bandColor)}>
          {c.alignment_band} alignment
        </span>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
        <Metric label="Keyword" value={c.keyword_score} />
        <Metric label="Semantic" value={c.semantic_score} />
        <Metric label="Length" value={c.length_score} />
        <Metric label="Combined" value={c.combined_score} />
      </div>
      <div className="text-xs space-y-1">
        <LineList title="Found" items={c.keywords_found} icon={<CheckCircle size={12} className="text-green-600" />} />
        <LineList title="Missing" items={c.keywords_missing} icon={<AlertCircle size={12} className="text-red-600" />} />
      </div>
      <p className="text-xs leading-relaxed text-gray-600 dark:text-gray-300">{c.feedback}</p>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded h-2">
        <div
          className="h-2 rounded bg-brand dark:bg-brand-dark"
          style={{ width: `${Math.min(100, c.combined_score * 100)}%` }}
        />
      </div>
      <div className="text-right text-[11px] text-gray-500">Weight: {(c.weight * 100).toFixed(0)}%</div>
    </div>
  )
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex flex-col">
      <span className="text-[11px] text-gray-500">{label}</span>
      <span className="font-semibold">{value.toFixed(2)}</span>
    </div>
  )
}

function LineList({ title, items, icon }: { title: string; items: string[]; icon: React.ReactNode }) {
  return (
    <div className="flex flex-wrap gap-1">
      <span className="text-[11px] font-medium">{title}:</span>
      {items.length === 0 && <span className="text-[11px] italic text-gray-400">None</span>}
      {items.map(i => (
        <span key={i} className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-[11px]">
          {icon}{i}
        </span>
      ))}
    </div>
  )
}