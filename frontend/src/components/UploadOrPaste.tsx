import React, { useRef } from 'react'

interface Props {
  transcript: string
  setTranscript: (v: string) => void
}

export default function UploadOrPaste({ transcript, setTranscript }: Props) {
  const fileRef = useRef<HTMLInputElement | null>(null)

  const onFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = ev => {
      setTranscript(String(ev.target?.result || ''))
    }
    reader.readAsText(file)
  }

  return (
    <div className="space-y-2">
      <textarea
        value={transcript}
        onChange={e => setTranscript(e.target.value)}
        placeholder="Paste transcript here..."
        className="w-full h-40 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand"
      />
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={() => fileRef.current?.click()}
          className="px-4 py-2 bg-brand dark:bg-brand-dark text-white rounded-md text-sm shadow hover:opacity-90 transition"
        >
          Upload .txt
        </button>
        <input
          ref={fileRef}
          type="file"
          accept=".txt"
          onChange={onFile}
          className="hidden"
        />
        <span className="text-xs text-gray-500 dark:text-gray-400">
          Optional: upload a .txt file.
        </span>
      </div>
    </div>
  )
}