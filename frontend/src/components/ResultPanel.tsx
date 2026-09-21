import { useState } from 'react'
import type { CompilationResult } from '../types/compiler'

type Props = {
  result: CompilationResult | null
  networkError: string | null
  loading: boolean
}

type Tab = 'summary' | 'errors' | 'ast' | 'jasmin'

export function ResultPanel({ result, networkError, loading }: Props) {
  const [tab, setTab] = useState<Tab>('summary')

  if (loading) return <div className="panel muted">Compiling with the OPLang pipeline…</div>
  if (networkError) {
    return (
      <div className="panel errorBox" role="alert">
        <strong>Could not reach the compiler API.</strong>
        <div>{networkError}</div>
      </div>
    )
  }
  if (!result) return <div className="panel muted">Compile a program to see results.</div>

  const jasminFiles = Object.entries(result.jasmin_files ?? {})

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
        <dl className="summary">
          <div><dt>Status</dt><dd>{result.success ? 'Success' : 'Failed'}</dd></div>
          <div><dt>Stage</dt><dd>{result.stage}</dd></div>
          <div><dt>Compilation time</dt><dd>{result.compilation_time_ms.toFixed(2)} ms</dd></div>
        </dl>
      )}
      {tab === 'errors' && (
        result.errors.length === 0
          ? <div className="emptyResult">No compiler errors.</div>
          : <ul className="compilerErrors">
              {result.errors.map((compilerError, index) => (
                <li key={`${compilerError.code}-${index}`}>
                  <strong>{compilerError.code}</strong>
                  <span>{compilerError.message}</span>
                </li>
              ))}
            </ul>
      )}
      {tab === 'ast' && <pre>{result.ast ? JSON.stringify(result.ast, null, 2) : 'No AST returned.'}</pre>}
      {tab === 'jasmin' && (
        jasminFiles.length === 0
          ? <div className="emptyResult">No Jasmin generated.</div>
          : jasminFiles.map(([name, code]) => (
              <section className="jasminFile" key={name}>
                <h3>{name}</h3>
                <pre>{code}</pre>
              </section>
            ))
      )}
    </div>
  )
}
