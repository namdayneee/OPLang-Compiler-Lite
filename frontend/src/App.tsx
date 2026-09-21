import { useEffect, useState } from 'react'
import { CodeEditor } from './components/CodeEditor'
import { ResultPanel } from './components/ResultPanel'
import { compileSource } from './services/compilerApi'
import type { CompilationResult } from './types/compiler'
import './styles.css'

const DEFAULT_SOURCE = `class Main {
    static void main() {
        io.writeIntLn(10);
    }
}`

export default function App() {
  const [source, setSource] = useState(() => localStorage.getItem('oplang-source') ?? DEFAULT_SOURCE)
  const [result, setResult] = useState<CompilationResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    localStorage.setItem('oplang-source', source)
  }, [source])

  async function onCompile() {
    setLoading(true)
    setError(null)
    try {
      setResult(await compileSource(source))
    } catch (e) {
      setResult(null)
      setError(e instanceof Error ? e.message : 'Compilation request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main>
      <header>
        <div>
          <h1>OPLang Compiler Lite</h1>
          <p>OPLang → Lexer → Parser → AST → Semantic Check → Jasmin</p>
        </div>
        <button className="compileButton" onClick={onCompile} disabled={loading}>
          {loading ? 'Compiling…' : 'Compile ▶'}
        </button>
      </header>

      <section className="workspace">
        <div className="column">
          <div className="sectionTitle">Source Code</div>
          <CodeEditor value={source} onChange={setSource} />
        </div>
        <div className="column">
          <div className="sectionTitle">Result</div>
          <ResultPanel result={result} error={error} />
        </div>
      </section>
    </main>
  )
}
