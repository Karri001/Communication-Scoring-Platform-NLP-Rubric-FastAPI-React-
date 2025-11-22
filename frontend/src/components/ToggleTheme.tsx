import { useEffect, useState } from 'react'
import { Moon, Sun } from 'lucide-react'

export default function ToggleTheme() {
  const [dark, setDark] = useState(false)

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [dark])

  return (
    <button
      onClick={() => setDark(d => !d)}
      className="px-3 py-2 rounded-md bg-gray-200 dark:bg-gray-700 text-sm flex items-center gap-2 transition"
    >
      {dark ? <Sun size={16} /> : <Moon size={16} />}
      {dark ? 'Light' : 'Dark'}
    </button>
  )
}