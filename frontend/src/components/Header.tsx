import type { CompilerExample } from '../data/examples'

interface HeaderProps {
  examples: readonly CompilerExample[]
  loading: boolean
  onCompile: () => void
  onSelectExample: (example: CompilerExample) => void
}

export function Header({
  examples,
  loading,
  onCompile,
  onSelectExample
}: HeaderProps) {
  return (
    <header>
      <div>
        <h1>OPLang Compiler Lite</h1>
        <p>OPLang → Lexer → Parser → AST → Semantic Check → Jasmin</p>
      </div>
      <div className="headerActions">
        <label htmlFor="example-select">Example</label>
        <select
          id="example-select"
          defaultValue=""
          onChange={(event) => {
            const example = examples.find(({ id }) => id === event.target.value)
            if (example) onSelectExample(example)
          }}
        >
          <option value="" disabled>
            Choose a program…
          </option>
          {examples.map((example) => (
            <option key={example.id} value={example.id}>
              {example.name}
            </option>
          ))}
        </select>
        <button className="compileButton" onClick={onCompile} disabled={loading}>
          {loading ? 'Compiling…' : 'Compile (Ctrl/Cmd+Enter)'}
        </button>
      </div>
    </header>
  )
}
