import { useState } from 'react'
import type { CompilationResult } from '../types/compiler'

type Props = {
  result: CompilationResult | null
  error: string | null
}

type Tab = 'summary' | 'errors' | 'ast' | 'jasmin'

export function ResultPanel({ result, error }: Props) {
  const [tab, setTab] = useState<Tab>('summary')

  if (error) return <div className="panel errorBox">{error}</div>
  if (!result) return <div className="panel muted">Compile a program to see results.</div>

  const jasmin = Object.entries(result.jasmin_files ?? {})
    .map(([name, code]) => `// ${name}\n${code}`)
    .join('\n\n')

  return (
    <div className="panel resultPanel">
      <div className="tabs">
        {(['summary', 'errors', 'ast', 'jasmin'] as Tab[]).map((name) => (
          <button key={name} className={tab === name ? 'active' : ''} onClick={() => setTab(name)}>
            {name.toUpperCase()}
          </button>
        ))}
      </div>

      {tab === 'summary' && (
        <pre>{JSON.stringify({ success: result.success, stage: result.stage, compilation_time_ms: result.compilation_time_ms }, null, 2)}</pre>
      )}
      {tab === 'errors' && <pre>{JSON.stringify(result.errors, null, 2)}</pre>}
      {tab === 'ast' && <pre>{JSON.stringify(result.ast, null, 2)}</pre>}
      {tab === 'jasmin' && <pre>{jasmin || 'No Jasmin generated.'}</pre>}
    </div>
  )
}
